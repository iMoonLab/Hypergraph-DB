from pathlib import Path
from typing import Union, Tuple, List
from dataclasses import dataclass


@dataclass
class BaseHypergraphDB:
    r"""
    Base class for hypergraph database.
    """

    storage_file: Union[str, Path] = "hyper_db.xml"

    def v(self, v_name: str) -> dict:
        r"""
        Return the vertex data.

        Args:
            ``v_name`` (``str``): The vertex name.
        """
        raise NotImplementedError

    def e(self, e_tuple: Tuple) -> dict:
        r"""
        Return the hyperedge data.

        Args:
            ``e_tuple`` (``Tuple``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        raise NotImplementedError

    def add_v(self, v_name: str, v_data: dict):
        r"""
        Add a vertex to the hypergraph.

        Args:
            ``v_name`` (``str``): The vertex name.
            ``v_data`` (``dict``): The vertex data.
        """
        raise NotImplementedError

    def add_e(self, e_tuple: Tuple, e_data: dict):
        r"""
        Add a hyperedge to the hypergraph.

        Args:
            ``e_tuple`` (``Tuple``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
            ``e_data`` (``dict``): The hyperedge data.
        """
        raise NotImplementedError

    def remove_v(self, v_name: str):
        r"""
        Remove a vertex from the hypergraph.

        Args:
            ``v_name`` (``str``): The vertex name.
        """
        raise NotImplementedError

    def remove_e(self, e_tuple: Tuple):
        r"""
        Remove a hyperedge from the hypergraph.

        Args:
            ``e_tuple`` (``Tuple``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        raise NotImplementedError

    def update_v(self, v_name: str):
        r"""
        Update the vertex data.

        Args:
            ``v_name`` (``str``): The vertex name.
        """
        raise NotImplementedError

    def update_e(self, e_tuple: Tuple):
        r"""
        Update the hyperedge data.

        Args:
            ``e_tuple`` (``Tuple``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        raise NotImplementedError

    def has_v(self, v_name: str) -> bool:
        r"""
        Return True if the vertex exists in the hypergraph.

        Args:
            ``v_name`` (``str``): The vertex name.
        """
        raise NotImplementedError

    def has_e(self, e_tuple: Tuple) -> bool:
        r"""
        Return True if the hyperedge exists in the hypergraph.

        Args:
            ``e_tuple`` (``Tuple``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        raise NotImplementedError

    def degree_v(self, v_name: str) -> int:
        r"""
        Return the degree of the vertex.

        Args:
            ``v_name`` (``str``): The vertex name.
        """
        raise NotImplementedError

    def degree_e(self, e_tuple: Tuple) -> int:
        r"""
        Return the degree of the hyperedge.

        Args:
            ``e_tuple`` (``Tuple``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        raise NotImplementedError

    def nbr_v(self, v_name: str) -> list:
        r"""
        Return the vertex neighbors of the vertex.

        Args:
            ``v_name`` (``str``): The vertex name.
        """
        raise NotImplementedError

    def nbr_e_of_v(self, v_name: str) -> list:
        r"""
        Return the hyperedge neighbors of the vertex.

        Args:
            ``v_name`` (``str``): The vertex name.
        """
        raise NotImplementedError

    def nbr_v_of_e(self, e_tuple: Tuple) -> list:
        r"""
        Return the vertex neighbors of the hyperedge.

        Args:
            ``e_tuple`` (``Tuple``): The hyperedge tuple: (v1_name, v2_name, ..., vn_name).
        """
        raise NotImplementedError

    def draw(self, ):
        r"""
        Draw the hypergraph.
        """
        raise NotImplementedError
    
    def sub(self, v_name_list: List[str]):
        r"""
        Return the sub-hypergraph.

        Args:
            ``v_name_list`` (``List[str]``): The list of vertex names.
        """
        raise NotImplementedError
    
    def sub_from_v(self, v_name: str, depth: int):
        r"""
        Return the sub-hypergraph from the vertex.

        Args:
            ``v_name`` (``str``): The vertex name.
            ``depth`` (``int``): The depth of the sub-hypergraph.
        """
        raise NotImplementedError
