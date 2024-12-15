import pytest
from hyperdb import HypergraphDB


@pytest.fixture()
def hg1():
    hg = HypergraphDB()
    hg.add_v(1, {"name": "Alice"})
    hg.add_v(2, {"name": "Bob"})
    hg.add_v(3, {"name": "Charlie"})
    hg.add_v(4, {"name": "David"})
    hg.add_v(5, {"name": "Eve"})
    hg.add_v(6, {"name": "Frank"})
    hg.add_e((1, 2), {"relation": "knows"})
    hg.add_e((1, 3), {"relation": "knows"})
    hg.add_e((2, 3, 4), {"relation": "knows"})
    hg.add_e((3, 4, 1, 5), {"relation": "study"})
    hg.add_e((4, 5, 6), {"relation": "study"})
    hg.add_e((5, 6, 1), {"relation": "study"})
    return hg


def test_add_v(hg1):
    hg1.add_v(7, {"name": "Grace"})
    assert hg1.has_v(7) == True


def test_add_e(hg1):
    hg1.add_e((6, 1), {"relation": "knows"})
    assert hg1.has_e((6, 1)) == True

    # test add_e with a vertex not in the hypergraph raises an error
    with pytest.raises(AssertionError):
        hg1.add_e((6, 7), {"relation": "knows"})


def test_has_v(hg1):
    assert hg1.has_v(1) == True
    assert hg1.has_v(7) == False


def test_has_e(hg1):
    assert hg1.has_e((1, 2)) == True
    assert hg1.has_e((6, 1)) == False
    assert hg1.has_e((1, 7)) == False
