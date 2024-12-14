import json
from typing import Tuple
from pathlib import Path
from dataclasses import dataclass

from hyper_db.base import BaseHypergraphDB


@dataclass
class HypergraphDB(BaseHypergraphDB):
    r"""
    Hypergraph database.
    """

    def __post_init__(self):
        self.storage_file = Path(self.storage_file)
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.storage = self._load()

    def _load(self) -> dict:
        if self.storage_file.exists():
            with self.storage_file.open("r") as f:
                return json.load(f)
        return {"vertices": {}, "hyperedges": {}}

    def _dump(self):
        with self.storage_file.open("w") as f:
            json.dump(self.storage, f)

    def v(self, v_name: str) -> dict:
        return self.storage["vertices"].get(v_name, {})

    def e(self, e_tuple: Tuple) -> dict:
        return self.storage["hyperedges"].get(e_tuple, {})

    def add_v(self, v_name: str, v_data: dict):
        self.storage["vertices"][v_name] = v_data
        self._dump()

    def add_e(self, e_tuple: Tuple, e_data: dict):
        self.storage["hyperedges"][e_tuple] = e_data
        self._dump()

    def remove_v(self, v_name: str):
        self.storage["vertices"].pop(v_name, None)
        self._dump()

    def remove_e(self, e_tuple: Tuple):
        self.storage["hyperedges"].pop(e_tuple, None)
        self._dump()
