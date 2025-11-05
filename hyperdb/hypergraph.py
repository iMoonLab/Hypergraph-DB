import json
import pickle as pkl
from collections import defaultdict
from collections.abc import Hashable
from copy import deepcopy
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from hyperdb.base import BaseHypergraphDB


@dataclass
class HypergraphDB(BaseHypergraphDB):
    r"""
    Hypergraph database.
    """

    _v_data: Dict[Any, Any] = field(default_factory=dict)
    _e_data: Dict[Tuple, Any] = field(default_factory=dict)
    _v_inci: Dict[Any, Set[Tuple]] = field(default_factory=lambda: defaultdict(set))

    def __post_init__(self):
        assert isinstance(self.storage_file, (str, Path))
        if isinstance(self.storage_file, str):
            self.storage_file = Path(self.storage_file)
        if self.storage_file.exists():
            self.load(self.storage_file)

    def load(self, storage_file: Union[str, Path]) -> bool:
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
        except Exception:
            return False

    def save(self, storage_file: Union[str, Path]) -> bool:
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
        except Exception:
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
        assert isinstance(e_tuple, (set, list, tuple)), "The hyperedge must be a set, list, or tuple of vertex ids."
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
        assert isinstance(e_tuple, (list, set, tuple)), "The hyperedge must be a list, set, or tuple of vertex ids."
        tmp = sorted(list(set(e_tuple)))
        for v_id in tmp:
            assert isinstance(v_id, Hashable), "The vertex id must be hashable."
            assert v_id in self._v_data, f"The vertex {v_id} does not exist in the hypergraph."
        return tuple(tmp)

    @cached_property
    def all_v(self) -> Set[Any]:
        r"""
        Return a set of all vertices in the hypergraph.
        """
        return set(self._v_data.keys())

    @cached_property
    def all_e(self) -> Set[Tuple]:
        r"""
        Return a set of all hyperedges in the hypergraph.
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
        if v_id not in self._v_data:
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
        assert isinstance(e_tuple, (list, set, tuple)), "The hyperedge must be a list, set, or tuple of vertex ids."
        if e_data is not None:
            assert isinstance(e_data, dict), "The hyperedge data must be a dictionary."
        else:
            e_data = {}
        e_tuple = self.encode_e(e_tuple)
        if e_tuple not in self._e_data:
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
        assert v_id in self._v_data, f"The vertex {v_id} does not exist in the hypergraph."
        del self._v_data[v_id]
        old_e_tuples, new_e_tuples = [], []
        for e_tuple in self._v_inci[v_id]:
            new_e_tuple = self.encode_e(set(e_tuple) - {v_id})
            if len(new_e_tuple) >= 2:
                # todo: maybe new e tuple existing in hg, need to merge to hyperedge information
                self._e_data[new_e_tuple] = deepcopy(self._e_data[e_tuple])
            del self._e_data[e_tuple]
            old_e_tuples.append(e_tuple)
            new_e_tuples.append(new_e_tuple)
        del self._v_inci[v_id]
        for old_e_tuple, new_e_tuple in zip(old_e_tuples, new_e_tuples):
            for _v_id in old_e_tuple:
                if _v_id != v_id:
                    self._v_inci[_v_id].remove(old_e_tuple)
                    if len(new_e_tuple) >= 2:
                        self._v_inci[_v_id].add(new_e_tuple)
        self._clear_cache()

    def remove_e(self, e_tuple: Union[List, Set, Tuple]):
        r"""
        Remove a hyperedge from the hypergraph.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        assert isinstance(e_tuple, (list, set, tuple)), "The hyperedge must be a list, set, or tuple of vertex ids."
        e_tuple = self.encode_e(e_tuple)
        assert e_tuple in self._e_data, f"The hyperedge {e_tuple} does not exist in the hypergraph."
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
        assert v_id in self._v_data, f"The vertex {v_id} does not exist in the hypergraph."
        self._v_data[v_id].update(v_data)
        self._clear_cache()

    def update_e(self, e_tuple: Union[List, Set, Tuple], e_data: dict):
        r"""
        Update the hyperedge data.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
            ``e_data`` (``dict``): The hyperedge data.
        """
        assert isinstance(e_tuple, (list, set, tuple)), "The hyperedge must be a list, set, or tuple of vertex ids."
        assert isinstance(e_data, dict), "The hyperedge data must be a dictionary."
        e_tuple = self.encode_e(e_tuple)
        assert e_tuple in self._e_data, f"The hyperedge {e_tuple} does not exist in the hypergraph."
        self._e_data[e_tuple].update(e_data)
        self._clear_cache()

    def has_v(self, v_id: Any) -> bool:
        r"""
        Check if the vertex exists.

        Args:
            ``v_id`` (``Any``): The vertex id.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        return v_id in self._v_data

    def has_e(self, e_tuple: Union[List, Set, Tuple]) -> bool:
        r"""
        Check if the hyperedge exists.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        assert isinstance(e_tuple, (list, set, tuple)), "The hyperedge must be a list, set, or tuple of vertex ids."
        try:
            e_tuple = self.encode_e(e_tuple)
        except AssertionError:
            return False
        return e_tuple in self._e_data

    def degree_v(self, v_id: Any) -> int:
        r"""
        Return the degree of the vertex.

        Args:
            ``v_id`` (``Any``): The vertex id.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        assert v_id in self._v_data, f"The vertex {v_id} does not exist in the hypergraph."
        return len(self._v_inci[v_id])

    def degree_e(self, e_tuple: Union[List, Set, Tuple]) -> int:
        r"""
        Return the degree of the hyperedge.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        assert isinstance(e_tuple, (list, set, tuple)), "The hyperedge must be a list, set, or tuple of vertex ids."
        e_tuple = self.encode_e(e_tuple)
        assert e_tuple in self._e_data, f"The hyperedge {e_tuple} does not exist in the hypergraph."
        return len(e_tuple)

    def nbr_e_of_v(self, v_id: Any) -> set:
        r"""
        Return the incident hyperedges of the vertex.

        Args:
            ``v_id`` (``Any``): The vertex id.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        assert v_id in self._v_data, f"The vertex {v_id} does not exist in the hypergraph."
        return set(self._v_inci[v_id])

    def nbr_v_of_e(self, e_tuple: Union[List, Set, Tuple]) -> set:
        r"""
        Return the incident vertices of the hyperedge.

        Args:
            ``e_tuple`` (``Union[List, Set, Tuple]``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        assert isinstance(e_tuple, (list, set, tuple)), "The hyperedge must be a list, set, or tuple of vertex ids."
        e_tuple = self.encode_e(e_tuple)
        assert e_tuple in self._e_data, f"The hyperedge {e_tuple} does not exist in the hypergraph."
        return set(e_tuple)

    def nbr_v(self, v_id: Any, exclude_self=True) -> set:
        r"""
        Return the neighbors of the vertex.

        Args:
            ``v_id`` (``Any``): The vertex id.
        """
        assert isinstance(v_id, Hashable), "The vertex id must be hashable."
        assert v_id in self._v_data, f"The vertex {v_id} does not exist in the hypergraph."
        nbrs: set = set()
        for e_tuple in self._v_inci[v_id]:
            nbrs.update(e_tuple)
        if exclude_self:
            nbrs.remove(v_id)
        return nbrs

    def to_hif(self, file_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        r"""
        Export the hypergraph to HIF (Hypergraph Interchange Format) format.

        Args:
            ``file_path`` (``Union[str, Path]``, optional): If provided, save to file. Otherwise return dict.

        Returns:
            ``Dict[str, Any]``: HIF format dictionary.
        """
        # Build incidences array (required)
        incidences = []
        edge_to_id = {}

        # First pass: assign edge IDs
        for e_tuple in self._e_data.keys():
            e_data = self._e_data[e_tuple]
            # Check if edge has an ID/name attribute
            if "id" in e_data:
                edge_id = e_data["id"]
            elif "name" in e_data:
                edge_id = e_data["name"]
            else:
                # Create a unique edge identifier
                # Use a string representation of sorted vertices
                edge_id = "_".join(str(v) for v in sorted(e_tuple))
            edge_to_id[e_tuple] = edge_id

        # Second pass: build incidences
        for e_tuple in self._e_data.keys():
            edge_id = edge_to_id[e_tuple]
            e_data = self._e_data[e_tuple]

            # Extract attrs (all fields except weight)
            e_attrs = {k: v for k, v in e_data.items() if k != "weight"}

            for v_id in e_tuple:
                v_data = self._v_data.get(v_id, {})
                # Extract attrs for incidence (all fields except weight)
                v_attrs = {k: v for k, v in v_data.items() if k != "weight"}

                incidence = {
                    "edge": edge_id,
                    "node": v_id,
                    "attrs": v_attrs,
                }
                # Only include weight if it exists
                if "weight" in v_data:
                    incidence["weight"] = v_data["weight"]
                incidences.append(incidence)

        # Build nodes array (optional)
        nodes = []
        for v_id in self._v_data.keys():
            v_data = self._v_data[v_id]
            v_attrs = {k: v for k, v in v_data.items() if k != "weight"}

            node = {"node": v_id, "attrs": v_attrs}
            # Only include weight if it exists
            if "weight" in v_data:
                node["weight"] = v_data["weight"]
            nodes.append(node)

        # Build edges array (optional)
        edges = []
        for e_tuple in self._e_data.keys():
            e_data = self._e_data[e_tuple]
            edge_id = edge_to_id[e_tuple]
            e_attrs = {k: v for k, v in e_data.items() if k != "weight"}

            edge = {"edge": edge_id, "attrs": e_attrs}
            # Only include weight if it exists
            if "weight" in e_data:
                edge["weight"] = e_data["weight"]
            edges.append(edge)

        # Build HIF structure
        hif_data = {
            "incidences": incidences,
            "network-type": "undirected",  # Default to undirected
        }

        if nodes:
            hif_data["nodes"] = nodes
        if edges:
            hif_data["edges"] = edges

        # Save to file if path provided
        if file_path is not None:
            if isinstance(file_path, str):
                file_path = Path(file_path)
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(hif_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                raise IOError(f"Failed to save HIF file: {e}")

        return hif_data

    def save_as_hif(self, file_path: Union[str, Path]) -> bool:
        r"""
        Save the hypergraph to HIF format JSON file.

        Args:
            ``file_path`` (``Union[str, Path]``): The file path to save the HIF file.

        Returns:
            ``bool``: True if successful, False otherwise.
        """
        try:
            self.to_hif(file_path)
            return True
        except Exception:
            return False

    def from_hif(self, hif_data: Union[str, Path, Dict]) -> bool:
        r"""
        Load hypergraph from HIF format data.

        Args:
            ``hif_data`` (``Union[str, Path, Dict]``): HIF data as dict, file path, or JSON string.

        Returns:
            ``bool``: True if successful, False otherwise.
        """
        try:
            # Load data if it's a file path or JSON string
            if isinstance(hif_data, (str, Path)):
                if isinstance(hif_data, str):
                    # Check if it's a JSON string or file path
                    if hif_data.strip().startswith("{"):
                        data = json.loads(hif_data)
                    else:
                        file_path = Path(hif_data)
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                else:
                    with open(hif_data, "r", encoding="utf-8") as f:
                        data = json.load(f)
            elif isinstance(hif_data, dict):
                data = hif_data
            else:
                return False

            # Validate required field
            if "incidences" not in data:
                return False

            # Clear existing data
            self._v_data = {}
            self._e_data = {}
            self._v_inci = defaultdict(set)
            self._clear_cache()

            # Build edge mapping from incidences
            edge_nodes_map: Dict[str, Set[str]] = {}  # edge_id -> set of nodes
            edge_attrs_map: Dict[str, Dict[str, Any]] = {}  # edge_id -> attrs
            node_attrs_map: Dict[str, Dict[str, Any]] = {}  # node_id -> attrs

            # Process incidences
            for incidence in data["incidences"]:
                edge_id = incidence["edge"]
                node_id = incidence["node"]

                # Initialize edge if not seen
                if edge_id not in edge_nodes_map:
                    edge_nodes_map[edge_id] = set()

                edge_nodes_map[edge_id].add(node_id)

                # Store node attributes from incidence
                if "attrs" in incidence:
                    if node_id not in node_attrs_map:
                        node_attrs_map[node_id] = {}
                    node_attrs_map[node_id].update(incidence["attrs"])

            # Process nodes array if present
            if "nodes" in data:
                for node in data["nodes"]:
                    node_id = node["node"]
                    if node_id not in node_attrs_map:
                        node_attrs_map[node_id] = {}
                    if "attrs" in node:
                        node_attrs_map[node_id].update(node["attrs"])
                    if "weight" in node:
                        node_attrs_map[node_id]["weight"] = node["weight"]

            # Process edges array if present
            if "edges" in data:
                for edge in data["edges"]:
                    edge_id = edge["edge"]
                    if edge_id not in edge_attrs_map:
                        edge_attrs_map[edge_id] = {}
                    if "attrs" in edge:
                        edge_attrs_map[edge_id].update(edge["attrs"])
                    if "weight" in edge:
                        edge_attrs_map[edge_id]["weight"] = edge["weight"]

            # Build hypergraph from edge mappings
            for edge_id, node_set in edge_nodes_map.items():
                if len(node_set) < 2:
                    continue  # Skip edges with less than 2 nodes

                # Convert to sorted tuple for edge key
                e_tuple = tuple(sorted(node_set))

                # Add nodes
                for node_id in node_set:
                    if node_id not in self._v_data:
                        node_data = node_attrs_map.get(node_id, {}).copy()
                        self._v_data[node_id] = node_data
                        self._v_inci[node_id] = set()

                # Add edge
                e_data = edge_attrs_map.get(edge_id, {}).copy()
                # Store the original HIF edge ID if it's meaningful (not just a generated ID)
                # Check if edge_id looks like a generated ID (contains underscores and numbers)
                # If it's a meaningful string (like a paper title), store it as 'id' or 'name'
                if not (
                    edge_id.startswith("_")
                    or "_" in edge_id
                    and all(c.isdigit() or c == "_" for c in edge_id.replace("_", ""))
                ):
                    # It's a meaningful ID, store it
                    if "id" not in e_data and "name" not in e_data:
                        e_data["id"] = edge_id
                self._e_data[e_tuple] = e_data

                # Update incidence mapping
                for node_id in node_set:
                    self._v_inci[node_id].add(e_tuple)

            self._clear_cache()
            return True

        except Exception:
            return False

    def load_from_hif(self, file_path: Union[str, Path]) -> bool:
        r"""
        Load hypergraph from HIF format JSON file.

        Args:
            ``file_path`` (``Union[str, Path]``): The file path to load the HIF file from.

        Returns:
            ``bool``: True if successful, False otherwise.
        """
        return self.from_hif(file_path)
