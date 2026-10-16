"""
Web-based management console for HypergraphDB.

Provides a local HTTP server with a REST API for browsing, creating, editing and
deleting vertices / hyperedges, viewing statistics, saving the database and
importing / exporting HIF files. The existing hypergraph viewer is served at
``/viewer`` from the same server.

Usage::

    db.admin()
"""

import json
import socketserver
import threading
import time
import webbrowser
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

from .base import BaseHypergraphDB
from .draw import HypergraphAPIHandler

MAX_BODY_SIZE = 200 * 1024 * 1024  # 200 MB, enough for large HIF imports


class AdminAPIError(Exception):
    """Error that is reported to the client as a JSON error response."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status


def _json_safe(value: Any) -> Any:
    """Convert a value into something json.dumps can serialize."""
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


def _preview(data: Any, limit: int = 120) -> str:
    text = json.dumps(data, ensure_ascii=False, default=str)
    return text if len(text) <= limit else text[:limit] + "..."


class AdminState:
    """Mutable state shared across requests (the handler is re-created for every request)."""

    def __init__(self, hypergraph_db: BaseHypergraphDB):
        self.hypergraph_db = hypergraph_db
        self.dirty = False
        self.last_saved: Optional[float] = None


class HypergraphAdminHandler(HypergraphAPIHandler):
    """HTTP request handler for the admin console.

    Admin endpoints live under ``/api/admin``. Every other GET path falls back to
    the viewer handler, so ``/api/vertices`` and ``/api/graph`` keep working for
    the embedded visualization page at ``/viewer``.
    """

    def __init__(self, state: AdminState, *args, **kwargs):
        self.state = state
        super().__init__(state.hypergraph_db, *args, **kwargs)

    # ------------------------------------------------------------------ routing

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        if path in ("/", "/admin", "/index.html"):
            self._send_html(self._read_template("admin.html"))
        elif path == "/viewer":
            self._send_html(self._get_html_template())
        elif path == "/api/admin/hif":
            self._handle(lambda: self.hypergraph_db.to_hif(), download="hypergraph.hif.json")
        elif path.startswith("/api/admin/"):
            routes = {
                "/api/admin/info": self._info,
                "/api/admin/stats": self._stats,
                "/api/admin/vertices": lambda: self._list_vertices(params),
                "/api/admin/edges": lambda: self._list_edges(params),
            }
            if path in routes:
                self._handle(routes[path])
            else:
                self._send_json({"error": f"Unknown endpoint: {path}"}, 404)
        else:
            super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        routes = {
            "/api/admin/vertex/get": self._get_vertex,
            "/api/admin/vertex/upsert": self._upsert_vertex,
            "/api/admin/vertex/delete": self._delete_vertex,
            "/api/admin/edge/get": self._get_edge,
            "/api/admin/edge/upsert": self._upsert_edge,
            "/api/admin/edge/delete": self._delete_edge,
            "/api/admin/save": self._save,
            "/api/admin/hif": self._import_hif,
        }
        if path not in routes:
            self._send_json({"error": f"Unknown endpoint: {path}"}, 404)
            return
        self._handle(lambda: routes[path](self._read_body()))

    # ------------------------------------------------------------------ helpers

    def _handle(self, fn, download: Optional[str] = None):
        try:
            result = fn()
        except AdminAPIError as e:
            self._send_json({"error": e.message}, e.status)
            return
        except AssertionError as e:
            self._send_json({"error": str(e) or "Invalid request"}, 400)
            return
        except Exception as e:  # pragma: no cover - defensive
            self._send_json({"error": f"{type(e).__name__}: {e}"}, 500)
            return
        self._send_json(result, 200, download=download)

    def _send_json(self, payload: Any, status: int = 200, download: Optional[str] = None):
        body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if download:
            self.send_header("Content-Disposition", f'attachment; filename="{download}"')
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_template(self, name: str) -> str:
        return (Path(__file__).parent / "templates" / name).read_text(encoding="utf-8")

    def _read_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY_SIZE:
            raise AdminAPIError("Request body too large", 413)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise AdminAPIError(f"Invalid JSON body: {e}")
        if not isinstance(body, dict):
            raise AdminAPIError("Request body must be a JSON object")
        return body

    def _resolve_v(self, raw: Any) -> Any:
        """Map a vertex id received as JSON back to the actual id stored in the DB.

        JSON-native ids (str / int / float) match directly; other hashable ids
        (e.g. tuples) are sent to the client as strings and matched by ``str()``.
        """
        hg = self.hypergraph_db
        if isinstance(raw, list):
            raw = tuple(raw)
        try:
            if hg.has_v(raw):
                return raw
        except (AssertionError, TypeError):
            pass
        for v_id in hg.all_v:
            if str(v_id) == str(raw):
                return v_id
        raise AdminAPIError(f"Vertex {raw!r} does not exist", 404)

    def _resolve_e(self, raw: Any) -> Tuple:
        if not isinstance(raw, list) or len(raw) < 2:
            raise AdminAPIError("A hyperedge must be a list of at least 2 vertex ids")
        return self.hypergraph_db.encode_e([self._resolve_v(v) for v in raw])

    @staticmethod
    def _require_dict(body: Dict[str, Any], key: str) -> Dict[str, Any]:
        data = body.get(key, {})
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise AdminAPIError(f"'{key}' must be a JSON object")
        return data

    def _mark_dirty(self):
        self.state.dirty = True

    def _edge_row(self, e_tuple: Tuple) -> Dict[str, Any]:
        data = self.hypergraph_db.e(e_tuple, {})
        return {
            "vertices": _json_safe(list(e_tuple)),
            "size": len(e_tuple),
            "preview": _preview(data),
        }

    @staticmethod
    def _paginate(rows: List[Any], params: Dict[str, str]) -> Dict[str, Any]:
        try:
            page = max(1, int(params.get("page", 1)))
            page_size = min(500, max(1, int(params.get("page_size", 20))))
        except ValueError:
            raise AdminAPIError("page and page_size must be integers")
        total = len(rows)
        start = (page - 1) * page_size
        return {
            "data": rows[start : start + page_size],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": max(1, (total + page_size - 1) // page_size),
            },
        }

    # ------------------------------------------------------------------ read endpoints

    def _info(self) -> Dict[str, Any]:
        hg = self.hypergraph_db
        storage = Path(hg.storage_file)
        return {
            "storage_file": str(storage.resolve()),
            "file_exists": storage.exists(),
            "file_size": storage.stat().st_size if storage.exists() else None,
            "num_v": hg.num_v,
            "num_e": hg.num_e,
            "dirty": self.state.dirty,
            "last_saved": self.state.last_saved,
        }

    def _stats(self) -> Dict[str, Any]:
        hg = self.hypergraph_db
        degrees = [hg.degree_v(v) for v in hg.all_v]
        sizes = [len(e) for e in hg.all_e]
        v_keys: Counter = Counter()
        e_keys: Counter = Counter()
        types: Counter = Counter()
        for v in hg.all_v:
            data = hg.v(v, {}) or {}
            v_keys.update(data.keys())
            if data.get("entity_type"):
                types[str(data["entity_type"])] += 1
        for e in hg.all_e:
            e_keys.update((hg.e(e, {}) or {}).keys())

        top = sorted(hg.all_v, key=lambda v: hg.degree_v(v), reverse=True)[:10]
        return {
            "num_v": hg.num_v,
            "num_e": hg.num_e,
            "isolated_v": sum(1 for d in degrees if d == 0),
            "avg_degree": round(sum(degrees) / len(degrees), 3) if degrees else 0,
            "max_degree": max(degrees, default=0),
            "avg_edge_size": round(sum(sizes) / len(sizes), 3) if sizes else 0,
            "max_edge_size": max(sizes, default=0),
            "degree_hist": sorted(Counter(degrees).items()),
            "edge_size_hist": sorted(Counter(sizes).items()),
            "entity_types": types.most_common(12),
            "vertex_keys": v_keys.most_common(20),
            "edge_keys": e_keys.most_common(20),
            "top_vertices": [{"id": _json_safe(v), "degree": hg.degree_v(v)} for v in top],
        }

    def _list_vertices(self, params: Dict[str, str]) -> Dict[str, Any]:
        hg = self.hypergraph_db
        search = params.get("search", "").strip().lower()
        entity_type = params.get("entity_type", "")
        sort_by = params.get("sort_by", "degree")
        desc = params.get("sort_order", "desc") == "desc"

        rows = []
        for v_id in hg.all_v:
            data = hg.v(v_id, {}) or {}
            if entity_type and str(data.get("entity_type", "")) != entity_type:
                continue
            id_match = bool(search) and search in str(v_id).lower()
            if search and not id_match and search not in _preview(data, 10**9).lower():
                continue
            rows.append(
                {
                    "id": _json_safe(v_id),
                    "degree": hg.degree_v(v_id),
                    "entity_type": str(data.get("entity_type", "")),
                    "preview": _preview(data),
                    "_id_match": id_match,
                }
            )
        if sort_by == "id":
            rows.sort(key=lambda r: str(r["id"]), reverse=desc)
        else:
            rows.sort(key=lambda r: (r["degree"], str(r["id"])), reverse=desc)
        # Stable sort: when searching, vertices whose id matches come before attribute-only matches
        rows.sort(key=lambda r: not r.pop("_id_match"))
        return self._paginate(rows, params)

    def _list_edges(self, params: Dict[str, str]) -> Dict[str, Any]:
        hg = self.hypergraph_db
        search = params.get("search", "").strip().lower()
        vertex = params.get("vertex")
        sort_by = params.get("sort_by", "size")
        desc = params.get("sort_order", "desc") == "desc"

        edges = hg.all_e
        if vertex:
            edges = hg.nbr_e_of_v(self._resolve_v(json.loads(vertex)))
        rows = []
        for e in edges:
            if search:
                haystack = " ".join(str(v) for v in e) + " " + _preview(hg.e(e, {}), 10**9)
                if search not in haystack.lower():
                    continue
            rows.append(self._edge_row(e))
        if sort_by == "vertices":
            rows.sort(key=lambda r: str(r["vertices"]), reverse=desc)
        else:
            rows.sort(key=lambda r: (r["size"], str(r["vertices"])), reverse=desc)
        return self._paginate(rows, params)

    def _get_vertex(self, body: Dict[str, Any]) -> Dict[str, Any]:
        hg = self.hypergraph_db
        v_id = self._resolve_v(body.get("id"))
        edges = sorted(hg.nbr_e_of_v(v_id), key=lambda e: (-len(e), str(e)))
        return {
            "id": _json_safe(v_id),
            "data": _json_safe(hg.v(v_id, {})),
            "degree": hg.degree_v(v_id),
            "neighbors": len(hg.nbr_v(v_id, exclude_self=False) - {v_id}),  # nbr_v() raises on isolated vertices
            "edges": [self._edge_row(e) for e in edges[:200]],
            "edges_truncated": len(edges) > 200,
        }

    def _get_edge(self, body: Dict[str, Any]) -> Dict[str, Any]:
        hg = self.hypergraph_db
        e_tuple = self._resolve_e(body.get("vertices"))
        if not hg.has_e(e_tuple):
            raise AdminAPIError("Hyperedge does not exist", 404)
        return {
            "vertices": [{"id": _json_safe(v), "degree": hg.degree_v(v)} for v in e_tuple],
            "data": _json_safe(hg.e(e_tuple, {})),
        }

    # ------------------------------------------------------------------ write endpoints

    def _upsert_vertex(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Create (``create: true``) or update a vertex.

        ``replace: true`` overwrites the attribute dict instead of merging into it,
        which is how the editor removes attributes.
        """
        hg = self.hypergraph_db
        data = self._require_dict(body, "data")
        if body.get("create"):
            v_id = body.get("id")
            if not isinstance(v_id, (str, int, float)) or isinstance(v_id, bool) or v_id == "":
                raise AdminAPIError("Vertex id must be a non-empty string or a number")
            if hg.has_v(v_id):
                raise AdminAPIError(f"Vertex {v_id!r} already exists", 409)
            hg.add_v(v_id, data)
        else:
            v_id = self._resolve_v(body.get("id"))
            if body.get("replace"):
                hg.v(v_id).clear()
            hg.update_v(v_id, data)
        self._mark_dirty()
        return self._get_vertex({"id": _json_safe(v_id)})

    def _delete_vertex(self, body: Dict[str, Any]) -> Dict[str, Any]:
        self.hypergraph_db.remove_v(self._resolve_v(body.get("id")))
        self._mark_dirty()
        return {"ok": True}

    def _upsert_edge(self, body: Dict[str, Any]) -> Dict[str, Any]:
        hg = self.hypergraph_db
        data = self._require_dict(body, "data")
        e_tuple = self._resolve_e(body.get("vertices"))
        exists = hg.has_e(e_tuple)
        if body.get("create"):
            if exists:
                raise AdminAPIError("Hyperedge already exists", 409)
            hg.add_e(e_tuple, data)
        else:
            if not exists:
                raise AdminAPIError("Hyperedge does not exist", 404)
            if body.get("replace"):
                hg.e(e_tuple).clear()
            hg.update_e(e_tuple, data)
        self._mark_dirty()
        return self._get_edge({"vertices": _json_safe(list(e_tuple))})

    def _delete_edge(self, body: Dict[str, Any]) -> Dict[str, Any]:
        hg = self.hypergraph_db
        e_tuple = self._resolve_e(body.get("vertices"))
        if not hg.has_e(e_tuple):
            raise AdminAPIError("Hyperedge does not exist", 404)
        hg.remove_e(e_tuple)
        self._mark_dirty()
        return {"ok": True}

    def _save(self, body: Dict[str, Any]) -> Dict[str, Any]:
        hg = self.hypergraph_db
        if not hg.save(hg.storage_file):
            raise AdminAPIError(f"Failed to save to {hg.storage_file}", 500)
        self.state.dirty = False
        self.state.last_saved = time.time()
        return self._info()

    def _import_hif(self, body: Dict[str, Any]) -> Dict[str, Any]:
        if "incidences" not in body:
            raise AdminAPIError("Invalid HIF data: missing 'incidences'")
        if not self.hypergraph_db.from_hif(body):
            raise AdminAPIError("Failed to import HIF data")
        self._mark_dirty()
        return self._info()


class _AdminTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class HypergraphAdmin:
    """Management console server for a hypergraph database."""

    def __init__(self, hypergraph_db: BaseHypergraphDB, host: str = "127.0.0.1", port: int = 8900):
        self.hypergraph_db = hypergraph_db
        self.host = host
        self.port = port
        self.state = AdminState(hypergraph_db)
        self.httpd: Optional[socketserver.TCPServer] = None

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def start_server(self, open_browser: bool = True) -> threading.Thread:
        def handler(*args, **kwargs):
            return HypergraphAdminHandler(self.state, *args, **kwargs)

        # Requests are served one at a time on purpose: HypergraphDB is not thread-safe.
        self.httpd = _AdminTCPServer((self.host, self.port), handler)
        self.port = self.httpd.server_address[1]
        thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        thread.start()

        print(f"🛠  Hypergraph DB admin started: {self.url}")
        if open_browser:
            webbrowser.open(self.url)
        return thread

    def stop_server(self):
        if self.httpd is not None:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None


def run_admin(
    hypergraph_db: BaseHypergraphDB,
    host: str = "127.0.0.1",
    port: int = 8900,
    open_browser: bool = True,
    blocking: bool = True,
) -> HypergraphAdmin:
    """Start the admin console for ``hypergraph_db``.

    Args:
        hypergraph_db: HypergraphDB instance to manage
        host: Interface to bind; keep the default unless you trust your network,
            the console has no authentication
        port: Server port (0 picks a free port)
        open_browser: Whether to open the console in a browser
        blocking: Whether to block until Ctrl+C. If False, returns immediately.

    Returns:
        HypergraphAdmin instance
    """
    admin = HypergraphAdmin(hypergraph_db, host=host, port=port)
    thread = admin.start_server(open_browser=open_browser)
    if not blocking:
        return admin

    print("⌨️  Press Ctrl+C to stop server")
    try:
        while thread.is_alive():
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    if admin.state.dirty:
        print("⚠️  Unsaved changes were discarded (use the Save button to persist them)")
    print("\n🛑 Server stopped")
    admin.stop_server()
    return admin
