import json
import urllib.error
import urllib.request

import pytest

from hyperdb import HypergraphDB
from hyperdb.admin import HypergraphAdmin


@pytest.fixture()
def server(tmp_path):
    db = HypergraphDB(storage_file=tmp_path / "admin.hgdb")
    db.add_v(1, {"name": "Alice", "entity_type": "person"})
    db.add_v(2, {"name": "Bob", "entity_type": "person"})
    db.add_v(3, {"name": "Charlie", "entity_type": "person"})
    db.add_v(4, {"name": "Paper", "entity_type": "doc"})
    db.add_e((1, 2), {"relation": "knows"})
    db.add_e((1, 2, 3, 4), {"relation": "wrote"})
    admin = HypergraphAdmin(db, port=0)
    admin.start_server(open_browser=False)
    yield admin
    admin.stop_server()


def call(admin, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(admin.url + path, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_pages_served(server):
    with urllib.request.urlopen(server.url + "/") as res:
        assert b"Hypergraph DB Admin" in res.read()
    with urllib.request.urlopen(server.url + "/viewer") as res:
        assert b"Hypergraph Visualization" in res.read()


def test_hypergraph_layout_served(server):
    # 查看器页面通过 <script src="hypergraph_layout.js"> 加载超图布局，/viewer 与 / 下都解析到同一路径
    with urllib.request.urlopen(server.url + "/hypergraph_layout.js") as res:
        assert res.headers["Content-Type"].startswith("application/javascript")
        assert "G6.register(G6.ExtensionCategory.LAYOUT, 'hypergraph'" in res.read().decode("utf-8")


def test_info_and_stats(server):
    status, info = call(server, "/api/admin/info")
    assert status == 200
    assert info["num_v"] == 4 and info["num_e"] == 2 and info["dirty"] is False

    _, stats = call(server, "/api/admin/stats")
    assert stats["max_degree"] == 2
    assert stats["edge_size_hist"] == [[2, 1], [4, 1]]
    assert stats["entity_types"][0] == ["person", 3]
    assert stats["edge_types"] == []

    server.hypergraph_db.update_e((1, 2), {"type": "social"})
    _, stats = call(server, "/api/admin/stats")
    assert stats["edge_types"] == [["social", 1]]


def test_list_vertices_and_edges(server):
    _, res = call(server, "/api/admin/vertices?search=bob")
    assert [v["id"] for v in res["data"]] == [2]

    _, res = call(server, "/api/admin/vertices?entity_type=doc")
    assert [v["id"] for v in res["data"]] == [4]

    _, res = call(server, "/api/admin/vertices?page_size=2&page=2")
    assert len(res["data"]) == 2 and res["pagination"]["total_pages"] == 2

    _, res = call(server, "/api/admin/edges?search=wrote")
    assert res["data"][0]["size"] == 4

    _, res = call(server, "/api/admin/edges?vertex=3")
    assert res["pagination"]["total"] == 1

    server.hypergraph_db.update_e((1, 2), {"type": "social"})
    _, res = call(server, "/api/admin/edges?edge_type=social")
    assert [e["size"] for e in res["data"]] == [2]


def test_vertex_crud(server):
    db = server.hypergraph_db
    status, res = call(server, "/api/admin/vertex/upsert", {"create": True, "id": 5, "data": {"name": "Eve"}})
    assert status == 200 and db.v(5) == {"name": "Eve"}

    status, _ = call(server, "/api/admin/vertex/upsert", {"create": True, "id": 5})
    assert status == 409

    # Merge vs replace
    call(server, "/api/admin/vertex/upsert", {"id": 5, "data": {"age": 30}})
    assert db.v(5) == {"name": "Eve", "age": 30}
    call(server, "/api/admin/vertex/upsert", {"id": 5, "data": {"age": 31}, "replace": True})
    assert db.v(5) == {"age": 31}

    _, detail = call(server, "/api/admin/vertex/get", {"id": 1})
    assert detail["degree"] == 2 and detail["neighbors"] == 3

    call(server, "/api/admin/vertex/delete", {"id": 2})
    assert not db.has_v(2) and db.num_e == 1  # (1, 2) dropped below 2 vertices

    status, _ = call(server, "/api/admin/vertex/get", {"id": 99})
    assert status == 404
    assert call(server, "/api/admin/info")[1]["dirty"] is True


def test_edge_crud(server):
    db = server.hypergraph_db
    status, res = call(server, "/api/admin/edge/upsert", {"create": True, "vertices": [3, 4], "data": {"w": 1}})
    assert status == 200 and db.e((3, 4)) == {"w": 1}

    status, _ = call(server, "/api/admin/edge/upsert", {"create": True, "vertices": [4, 3]})
    assert status == 409
    status, _ = call(server, "/api/admin/edge/upsert", {"create": True, "vertices": [1, 42]})
    assert status == 404
    status, _ = call(server, "/api/admin/edge/upsert", {"create": True, "vertices": [1]})
    assert status == 400

    call(server, "/api/admin/edge/upsert", {"vertices": [3, 4], "data": {"x": 2}, "replace": True})
    assert db.e((3, 4)) == {"x": 2}

    call(server, "/api/admin/edge/delete", {"vertices": [3, 4]})
    assert not db.has_e((3, 4))


def test_save_and_hif_roundtrip(server):
    db = server.hypergraph_db
    call(server, "/api/admin/vertex/upsert", {"create": True, "id": "new"})
    status, info = call(server, "/api/admin/save", {})
    assert status == 200 and info["dirty"] is False and info["file_exists"]
    assert HypergraphDB(storage_file=db.storage_file).has_v("new")

    _, hif = call(server, "/api/admin/hif")
    assert "incidences" in hif

    status, _ = call(server, "/api/admin/hif", {"nope": []})
    assert status == 400
    status, info = call(
        server, "/api/admin/hif", {"incidences": [{"edge": "e", "node": "a"}, {"edge": "e", "node": "b"}]}
    )
    assert status == 200 and info["num_v"] == 2 and info["num_e"] == 1 and info["dirty"] is True


def test_bad_requests(server):
    assert call(server, "/api/admin/nope")[0] == 404
    assert call(server, "/api/admin/vertex/upsert", {"id": 1, "data": [1, 2]})[0] == 400
    assert call(server, "/api/admin/vertex/upsert", {"create": True, "id": ""})[0] == 400


def test_viewer_graph_accepts_non_string_ids(server):
    with urllib.request.urlopen(server.url + "/api/graph?vertex_id=1") as res:
        data = json.loads(res.read())
    assert "error" not in data and len(data["edges"]) == 2


def test_vertex_search_ranks_id_matches_first(server):
    # "bobby" has degree 0 but matches by id, so it outranks attribute-only matches with higher degree
    call(server, "/api/admin/vertex/upsert", {"create": True, "id": "bobby"})
    _, res = call(server, "/api/admin/vertices?search=bob")
    assert [v["id"] for v in res["data"]] == ["bobby", 2]


def test_labels(tmp_path):
    db = HypergraphDB(storage_file=tmp_path / "labeled.hgdb")
    db.add_v(1, {"entity_type": "person"})
    labels = {"zh": {"entity_type": {"person": "人物"}}}

    # Default: <name>.labels.json next to the storage file, re-read on every /info
    admin = HypergraphAdmin(db, port=0)
    admin.start_server(open_browser=False)
    try:
        assert call(admin, "/api/admin/info")[1]["labels"] == {}
        (tmp_path / "labeled.labels.json").write_text(json.dumps(labels), encoding="utf-8")
        assert call(admin, "/api/admin/info")[1]["labels"] == labels
        (tmp_path / "labeled.labels.json").write_text("not json", encoding="utf-8")
        assert call(admin, "/api/admin/info")[1]["labels"] == {}
    finally:
        admin.stop_server()

    # Explicit labels win over the file
    explicit = {"en": {"key": {"entity_type": "Kind"}}}
    admin = HypergraphAdmin(db, port=0, labels=explicit)
    admin.start_server(open_browser=False)
    try:
        assert call(admin, "/api/admin/info")[1]["labels"] == explicit
    finally:
        admin.stop_server()
