import pickle as pkl
from pathlib import Path
from copy import deepcopy
from collections import defaultdict
from collections.abc import Hashable
from functools import cached_property
from dataclasses import dataclass, field
from typing import Tuple, List, Any, Union, Set, Dict, Optional


from hyperdb.base import BaseHypergraphDB


@dataclass
class HypergraphDB(BaseHypergraphDB):
    r"""
    Hypergraph database.
    """

    _v_data: Dict[str, Any] = field(default_factory=dict)
    _e_data: Dict[Tuple, Any] = field(default_factory=dict)
    _v_inci: Dict[str, Set[Tuple]] = field(default_factory=lambda: defaultdict(set))

    def __post_init__(self):
        assert isinstance(self.storage_file, (str, Path))
        if isinstance(self.storage_file, str):
            self.storage_file = Path(self.storage_file)
        if self.storage_file.exists():
            self.load(self.storage_file)

    def load(self, storage_file: Path) -> dict:
        r"""
        Load the hypergraph database from the storage file.
        """
        try:
            with open(storage_file, "rb") as f:
                data = pkl.load(f)
            self._v_data = data.get("v_data", {})
            self._v_inci = data.get("v_inci", {})
            self._e_data = data.get("e_data", {})
            return True
        except Exception as e:
            return False

    def save(self, storage_file: Path) -> dict:
        r"""
        Save the hypergraph database to the storage file.
        """
        data = {
            "v_data": self._v_data,
            "v_inci": self._v_inci,
            "e_data": self._e_data,
        }
        try:
            with open(storage_file, "wb") as f:
                pkl.dump(data, f)
            return True
        except Exception as e:
            return False

    def _clear_cache(self):
        r"""
        Clear the cached properties.
        """
        self.__dict__.pop("all_v", None)
        self.__dict__.pop("all_e", None)
        self.__dict__.pop("num_v", None)
        self.__dict__.pop("num_e", None)

    def v(self, v_id: str, default: Any = None) -> dict:
        r"""
        Return the vertex data.

        Args:
            ``v_id`` (``str``): The vertex id.
            ``default`` (``Any``): The default value if the vertex does not exist.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        try:
            return self._v_data[v_id]
        except KeyError:
            return default

    def e(self, e_tuple: Union[List, Set, Tuple], default: Any = None) -> dict:
        r"""
        Return the hyperedge data.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
            ``default`` (``Any``): The default value if the hyperedge does not exist.
        """
        assert isinstance(
            e_tuple, (set, list, tuple)
        ), "The hyperedge must be a set, list, or tuple of vertex ids."
        e_tuple = self.encode_e(e_tuple)
        try:
            return self._e_data[e_tuple]
        except KeyError:
            return default

    def encode_e(self, e_tuple: Union[List, Set, Tuple]) -> Tuple:
        r"""
        Sort and check the hyperedge tuple.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        assert isinstance(
            e_tuple, (list, set, tuple)
        ), "The hyperedge must be a list, set, or tuple of vertex ids."
        tmp = sorted(list(set(e_tuple)))
        for v_id in tmp:
            assert isinstance(v_id, Hashable), "The vertex id must be hashable."
            assert (
                v_id in self.all_v
            ), f"The vertex {v_id} does not exist in the hypergraph."
        return tuple(tmp)

    @cached_property
    def all_v(self) -> List[str]:
        r"""
        Return a list of all vertices in the hypergraph.
        """
        return set(self._v_data.keys())

    @cached_property
    def all_e(self) -> List[Tuple]:
        r"""
        Return a list of all hyperedges in the hypergraph.
        """
        return set(self._e_data.keys())
    
    @cached_property
    def num_v(self) -> int:
        r"""
        Return the number of vertices in the hypergraph.
        """
        return len(self._v_data)
    
    @cached_property
    def num_e(self) -> int:
        r"""
        Return the number of hyperedges in the hypergraph.
        """
        return len(self._e_data)

    def add_v(self, v_id: Any, v_data: Optional[Dict] = None):
        r"""
        Add a vertex to the hypergraph.

        Args:
            ``v_id`` (``Any``): The vertex id.
            ``v_data`` (``dict``, optional): The vertex data.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        if v_data is not None:
            assert isinstance(v_data, dict), "The vertex data must be a dictionary."
        else:
            v_data = {}
        if v_id not in self.all_v:
            self._v_data[v_id] = v_data
            self._v_inci[v_id] = set()
        else:
            self._v_data[v_id].update(v_data)
        self._clear_cache()

    def add_e(self, e_tuple: Union[List, Set, Tuple], e_data: Optional[Dict] = None):
        r"""
        Add a hyperedge to the hypergraph.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
            ``e_data`` (``dict``, optional): The hyperedge data.
        """
        assert isinstance(
            e_tuple, (list, set, tuple)
        ), "The hyperedge must be a list, set, or tuple of vertex ids."
        if e_data is not None:
            assert isinstance(e_data, dict), "The hyperedge data must be a dictionary."
        else:
            e_data = {}
        e_tuple = self.encode_e(e_tuple)
        if e_tuple not in self.all_e:
            self._e_data[e_tuple] = e_data
            for v in e_tuple:
                self._v_inci[v].add(e_tuple)
        else:
            self._e_data[e_tuple].update(e_data)
        self._clear_cache()

    def remove_v(self, v_id: Any):
        r"""
        Remove a vertex from the hypergraph.

        Args:
            ``v_id`` (``Any``): The vertex id.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        assert (
            v_id in self.all_v
        ), f"The vertex {v_id} does not exist in the hypergraph."
        del self._v_data[v_id]
        for e_tuple in self._v_inci[v_id]:
            new_e_tuple = self.encode_e(set(e_tuple) - {v_id})
            if len(new_e_tuple) >= 2:
                self._e_data[new_e_tuple] = deepcopy(self._e_data[e_tuple])
            del self._e_data[e_tuple]
        del self._v_inci[v_id]
        self._clear_cache()

    def remove_e(self, e_tuple: Union[List, Set, Tuple]):
        r"""
        Remove a hyperedge from the hypergraph.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        assert isinstance(
            e_tuple, (list, set, tuple)
        ), "The hyperedge must be a list, set, or tuple of vertex ids."
        e_tuple = self.encode_e(e_tuple)
        assert (
            e_tuple in self.all_e
        ), f"The hyperedge {e_tuple} does not exist in the hypergraph."
        for v in e_tuple:
            self._v_inci[v].remove(e_tuple)
        del self._e_data[e_tuple]
        self._clear_cache()

    def update_v(self, v_id: Any, v_data: dict):
        r"""
        Update the vertex data.

        Args:
            ``v_id`` (``Any``): The vertex id.
            ``v_data`` (``dict``): The vertex data.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        assert isinstance(v_data, dict), "The vertex data must be a dictionary."
        assert (
            v_id in self.all_v
        ), f"The vertex {v_id} does not exist in the hypergraph."
        self._v_data[v_id].update(v_data)
        self._clear_cache()

    def update_e(self, e_tuple: Union[List, Set, Tuple], e_data: dict):
        r"""
        Update the hyperedge data.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
            ``e_data`` (``dict``): The hyperedge data.
        """
        assert isinstance(
            e_tuple, (list, set, tuple)
        ), "The hyperedge must be a list, set, or tuple of vertex ids."
        assert isinstance(e_data, dict), "The hyperedge data must be a dictionary."
        e_tuple = self.encode_e(e_tuple)
        assert (
            e_tuple in self.all_e
        ), f"The hyperedge {e_tuple} does not exist in the hypergraph."
        self._e_data[e_tuple].update(e_data)
        self._clear_cache()

    def has_v(self, v_id: Any) -> bool:
        r"""
        Check if the vertex exists.

        Args:
            ``v_id`` (``Any``): The vertex id.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        return v_id in self.all_v

    def has_e(self, e_tuple: Union[List, Set, Tuple]) -> bool:
        r"""
        Check if the hyperedge exists.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        assert isinstance(
            e_tuple, (list, set, tuple)
        ), "The hyperedge must be a list, set, or tuple of vertex ids."
        try:
            e_tuple = self.encode_e(e_tuple)
        except AssertionError:
            return False
        return e_tuple in self.all_e

    def degree_v(self, v_id: Any) -> int:
        r"""
        Return the degree of the vertex.

        Args:
            ``v_id`` (``Any``): The vertex id.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        assert (
            v_id in self.all_v
        ), f"The vertex {v_id} does not exist in the hypergraph."
        return len(self._v_inci[v_id])

    def degree_e(self, e_tuple: Union[List, Set, Tuple]) -> int:
        r"""
        Return the degree of the hyperedge.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        assert isinstance(
            e_tuple, (list, set, tuple)
        ), "The hyperedge must be a list, set, or tuple of vertex ids."
        e_tuple = self.encode_e(e_tuple)
        assert (
            e_tuple in self.all_e
        ), f"The hyperedge {e_tuple} does not exist in the hypergraph."
        return len(e_tuple)

    def nbr_e_of_v(self, v_id: Any) -> list:
        r"""
        Return the incident hyperedges of the vertex.

        Args:
            ``v_id`` (``Any``): The vertex id.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        assert (
            v_id in self.all_v
        ), f"The vertex {v_id} does not exist in the hypergraph."
        return set(self._v_inci[v_id])

    def nbr_v_of_e(self, e_tuple: Union[List, Set, Tuple]) -> list:
        r"""
        Return the incident vertices of the hyperedge.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        assert isinstance(
            e_tuple, (list, set, tuple)
        ), "The hyperedge must be a list, set, or tuple of vertex ids."
        e_tuple = self.encode_e(e_tuple)
        assert (
            e_tuple in self.all_e
        ), f"The hyperedge {e_tuple} does not exist in the hypergraph."
        return set(e_tuple)

    def nbr_v(self, v_id: Any, exclude_self=True) -> list:
        r"""
        Return the neighbors of the vertex.

        Args:
            ``v_id`` (``Any``): The vertex id.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        assert (
            v_id in self.all_v
        ), f"The vertex {v_id} does not exist in the hypergraph."
        nbrs = set()
        for e_tuple in self._v_inci[v_id]:
            nbrs.update(e_tuple)
        if exclude_self:
            nbrs.remove(v_id)
        return set(nbrs)
