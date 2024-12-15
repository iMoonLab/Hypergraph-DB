import pytest
from hyperdb import HypergraphDB


@pytest.fixture()
def hg():
    bd = HypergraphDB()
    bd.add_v(1, {"name": "Alice"})
    bd.add_v(2, {"name": "Bob"})
    bd.add_v(3, {"name": "Charlie"})
    bd.add_v(4, {"name": "David"})
    bd.add_v(5, {"name": "Eve"})
    bd.add_v(6, {"name": "Frank"})
    bd.add_e((1, 2), {"relation": "knows"})
    bd.add_e((1, 3), {"relation": "knows"})
    bd.add_e((2, 3, 4), {"relation": "knows"})
    bd.add_e((3, 4, 1, 5), {"relation": "study"})
    bd.add_e((6, 5, 4), {"relation": "study"})
    bd.add_e((1, 5, 6), {"relation": "study"})
    return bd


def test_all_v(hg):
    assert hg.all_v == set([1, 2, 3, 4, 5, 6])
    assert hg.num_v == 6
    hg.remove_v(2)
    assert hg.all_v == set([1, 3, 4, 5, 6])
    assert hg.num_v == 5


def test_all_e(hg):
    assert hg.all_e == set(
        [(1, 2), (1, 3), (2, 3, 4), (1, 3, 4, 5), (4, 5, 6), (1, 5, 6)]
    )
    assert hg.num_e == 6
    hg.remove_v(2)
    assert hg.all_e == set([(1, 3), (3, 4), (1, 3, 4, 5), (4, 5, 6), (1, 5, 6)])
    assert hg.num_e == 5


def test_v(hg):
    assert hg.v(1) == {"name": "Alice"}
    assert hg.v(2) == {"name": "Bob"}
    assert hg.v(3) == {"name": "Charlie"}
    assert hg.v(4) == {"name": "David"}
    assert hg.v(5) == {"name": "Eve"}
    assert hg.v(6) == {"name": "Frank"}
    assert hg.v(7) == None


def test_e(hg):
    assert hg.e((1, 2)) == {"relation": "knows"}
    assert hg.e((1, 3)) == {"relation": "knows"}
    assert hg.e((2, 3, 4)) == {"relation": "knows"}
    assert hg.e((3, 4, 1, 5)) == {"relation": "study"}
    assert hg.e((4, 5, 6)) == {"relation": "study"}
    assert hg.e((1, 5, 6)) == {"relation": "study"}
    assert hg.e((6, 1)) == None
    with pytest.raises(AssertionError):
        hg.e((1, 7))


def test_add_v(hg):
    hg.add_v(7, {"name": "Grace"})
    assert hg.has_v(7) == True
    assert hg.v(7) == {"name": "Grace"}
    hg.add_v(8)
    assert hg.has_v(8) == True
    assert hg.v(8) == {}


def test_add_e(hg):
    hg.add_e((6, 1), {"relation": "knows"})
    assert hg.has_e((6, 1)) == True
    assert hg.e((6, 1)) == {"relation": "knows"}

    # test add_e with a vertex not in the hypergraph raises an error
    with pytest.raises(AssertionError):
        hg.add_e((6, 7), {"relation": "knows"})


def test_remove_v(hg):
    hg.has_v(6) == True
    hg.has_e((1, 5, 6)) == True
    hg.e((1, 5, 6)) == {"relation": "study"}
    hg.remove_v(6)
    hg.has_v(6) == False
    hg.has_e((1, 5, 6)) == False
    hg.has_e((5, 1)) == {"relation": "study"}


def test_remove_e(hg):
    hg.has_e((1, 2)) == True
    hg.remove_e((1, 2))
    hg.has_e((1, 2)) == False
    with pytest.raises(AssertionError):
        hg.remove_e((1, 7))
    with pytest.raises(AssertionError):
        hg.remove_e((7, 1))


def test_has_v(hg):
    assert hg.has_v(1) == True
    assert hg.has_v(7) == False


def test_has_e(hg):
    assert hg.has_e((1, 2)) == True
    assert hg.has_e((6, 1)) == False
    assert hg.has_e((1, 7)) == False


def test_update_v(hg):
    assert hg.v(1) == {"name": "Alice"}
    hg.update_v(1, {"name": "Alice Smith"})
    assert hg.v(1) == {"name": "Alice Smith"}
    with pytest.raises(AssertionError):
        hg.update_v(7, {"name": "Grace"})


def test_update_e(hg):
    assert hg.e((1, 2)) == {"relation": "knows"}
    hg.update_e((1, 2), {"relation": "friends"})
    assert hg.e((1, 2)) == {"relation": "friends"}
    with pytest.raises(AssertionError):
        hg.update_e((1, 7), {"relation": "knows"})


def test_degree_v(hg):
    assert hg.degree_v(1) == 4
    assert hg.degree_v(2) == 2
    assert hg.degree_v(4) == 3
    hg.add_e((1, 4), {"relation": "friends"})
    assert hg.degree_v(1) == 5
    assert hg.degree_v(2) == 2
    assert hg.degree_v(4) == 4
    hg.remove_e((2, 3, 4))
    assert hg.degree_v(1) == 5
    assert hg.degree_v(2) == 1
    assert hg.degree_v(4) == 3


def test_degree_e(hg):
    assert hg.degree_e((1, 2)) == 2
    assert hg.degree_e((1, 3)) == 2
    assert hg.degree_e((2, 3, 4)) == 3
    assert hg.degree_e((3, 4, 1, 5)) == 4
    assert hg.degree_e((4, 5, 6)) == 3
    assert hg.degree_e((1, 5, 6)) == 3
    hg.add_e((1, 4), {"relation": "friends"})
    assert hg.degree_e((1, 2)) == 2
    hg.remove_e((1, 2))
    with pytest.raises(AssertionError):
        hg.degree_e((1, 2))
    with pytest.raises(AssertionError):
        hg.degree_e((1, 7))


def test_nbr_e_of_v(hg):
    assert hg.nbr_e_of_v(1) == set([(1, 2), (1, 3), (1, 3, 4, 5), (1, 5, 6)])
    assert hg.nbr_e_of_v(2) == set([(1, 2), (2, 3, 4)])
    assert hg.nbr_e_of_v(3) == set([(1, 3), (2, 3, 4), (1, 3, 4, 5)])
    assert hg.nbr_e_of_v(4) == set([(2, 3, 4), (1, 3, 4, 5), (4, 5, 6)])
    assert hg.nbr_e_of_v(5) == set([(1, 3, 4, 5), (4, 5, 6), (1, 5, 6)])
    assert hg.nbr_e_of_v(6) == set([(4, 5, 6), (1, 5, 6)])
    hg.add_e((1, 4), {"relation": "friends"})
    assert hg.nbr_e_of_v(1) == set([(1, 2), (1, 3), (1, 4), (1, 3, 4, 5), (1, 5, 6)])
    assert hg.nbr_e_of_v(4) == set([(1, 4), (2, 3, 4), (1, 3, 4, 5), (4, 5, 6)])
    hg.remove_e((1, 2))
    assert hg.nbr_e_of_v(1) == set([(1, 3), (1, 4), (1, 3, 4, 5), (1, 5, 6)])
    assert hg.nbr_e_of_v(2) == set([(2, 3, 4)])
    with pytest.raises(AssertionError):
        hg.nbr_e_of_v(7)


def test_nbr_v_of_e(hg):
    assert hg.nbr_v_of_e((1, 2)) == set([1, 2])
    assert hg.nbr_v_of_e((1, 3)) == set([1, 3])
    assert hg.nbr_v_of_e((2, 3, 4)) == set([2, 3, 4])
    assert hg.nbr_v_of_e((3, 4, 1, 5)) == set([3, 4, 1, 5])
    assert hg.nbr_v_of_e((4, 5, 6)) == set([4, 5, 6])
    assert hg.nbr_v_of_e((1, 5, 6)) == set([1, 5, 6])
    hg.add_e((1, 4), {"relation": "friends"})
    assert hg.nbr_v_of_e((1, 4)) == set([1, 4])
    assert hg.nbr_v_of_e((1, 3, 4, 5)) == set([1, 3, 4, 5])
    hg.remove_e((1, 2))
    with pytest.raises(AssertionError):
        assert hg.nbr_v_of_e((1, 2)) == set([1])
    with pytest.raises(AssertionError):
        hg.nbr_v_of_e((1, 7))


def test_nbr_v(hg):
    assert hg.nbr_v(1) == set([2, 3, 4, 5, 6])
    assert hg.nbr_v(2) == set([1, 3, 4])
    assert hg.nbr_v(3) == set([1, 2, 4, 5])
    assert hg.nbr_v(4) == set([1, 2, 3, 5, 6])
    assert hg.nbr_v(5) == set([1, 3, 4, 6])
    assert hg.nbr_v(6) == set([1, 4, 5])
    hg.add_e((1, 4), {"relation": "friends"})
    assert hg.nbr_v(1) == set([2, 3, 4, 5, 6])
    assert hg.nbr_v(4) == set([1, 2, 3, 5, 6])
    hg.remove_e((1, 2))
    assert hg.nbr_v(1) == set([3, 4, 5, 6])
    assert hg.nbr_v(2) == set([3, 4])
    with pytest.raises(AssertionError):
        hg.nbr_v(7)
    assert hg.nbr_v(1, exclude_self=False) == set([1, 3, 4, 5, 6])


def test_save_and_load(hg, tmpdir):
    file_path = str(tmpdir.join("my_hypergraph.hgdb"))
    hg.save(file_path)
    hg2 = HypergraphDB(storage_file=file_path)
    assert hg.all_v == hg2.all_v
    assert hg.all_e == hg2.all_e
    assert hg.num_v == hg2.num_v
    assert hg.num_e == hg2.num_e
    assert hg.v(1) == hg2.v(1)
    assert hg.v(2) == hg2.v(2)
    assert hg.v(3) == hg2.v(3)
    assert hg.v(4) == hg2.v(4)
    assert hg.v(5) == hg2.v(5)
    assert hg.v(6) == hg2.v(6)
    assert hg.e((1, 2)) == hg2.e((1, 2))
    assert hg.e((1, 3)) == hg2.e((1, 3))
    assert hg.e((2, 3, 4)) == hg2.e((2, 3, 4))
    assert hg.e((3, 4, 1, 5)) == hg2.e((3, 4, 1, 5))
    assert hg.e((4, 5, 6)) == hg2.e((4, 5, 6))
    assert hg.e((1, 5, 6)) == hg2.e((1, 5, 6))
    hg2.remove_v(2)
    assert hg2.has_v(2) == False
    hg3 = HypergraphDB()
    hg3.load(file_path)
    assert hg == hg3
