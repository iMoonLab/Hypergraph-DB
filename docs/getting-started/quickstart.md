# Quick Start Guide

This guide will get you up and running with Hypergraph-DB in just a few minutes!

## Installation

First, install Hypergraph-DB:

```bash
pip install hypergraph-db
```

## Your First Hypergraph

Let's create a simple hypergraph representing a social network with group activities:

```python
from hyperdb import HypergraphDB

# Create a new hypergraph database
hg = HypergraphDB()

# Add some people as vertices
hg.add_v(1, {"name": "Alice", "age": 30, "city": "New York"})
hg.add_v(2, {"name": "Bob", "age": 24, "city": "Los Angeles"})
hg.add_v(3, {"name": "Charlie", "age": 28, "city": "Chicago"})
hg.add_v(4, {"name": "David", "age": 35, "city": "Miami"})

print(f"Added {hg.num_v} vertices")
```

## Adding Relationships

Now let's add some relationships (hyperedges):

```python
# Pairwise relationships
hg.add_e((1, 2), {"relation": "friends", "since": "2020"})
hg.add_e((2, 3), {"relation": "colleagues", "company": "TechCorp"})

# Group relationships (the power of hypergraphs!)
hg.add_e((1, 2, 3), {"relation": "study_group", "subject": "Machine Learning"})
hg.add_e((1, 3, 4), {"relation": "project_team", "project": "WebApp"})

print(f"Added {hg.num_e} hyperedges")
```

## Basic Queries

Explore your hypergraph with simple queries:

```python
# Get all vertices and edges
print("All vertices:", hg.all_v)
print("All edges:", hg.all_e)

# Get information about specific vertices
alice_info = hg.v[1]
print("Alice's info:", alice_info)

# Find all hyperedges containing Alice (vertex 1)
alice_edges = hg.N_e(1)
print("Hyperedges containing Alice:", alice_edges)

# Get degree information
alice_degree = hg.d_v(1)  # Number of hyperedges containing Alice
print(f"Alice is connected to {alice_degree} hyperedges")
```

## Working with Attributes

Hypergraph-DB allows rich attributes on both vertices and hyperedges:

```python
# Update vertex attributes
hg.update_v(1, {"profession": "Data Scientist", "skills": ["Python", "ML"]})

# Update edge attributes
edge_id = list(hg.all_e)[0]  # Get first edge ID
hg.update_e(edge_id, {"strength": "strong", "frequency": "daily"})

# Access updated information
print("Updated Alice info:", hg.v[1])
print("Updated edge info:", hg.e[edge_id])
```

## Persistence

Save and load your hypergraph:

```python
# Save to file
hg.save("my_social_network.pkl")

# Load from file
hg_loaded = HypergraphDB()
hg_loaded.load("my_social_network.pkl")

print(f"Loaded hypergraph with {hg_loaded.num_v} vertices and {hg_loaded.num_e} edges")
```

## Visualization

Visualize your hypergraph in a web browser:

```python
# This opens an interactive visualization in your default browser
hg.draw()
```

The visualization will show:

- **Vertices** as nodes with their attributes
- **Hyperedges** connecting multiple vertices
- **Interactive features** for exploring the structure

## Complete Example

Here's a complete example putting it all together:

```python
from hyperdb import HypergraphDB

def create_research_collaboration_network():
    """Create a hypergraph representing research collaborations."""

    hg = HypergraphDB()

    # Add researchers
    researchers = {
        1: {"name": "Dr. Alice", "field": "ML", "university": "MIT"},
        2: {"name": "Dr. Bob", "field": "NLP", "university": "Stanford"},
        3: {"name": "Dr. Charlie", "field": "Vision", "university": "CMU"},
        4: {"name": "Dr. Diana", "field": "Robotics", "university": "Berkeley"},
        5: {"name": "Dr. Eve", "field": "Theory", "university": "Princeton"}
    }

    for id, info in researchers.items():
        hg.add_v(id, info)

    # Add research papers (as hyperedges connecting collaborators)
    papers = [
        ((1, 2), {"title": "Deep Learning for NLP", "year": 2023, "venue": "ICML"}),
        ((1, 3), {"title": "Computer Vision Advances", "year": 2023, "venue": "CVPR"}),
        ((2, 3, 4), {"title": "Multimodal AI", "year": 2024, "venue": "NeurIPS"}),
        ((1, 2, 3, 5), {"title": "AI Theory and Practice", "year": 2024, "venue": "JMLR"})
    ]

    for authors, paper_info in papers:
        hg.add_e(authors, paper_info)

    return hg

# Create the network
research_hg = create_research_collaboration_network()

# Analyze the network
print(f"Research network: {research_hg.num_v} researchers, {research_hg.num_e} papers")

# Find Dr. Alice's collaborations
alice_papers = research_hg.N_e(1)
print(f"Dr. Alice has collaborated on {len(alice_papers)} papers")

# Find the largest collaboration
largest_collab = max(research_hg.all_e, key=lambda e: research_hg.d_e(e))
collab_size = research_hg.d_e(largest_collab)
print(f"Largest collaboration has {collab_size} authors")

# Visualize the research network
research_hg.draw()
```

## Next Steps

Now that you've learned the basics, explore more advanced features:

- **[Hypergraph Concepts](hypergraph-basics.md)** - Deep dive into hypergraph theory
- **[API Reference](../api/index.md)** - Complete documentation of all functions
- **[Advanced Examples](../examples/advanced.md)** - Complex use cases and patterns
- **[Visualization Guide](../visualization/index.md)** - Interactive visualization features

## Common Patterns

### Pattern 1: Multi-level Relationships

```python
# Different types of relationships at different levels
hg.add_e((1, 2), {"type": "friendship"})
hg.add_e((1, 2, 3), {"type": "team"})
hg.add_e((1, 2, 3, 4, 5), {"type": "department"})
```

### Pattern 2: Temporal Networks

```python
# Add time information to track evolution
hg.add_e((1, 2), {"type": "collaboration", "start": "2023-01", "end": "2023-06"})
hg.add_e((1, 2, 3), {"type": "collaboration", "start": "2023-07", "end": "2024-01"})
```

### Pattern 3: Weighted Relationships

```python
# Add weights to represent relationship strength
hg.add_e((1, 2, 3), {"type": "project", "weight": 0.8, "importance": "high"})
```

!!! tip "Performance Tips" - Use meaningful vertex and edge IDs for easier debugging - Batch operations when adding many vertices/edges - Use `draw()` periodically to visualize and understand your data structure - Save your work frequently with `save()` method
