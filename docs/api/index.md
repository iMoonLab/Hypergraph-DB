# API Reference

This section provides complete documentation for all Hypergraph-DB classes and methods.

## Core Classes

### HypergraphDB
::: hyperdb.HypergraphDB
    options:
      show_root_heading: true
      show_source: true

The main class for creating and manipulating hypergraphs. Provides all essential operations for vertices, hyperedges, and persistence.

**Key Features:**
- Add, remove, and update vertices and hyperedges
- Query relationships and neighborhood information  
- Persistence with save/load functionality
- Built-in visualization capabilities

### BaseHypergraphDB
::: hyperdb.BaseHypergraphDB
    options:
      show_root_heading: true
      show_source: true

The foundational base class that defines the core hypergraph structure and basic operations.

## Quick Reference

### Vertex Operations

| Method | Description |
|--------|-------------|
| `add_v(vid, attr=None)` | Add a vertex with optional attributes |
| `remove_v(vid)` | Remove a vertex and all connected hyperedges |
| `update_v(vid, attr)` | Update vertex attributes |
| `v[vid]` | Access vertex attributes |
| `all_v` | Get all vertex IDs |
| `num_v` | Get total number of vertices |

### Hyperedge Operations

| Method | Description |
|--------|-------------|
| `add_e(vertices, attr=None)` | Add a hyperedge connecting multiple vertices |
| `remove_e(eid)` | Remove a hyperedge |
| `update_e(eid, attr)` | Update hyperedge attributes |
| `e[eid]` | Access hyperedge attributes |
| `all_e` | Get all hyperedge IDs |
| `num_e` | Get total number of hyperedges |

### Query Operations

| Method | Description |
|--------|-------------|
| `d_v(vid)` | Get degree of a vertex (number of incident hyperedges) |
| `d_e(eid)` | Get size of a hyperedge (number of vertices) |
| `N_v(vid)` | Get all vertices connected to a vertex via hyperedges |
| `N_e(vid)` | Get all hyperedges containing a vertex |
| `N_v_of_e(eid)` | Get all vertices in a hyperedge |

### Persistence Operations

| Method | Description |
|--------|-------------|
| `save(filepath)` | Save hypergraph to file |
| `load(filepath)` | Load hypergraph from file |
| `copy()` | Create a deep copy of the hypergraph |

### Visualization

| Method | Description |
|--------|-------------|
| `show(port=8080)` | Launch interactive web visualization |

## Usage Examples

### Basic Operations

```python
from hyperdb import HypergraphDB

# Create hypergraph
hg = HypergraphDB()

# Add vertices
hg.add_v(1, {"name": "Alice"})
hg.add_v(2, {"name": "Bob"})
hg.add_v(3, {"name": "Charlie"})

# Add hyperedges
hg.add_e((1, 2), {"relation": "friends"})
hg.add_e((1, 2, 3), {"relation": "team"})

# Query operations
print(f"Alice's degree: {hg.d_v(1)}")
print(f"Alice's neighbors: {hg.N_v(1)}")
print(f"Alice's hyperedges: {hg.N_e(1)}")
```

### Advanced Queries

```python
# Find all vertices with specific attributes
data_scientists = [vid for vid in hg.all_v 
                   if hg.v[vid].get("profession") == "Data Scientist"]

# Find large collaborations (hyperedges with many vertices)
large_teams = [eid for eid in hg.all_e if hg.d_e(eid) >= 4]

# Find vertices that appear in multiple hyperedges
highly_connected = [vid for vid in hg.all_v if hg.d_v(vid) >= 3]
```

### Working with Attributes

```python
# Rich vertex attributes
hg.add_v("person1", {
    "name": "Dr. Smith",
    "age": 45,
    "skills": ["Python", "Machine Learning", "Statistics"],
    "publications": 127,
    "h_index": 42
})

# Rich hyperedge attributes
hg.add_e(("person1", "person2", "person3"), {
    "type": "research_paper",
    "title": "Advanced Hypergraph Algorithms",
    "year": 2024,
    "venue": "ICML",
    "impact_factor": 3.2,
    "citations": 15
})
```

## Error Handling

The API includes comprehensive error handling:

```python
try:
    hg.add_v(1, {"name": "Alice"})
    hg.add_v(1, {"name": "Bob"})  # Raises error - vertex already exists
except ValueError as e:
    print(f"Error: {e}")

try:
    hg.remove_v(999)  # Raises error - vertex doesn't exist
except KeyError as e:
    print(f"Error: {e}")
```

## Performance Considerations

- **Vertex IDs**: Use hashable types (int, str, tuple) for best performance
- **Batch Operations**: Add multiple vertices/edges at once when possible
- **Memory Usage**: Large attribute dictionaries increase memory usage
- **Persistence**: Use pickle format for fastest save/load operations

## Type Hints

Hypergraph-DB includes comprehensive type hints for better IDE support:

```python
from typing import Set, Dict, Any, Tuple, List
from hyperdb import HypergraphDB

# The API is fully typed
hg: HypergraphDB = HypergraphDB()
vertex_id: int = 1
attributes: Dict[str, Any] = {"name": "Alice"}
vertices: Tuple[int, ...] = (1, 2, 3)
```
