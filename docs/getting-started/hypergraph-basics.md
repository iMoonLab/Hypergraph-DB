# Hypergraph Basics

A **hypergraph** is a generalization of a graph where edges (called **hyperedges**) can connect any number of vertices, not just two. This makes hypergraphs particularly powerful for modeling complex relationships in real-world scenarios.

## What is a Hypergraph?

### Traditional Graph vs Hypergraph

=== "Traditional Graph"
    In a traditional graph:
    - **Vertices** (nodes) represent entities
    - **Edges** connect exactly two vertices
    - Relationships are pairwise only
    
    ```python
    # Example: Social network friendship
    edges = [
        (Alice, Bob),      # Alice and Bob are friends
        (Bob, Charlie),    # Bob and Charlie are friends
        (Alice, Charlie)   # Alice and Charlie are friends
    ]
    ```

=== "Hypergraph"
    In a hypergraph:
    - **Vertices** represent entities
    - **Hyperedges** can connect any number of vertices
    - Can model group relationships naturally
    
    ```python
    # Example: Group activities
    hyperedges = [
        (Alice, Bob),              # Alice and Bob have coffee
        (Alice, Bob, Charlie),     # All three work on a project
        (Bob, Charlie, David, Eve) # Team meeting
    ]
    ```

## Key Concepts

### Vertices
Vertices represent the fundamental entities in your data:

```python
from hyperdb import HypergraphDB

hg = HypergraphDB()

# Add vertices with attributes
hg.add_v(1, {"name": "Alice", "age": 30, "role": "Engineer"})
hg.add_v(2, {"name": "Bob", "age": 25, "role": "Designer"})
hg.add_v(3, {"name": "Charlie", "age": 35, "role": "Manager"})
```

### Hyperedges
Hyperedges represent relationships between multiple vertices:

```python
# Binary relationship (like traditional edge)
hg.add_e((1, 2), {"type": "collaboration", "project": "WebApp"})

# Multi-way relationship (unique to hypergraphs)
hg.add_e((1, 2, 3), {"type": "team", "project": "Database"})

# Even larger groups
hg.add_e((1, 2, 3, 4, 5), {"type": "department", "name": "Engineering"})
```

## Real-World Applications

### 1. Academic Collaboration Networks

Model research papers and their authors:

```python
# Authors as vertices
hg.add_v("alice", {"name": "Dr. Alice Smith", "field": "ML"})
hg.add_v("bob", {"name": "Dr. Bob Jones", "field": "NLP"})
hg.add_v("charlie", {"name": "Dr. Charlie Brown", "field": "Vision"})

# Papers as hyperedges connecting all co-authors
hg.add_e(("alice", "bob"), {
    "title": "Deep Learning for NLP",
    "year": 2023,
    "venue": "ICML"
})

hg.add_e(("alice", "bob", "charlie"), {
    "title": "Multimodal AI Systems", 
    "year": 2024,
    "venue": "NeurIPS"
})
```

### 2. E-commerce Transactions

Model shopping baskets with multiple items:

```python
# Products as vertices
hg.add_v("laptop", {"category": "Electronics", "price": 999})
hg.add_v("mouse", {"category": "Electronics", "price": 25})
hg.add_v("keyboard", {"category": "Electronics", "price": 75})

# Shopping baskets as hyperedges
hg.add_e(("laptop", "mouse", "keyboard"), {
    "transaction_id": "T001",
    "customer": "John Doe",
    "total": 1099,
    "date": "2024-01-15"
})
```

### 3. Social Group Activities

Model group events and activities:

```python
# People as vertices
people = ["alice", "bob", "charlie", "david", "eve"]
for person in people:
    hg.add_v(person, {"type": "person"})

# Group activities as hyperedges
hg.add_e(("alice", "bob", "charlie"), {
    "activity": "Study Group",
    "subject": "Machine Learning",
    "location": "Library"
})

hg.add_e(("bob", "david", "eve"), {
    "activity": "Basketball Game",
    "location": "Gym",
    "time": "Saturday 3pm"
})
```

## Advantages of Hypergraphs

### 1. **Natural Group Modeling**
- No need to artificially decompose group relationships into pairwise connections
- Preserves the semantic meaning of multi-way interactions

### 2. **Information Preservation**
- Traditional graphs lose information when representing group relationships
- Hypergraphs maintain the original group structure

### 3. **Flexible Queries**
- Find all groups containing a specific member
- Discover overlapping communities naturally
- Analyze group sizes and compositions

## Mathematical Properties

### Degree Concepts

In hypergraphs, we have several types of degrees:

```python
# Vertex degree: number of hyperedges containing the vertex
vertex_degree = hg.d_v(vertex_id)

# Hyperedge size: number of vertices in the hyperedge  
edge_size = hg.d_e(edge_id)

# Get all neighbors of a vertex (vertices connected via any hyperedge)
neighbors = hg.N_v(vertex_id)
```

### Incidence Relationships

```python
# Get all hyperedges containing a vertex
incident_edges = hg.N_e(vertex_id)

# Get all vertices in a hyperedge
vertices_in_edge = hg.N_v_of_e(edge_id)
```

## Comparison with Other Data Structures

| Feature | Graph | Hypergraph | Database Table |
|---------|-------|------------|----------------|
| Relationship Type | Pairwise | Multi-way | Rows & Columns |
| Group Modeling | Artificial | Natural | Complex JOINs |
| Query Flexibility | Medium | High | Very High |
| Mathematical Theory | Rich | Growing | Different Domain |
| Visualization | Easy | Challenging | Tabular |

## Getting Started with Hypergraph-DB

Now that you understand the basics of hypergraphs, let's explore how to use Hypergraph-DB effectively:

1. **[Quick Start Guide](quickstart.md)** - Basic operations and examples
2. **[API Reference](../api/index.md)** - Complete function documentation
3. **[Advanced Examples](../examples/advanced.md)** - Complex use cases

!!! tip "Best Practices"
    - Use meaningful attributes for both vertices and hyperedges
    - Consider the semantic meaning when deciding between multiple binary edges vs. one hyperedge
    - Leverage the natural group structure in your data
    - Use visualization to understand complex relationships
