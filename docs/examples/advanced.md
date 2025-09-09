# Advanced Examples

This page showcases advanced usage patterns and complex applications of Hypergraph-DB.

## Advanced Pattern 1: Temporal Hypergraphs

Model relationships that evolve over time:

```python
from hyperdb import HypergraphDB
from datetime import datetime, timedelta
import json

class TemporalHypergraph(HypergraphDB):
    """Extended HypergraphDB with temporal capabilities."""
    
    def add_temporal_edge(self, vertices, start_time, end_time=None, **kwargs):
        """Add a hyperedge with temporal information."""
        edge_attr = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat() if end_time else None,
            "active": end_time is None or datetime.now() <= end_time,
            **kwargs
        }
        return self.add_e(vertices, edge_attr)
    
    def get_active_edges_at_time(self, timestamp):
        """Get all edges active at a specific time."""
        active_edges = []
        for edge_id in self.all_e:
            edge_data = self.e[edge_id]
            start = datetime.fromisoformat(edge_data["start_time"])
            end = datetime.fromisoformat(edge_data["end_time"]) if edge_data["end_time"] else datetime.now()
            
            if start <= timestamp <= end:
                active_edges.append(edge_id)
        return active_edges
    
    def get_edge_timeline(self, vertex_id):
        """Get timeline of all edges involving a vertex."""
        timeline = []
        for edge_id in self.N_e(vertex_id):
            edge_data = self.e[edge_id]
            timeline.append({
                "edge_id": edge_id,
                "vertices": list(self.N_v_of_e(edge_id)),
                "start": edge_data["start_time"],
                "end": edge_data["end_time"],
                "duration_days": self._calculate_duration(edge_data)
            })
        return sorted(timeline, key=lambda x: x["start"])
    
    def _calculate_duration(self, edge_data):
        """Calculate edge duration in days."""
        start = datetime.fromisoformat(edge_data["start_time"])
        end = datetime.fromisoformat(edge_data["end_time"]) if edge_data["end_time"] else datetime.now()
        return (end - start).days

# Example: Academic collaboration network over time
temporal_hg = TemporalHypergraph()

# Add researchers
researchers = ["alice", "bob", "charlie", "diana", "eve"]
for researcher in researchers:
    temporal_hg.add_v(researcher, {"name": researcher.title(), "type": "researcher"})

# Add temporal collaborations
base_date = datetime(2020, 1, 1)

# Early collaborations
temporal_hg.add_temporal_edge(
    ("alice", "bob"), 
    base_date, 
    base_date + timedelta(days=180),
    project="Deep Learning Basics",
    type="research"
)

# Expanding collaboration
temporal_hg.add_temporal_edge(
    ("alice", "bob", "charlie"), 
    base_date + timedelta(days=90),
    base_date + timedelta(days=365),
    project="Advanced AI Systems",
    type="research"
)

# Large team formation
temporal_hg.add_temporal_edge(
    ("alice", "bob", "charlie", "diana", "eve"), 
    base_date + timedelta(days=200),
    base_date + timedelta(days=500),
    project="AI for Social Good",
    type="research",
    funding="NSF Grant"
)

# Ongoing collaboration
temporal_hg.add_temporal_edge(
    ("charlie", "diana"), 
    base_date + timedelta(days=400),
    None,  # Still ongoing
    project="Quantum ML",
    type="research"
)

# Analyze temporal patterns
print("Alice's collaboration timeline:")
alice_timeline = temporal_hg.get_edge_timeline("alice")
for collab in alice_timeline:
    print(f"  {collab['start'][:10]} - {collab['end'][:10] if collab['end'] else 'ongoing'}: "
          f"{len(collab['vertices'])} people, {collab['duration_days']} days")

# Find active collaborations at specific time
query_date = base_date + timedelta(days=300)
active_edges = temporal_hg.get_active_edges_at_time(query_date)
print(f"\nActive collaborations on {query_date.date()}:")
for edge_id in active_edges:
    participants = list(temporal_hg.N_v_of_e(edge_id))
    edge_data = temporal_hg.e[edge_id]
    print(f"  {edge_data.get('project', 'Unknown')}: {participants}")
```

## Advanced Pattern 2: Multi-Layer Hypergraphs

Model different types of relationships in separate layers:

```python
from hyperdb import HypergraphDB
from enum import Enum

class RelationshipType(Enum):
    SOCIAL = "social"
    PROFESSIONAL = "professional"
    FAMILY = "family"
    ACADEMIC = "academic"

class MultiLayerHypergraph:
    """Hypergraph with multiple relationship layers."""
    
    def __init__(self):
        self.layers = {rel_type: HypergraphDB() for rel_type in RelationshipType}
        self.global_vertices = {}
    
    def add_vertex(self, vid, attributes):
        """Add vertex to all layers."""
        self.global_vertices[vid] = attributes
        for layer in self.layers.values():
            layer.add_v(vid, attributes)
    
    def add_edge(self, vertices, layer_type: RelationshipType, attributes):
        """Add edge to specific layer."""
        layer = self.layers[layer_type]
        edge_id = layer.add_e(vertices, {**attributes, "layer": layer_type.value})
        return edge_id
    
    def get_layer(self, layer_type: RelationshipType):
        """Get specific layer."""
        return self.layers[layer_type]
    
    def get_cross_layer_neighbors(self, vertex_id):
        """Find neighbors across all layers."""
        all_neighbors = set()
        layer_neighbors = {}
        
        for layer_type, layer in self.layers.items():
            if vertex_id in layer.all_v:
                neighbors = layer.N_v(vertex_id)
                layer_neighbors[layer_type.value] = neighbors
                all_neighbors.update(neighbors)
        
        return {
            "all_neighbors": all_neighbors,
            "by_layer": layer_neighbors
        }
    
    def find_multi_layer_communities(self, min_layers=2):
        """Find communities that exist across multiple layers."""
        communities = []
        
        # Get all possible vertex combinations
        all_vertices = list(self.global_vertices.keys())
        
        for i in range(len(all_vertices)):
            for j in range(i + 1, len(all_vertices)):
                for k in range(j + 1, len(all_vertices)):
                    vertex_set = {all_vertices[i], all_vertices[j], all_vertices[k]}
                    
                    # Check how many layers contain this community
                    layers_with_community = []
                    for layer_type, layer in self.layers.items():
                        # Check if these vertices are connected in this layer
                        shared_edges = None
                        for vertex in vertex_set:
                            vertex_edges = set(layer.N_e(vertex)) if vertex in layer.all_v else set()
                            if shared_edges is None:
                                shared_edges = vertex_edges
                            else:
                                shared_edges &= vertex_edges
                        
                        if shared_edges:  # Found shared edges
                            layers_with_community.append(layer_type.value)
                    
                    if len(layers_with_community) >= min_layers:
                        communities.append({
                            "vertices": list(vertex_set),
                            "layers": layers_with_community,
                            "strength": len(layers_with_community)
                        })
        
        return sorted(communities, key=lambda x: x["strength"], reverse=True)

# Example usage
mlhg = MultiLayerHypergraph()

# Add people
people = {
    "alice": {"name": "Alice", "age": 30, "profession": "Engineer"},
    "bob": {"name": "Bob", "age": 28, "profession": "Designer"},
    "charlie": {"name": "Charlie", "age": 32, "profession": "Manager"},
    "diana": {"name": "Diana", "age": 29, "profession": "Scientist"},
    "eve": {"name": "Eve", "age": 27, "profession": "Analyst"}
}

for person_id, info in people.items():
    mlhg.add_vertex(person_id, info)

# Add relationships in different layers
# Social layer
mlhg.add_edge(("alice", "bob"), RelationshipType.SOCIAL, 
              {"type": "friendship", "since": "2020", "strength": "strong"})
mlhg.add_edge(("alice", "charlie", "diana"), RelationshipType.SOCIAL,
              {"type": "friend_group", "activity": "hiking"})

# Professional layer
mlhg.add_edge(("alice", "bob", "charlie"), RelationshipType.PROFESSIONAL,
              {"type": "project_team", "project": "WebApp", "role": "development"})
mlhg.add_edge(("charlie", "diana", "eve"), RelationshipType.PROFESSIONAL,
              {"type": "management_team", "department": "Engineering"})

# Academic layer
mlhg.add_edge(("alice", "diana"), RelationshipType.ACADEMIC,
              {"type": "research_collaboration", "field": "AI"})
mlhg.add_edge(("bob", "charlie", "eve"), RelationshipType.ACADEMIC,
              {"type": "study_group", "subject": "Data Science"})

# Analysis
print("Multi-layer analysis:")

# Analyze Alice's cross-layer connections
alice_connections = mlhg.get_cross_layer_neighbors("alice")
print(f"Alice's connections across layers:")
for layer, neighbors in alice_connections["by_layer"].items():
    if neighbors:
        print(f"  {layer}: {list(neighbors)}")

# Find multi-layer communities
communities = mlhg.find_multi_layer_communities(min_layers=2)
print(f"\nMulti-layer communities:")
for community in communities:
    print(f"  {community['vertices']} - appears in {community['strength']} layers: {community['layers']}")

# Layer-specific analysis
social_layer = mlhg.get_layer(RelationshipType.SOCIAL)
professional_layer = mlhg.get_layer(RelationshipType.PROFESSIONAL)

print(f"\nLayer statistics:")
print(f"  Social: {social_layer.num_v} vertices, {social_layer.num_e} edges")
print(f"  Professional: {professional_layer.num_v} vertices, {professional_layer.num_e} edges")
```

## Advanced Pattern 3: Hypergraph Analytics and Metrics

Implement advanced analytics for hypergraph structures:

```python
from hyperdb import HypergraphDB
from collections import defaultdict, Counter
import math
from itertools import combinations

class HypergraphAnalytics:
    """Advanced analytics for hypergraphs."""
    
    def __init__(self, hypergraph: HypergraphDB):
        self.hg = hypergraph
    
    def clustering_coefficient(self, vertex_id):
        """Calculate clustering coefficient for a vertex in hypergraph context."""
        # Get neighbors of the vertex
        neighbors = self.hg.N_v(vertex_id)
        if len(neighbors) < 2:
            return 0.0
        
        # Count triangular relationships (3-way connections)
        triangular_connections = 0
        possible_triangles = len(list(combinations(neighbors, 2)))
        
        for neighbor1, neighbor2 in combinations(neighbors, 2):
            # Check if vertex_id, neighbor1, neighbor2 form a triangle
            # (are connected by a hyperedge containing all three)
            vertex_edges = set(self.hg.N_e(vertex_id))
            neighbor1_edges = set(self.hg.N_e(neighbor1))
            neighbor2_edges = set(self.hg.N_e(neighbor2))
            
            common_edges = vertex_edges & neighbor1_edges & neighbor2_edges
            if common_edges:
                triangular_connections += 1
        
        return triangular_connections / possible_triangles if possible_triangles > 0 else 0.0
    
    def hyperedge_centrality(self, edge_id):
        """Calculate centrality of a hyperedge based on its connectivity."""
        vertices_in_edge = self.hg.N_v_of_e(edge_id)
        edge_size = len(vertices_in_edge)
        
        # Calculate how well-connected the vertices in this edge are
        total_connections = 0
        for vertex in vertices_in_edge:
            total_connections += self.hg.degree_v(vertex)
        
        # Normalize by edge size
        avg_connectivity = total_connections / edge_size if edge_size > 0 else 0
        
        # Weight by edge size (larger edges potentially more important)
        centrality = avg_connectivity * math.log(edge_size + 1)
        
        return centrality
    
    def find_core_vertices(self, k_core=2):
        """Find k-core vertices (vertices with degree >= k)."""
        core_vertices = []
        for vertex in self.hg.all_v:
            if self.hg.degree_v(vertex) >= k_core:
                core_vertices.append({
                    "vertex": vertex,
                    "degree": self.hg.degree_v(vertex),
                    "attributes": self.hg.v(vertex)
                })
        
        return sorted(core_vertices, key=lambda x: x["degree"], reverse=True)
    
    def community_detection_simple(self):
        """Simple community detection based on shared hyperedges."""
        communities = []
        visited_vertices = set()
        
        for vertex in self.hg.all_v:
            if vertex in visited_vertices:
                continue
            
            # Start a new community
            community = {vertex}
            queue = [vertex]
            
            while queue:
                current_vertex = queue.pop(0)
                # Get all vertices connected via hyperedges
                neighbors = self.hg.N_v(current_vertex)
                
                for neighbor in neighbors:
                    if neighbor not in community:
                        community.add(neighbor)
                        queue.append(neighbor)
            
            # Mark all vertices in this community as visited
            visited_vertices.update(community)
            communities.append(list(community))
        
        return communities
    
    def hyperedge_overlap_analysis(self):
        """Analyze overlaps between hyperedges."""
        edge_list = list(self.hg.all_e)
        overlaps = []
        
        for i, edge1 in enumerate(edge_list):
            for j, edge2 in enumerate(edge_list[i+1:], i+1):
                vertices1 = self.hg.N_v_of_e(edge1)
                vertices2 = self.hg.N_v_of_e(edge2)
                
                intersection = vertices1 & vertices2
                union = vertices1 | vertices2
                
                if intersection:  # There is an overlap
                    jaccard_similarity = len(intersection) / len(union)
                    overlap_size = len(intersection)
                    
                    overlaps.append({
                        "edge1": edge1,
                        "edge2": edge2,
                        "overlap_vertices": list(intersection),
                        "overlap_size": overlap_size,
                        "jaccard_similarity": jaccard_similarity,
                        "edge1_size": len(vertices1),
                        "edge2_size": len(vertices2)
                    })
        
        return sorted(overlaps, key=lambda x: x["jaccard_similarity"], reverse=True)
    
    def structural_statistics(self):
        """Calculate comprehensive structural statistics."""
        vertices = list(self.hg.all_v)
        edges = list(self.hg.all_e)
        
        # Degree statistics
        vertex_degrees = [self.hg.degree_v(v) for v in vertices]
        edge_sizes = [self.hg.degree_e(e) for e in edges]
        
        # Clustering coefficients
        clustering_coeffs = [self.clustering_coefficient(v) for v in vertices]
        
        # Edge centralities
        edge_centralities = [self.hyperedge_centrality(e) for e in edges]
        
        return {
            "basic_stats": {
                "num_vertices": len(vertices),
                "num_edges": len(edges),
                "density": len(edges) / (2 ** len(vertices) - len(vertices) - 1) if len(vertices) > 1 else 0
            },
            "degree_stats": {
                "avg_vertex_degree": sum(vertex_degrees) / len(vertex_degrees) if vertex_degrees else 0,
                "max_vertex_degree": max(vertex_degrees) if vertex_degrees else 0,
                "min_vertex_degree": min(vertex_degrees) if vertex_degrees else 0,
                "degree_distribution": Counter(vertex_degrees)
            },
            "edge_stats": {
                "avg_edge_size": sum(edge_sizes) / len(edge_sizes) if edge_sizes else 0,
                "max_edge_size": max(edge_sizes) if edge_sizes else 0,
                "min_edge_size": min(edge_sizes) if edge_sizes else 0,
                "size_distribution": Counter(edge_sizes)
            },
            "clustering_stats": {
                "avg_clustering": sum(clustering_coeffs) / len(clustering_coeffs) if clustering_coeffs else 0,
                "max_clustering": max(clustering_coeffs) if clustering_coeffs else 0,
                "vertices_with_clustering": len([c for c in clustering_coeffs if c > 0])
            },
            "centrality_stats": {
                "avg_edge_centrality": sum(edge_centralities) / len(edge_centralities) if edge_centralities else 0,
                "max_edge_centrality": max(edge_centralities) if edge_centralities else 0
            }
        }

# Example usage
hg = HypergraphDB()

# Create a complex network
researchers = {f"researcher_{i}": {"name": f"Dr. {chr(65+i)}", "field": ["AI", "ML", "NLP", "Vision"][i%4]} 
               for i in range(20)}

for rid, info in researchers.items():
    hg.add_v(rid, info)

# Add various sized collaborations
collaborations = [
    # Small collaborations
    (("researcher_0", "researcher_1"), {"type": "paper", "size": "small"}),
    (("researcher_2", "researcher_3"), {"type": "paper", "size": "small"}),
    
    # Medium collaborations
    (("researcher_0", "researcher_2", "researcher_4"), {"type": "paper", "size": "medium"}),
    (("researcher_1", "researcher_3", "researcher_5"), {"type": "paper", "size": "medium"}),
    (("researcher_6", "researcher_7", "researcher_8"), {"type": "paper", "size": "medium"}),
    
    # Large collaborations
    (("researcher_0", "researcher_1", "researcher_2", "researcher_4", "researcher_6"), 
     {"type": "grant", "size": "large"}),
    (("researcher_3", "researcher_5", "researcher_7", "researcher_8", "researcher_9", "researcher_10"), 
     {"type": "grant", "size": "large"}),
    
    # Very large collaboration
    (tuple(f"researcher_{i}" for i in range(10, 18)), {"type": "conference", "size": "xlarge"})
]

for collab_vertices, collab_info in collaborations:
    hg.add_e(collab_vertices, collab_info)

# Perform analytics
analytics = HypergraphAnalytics(hg)

# Comprehensive analysis
stats = analytics.structural_statistics()
print("Structural Statistics:")
print(f"  Basic: {stats['basic_stats']}")
print(f"  Degrees: avg={stats['degree_stats']['avg_vertex_degree']:.2f}, "
      f"max={stats['degree_stats']['max_vertex_degree']}")
print(f"  Edge sizes: avg={stats['edge_stats']['avg_edge_size']:.2f}, "
      f"max={stats['edge_stats']['max_edge_size']}")
print(f"  Clustering: avg={stats['clustering_stats']['avg_clustering']:.3f}")

# Find core researchers
core_researchers = analytics.find_core_vertices(k_core=2)
print(f"\nCore researchers (degree >= 2):")
for researcher in core_researchers[:5]:  # Top 5
    print(f"  {researcher['attributes']['name']}: degree {researcher['degree']}")

# Analyze hyperedge overlaps
overlaps = analytics.hyperedge_overlap_analysis()
print(f"\nTop hyperedge overlaps:")
for overlap in overlaps[:3]:  # Top 3
    print(f"  Edges {overlap['edge1']} & {overlap['edge2']}: "
          f"{overlap['overlap_size']} shared vertices, "
          f"Jaccard={overlap['jaccard_similarity']:.3f}")

# Community detection
communities = analytics.community_detection_simple()
print(f"\nDetected {len(communities)} communities:")
for i, community in enumerate(communities):
    if len(community) > 1:  # Only show non-trivial communities
        names = [researchers[r]["name"] for r in community]
        print(f"  Community {i+1}: {names}")
```

## Advanced Pattern 4: Dynamic Hypergraph Updates

Handle dynamic updates and maintain consistency:

```python
from hyperdb import HypergraphDB
import time
from typing import Dict, List, Set, Callable

class DynamicHypergraph(HypergraphDB):
    """Extended hypergraph with change tracking and callbacks."""
    
    def __init__(self):
        super().__init__()
        self.change_log = []
        self.callbacks = {
            'vertex_added': [],
            'vertex_removed': [],
            'vertex_updated': [],
            'edge_added': [],
            'edge_removed': [],
            'edge_updated': []
        }
        self.version = 1
    
    def register_callback(self, event_type: str, callback: Callable):
        """Register callback for specific events."""
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
    
    def _log_change(self, operation: str, entity_type: str, entity_id, old_value=None, new_value=None):
        """Log changes for history tracking."""
        change = {
            'timestamp': time.time(),
            'version': self.version,
            'operation': operation,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'old_value': old_value,
            'new_value': new_value
        }
        self.change_log.append(change)
        self.version += 1
    
    def _trigger_callbacks(self, event_type: str, **kwargs):
        """Trigger registered callbacks."""
        for callback in self.callbacks[event_type]:
            try:
                callback(self, **kwargs)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def add_v(self, vid, attr=None):
        """Add vertex with change tracking."""
        if vid in self.all_v:
            raise ValueError(f"Vertex {vid} already exists")
        
        super().add_v(vid, attr)
        self._log_change('add', 'vertex', vid, None, attr)
        self._trigger_callbacks('vertex_added', vertex_id=vid, attributes=attr)
        return vid
    
    def remove_v(self, vid):
        """Remove vertex with change tracking."""
        if vid not in self.all_v:
            raise KeyError(f"Vertex {vid} does not exist")
        
        old_attr = self.v[vid].copy()
        affected_edges = list(self.N_e(vid))
        
        super().remove_v(vid)
        self._log_change('remove', 'vertex', vid, old_attr, None)
        self._trigger_callbacks('vertex_removed', vertex_id=vid, old_attributes=old_attr, 
                               affected_edges=affected_edges)
        return vid
    
    def update_v(self, vid, attr):
        """Update vertex with change tracking."""
        if vid not in self.all_v:
            raise KeyError(f"Vertex {vid} does not exist")
        
        old_attr = self.v[vid].copy()
        super().update_v(vid, attr)
        new_attr = self.v[vid].copy()
        
        self._log_change('update', 'vertex', vid, old_attr, new_attr)
        self._trigger_callbacks('vertex_updated', vertex_id=vid, 
                               old_attributes=old_attr, new_attributes=new_attr)
        return vid
    
    def add_e(self, vertices, attr=None):
        """Add edge with change tracking."""
        edge_id = super().add_e(vertices, attr)
        self._log_change('add', 'edge', edge_id, None, {'vertices': vertices, 'attributes': attr})
        self._trigger_callbacks('edge_added', edge_id=edge_id, vertices=vertices, attributes=attr)
        return edge_id
    
    def batch_update(self, operations: List[Dict]):
        """Perform batch updates atomically."""
        saved_state = self.copy()
        successful_ops = []
        
        try:
            for op in operations:
                op_type = op['type']
                if op_type == 'add_vertex':
                    self.add_v(op['vertex_id'], op.get('attributes'))
                elif op_type == 'add_edge':
                    self.add_e(op['vertices'], op.get('attributes'))
                elif op_type == 'update_vertex':
                    self.update_v(op['vertex_id'], op['attributes'])
                # Add more operation types as needed
                
                successful_ops.append(op)
        
        except Exception as e:
            # Rollback to saved state
            self.__dict__.update(saved_state.__dict__)
            print(f"Batch update failed at operation {len(successful_ops)}: {e}")
            print("Rolled back all changes.")
            raise
        
        return successful_ops
    
    def get_changes_since_version(self, version: int):
        """Get all changes since a specific version."""
        return [change for change in self.change_log if change['version'] > version]
    
    def export_changes(self, start_version: int = 0):
        """Export changes for synchronization."""
        changes = self.get_changes_since_version(start_version)
        return {
            'current_version': self.version,
            'changes': changes
        }

# Example usage with change tracking
dhg = DynamicHypergraph()

# Set up callbacks for monitoring
def vertex_added_callback(hg, vertex_id, attributes):
    print(f"✅ Vertex {vertex_id} added with attributes: {attributes}")

def edge_added_callback(hg, edge_id, vertices, attributes):
    print(f"🔗 Edge {edge_id} added connecting {vertices}")

def vertex_removed_callback(hg, vertex_id, old_attributes, affected_edges):
    print(f"❌ Vertex {vertex_id} removed, affecting {len(affected_edges)} edges")

# Register callbacks
dhg.register_callback('vertex_added', vertex_added_callback)
dhg.register_callback('edge_added', edge_added_callback)
dhg.register_callback('vertex_removed', vertex_removed_callback)

# Perform operations
print("Performing dynamic operations:")

# Add vertices
dhg.add_v("alice", {"name": "Alice", "role": "researcher"})
dhg.add_v("bob", {"name": "Bob", "role": "engineer"})
dhg.add_v("charlie", {"name": "Charlie", "role": "manager"})

# Add edges
dhg.add_e(("alice", "bob"), {"type": "collaboration", "project": "AI"})
dhg.add_e(("alice", "bob", "charlie"), {"type": "team", "department": "R&D"})

# Update vertex
dhg.update_v("alice", {"name": "Dr. Alice", "role": "senior_researcher", "publications": 25})

# Batch operations
batch_ops = [
    {"type": "add_vertex", "vertex_id": "diana", "attributes": {"name": "Diana", "role": "analyst"}},
    {"type": "add_edge", "vertices": ("charlie", "diana"), "attributes": {"type": "supervision"}},
    {"type": "update_vertex", "vertex_id": "bob", "attributes": {"name": "Robert", "role": "senior_engineer"}}
]

print("\nPerforming batch update:")
successful = dhg.batch_update(batch_ops)
print(f"Successfully completed {len(successful)} operations")

# Show change history
print(f"\nChange history (version {dhg.version}):")
for change in dhg.change_log[-5:]:  # Last 5 changes
    print(f"  v{change['version']}: {change['operation']} {change['entity_type']} {change['entity_id']}")

# Export changes for synchronization
changes_export = dhg.export_changes(start_version=3)
print(f"\nChanges since version 3: {len(changes_export['changes'])} changes")

# Remove vertex (will trigger callback about affected edges)
print("\nRemoving vertex:")
dhg.remove_v("alice")

print(f"Final state: {dhg.num_v} vertices, {dhg.num_e} edges")
```

These advanced patterns demonstrate the flexibility and power of Hypergraph-DB for complex scenarios:

1. **Temporal Hypergraphs**: Track relationships over time
2. **Multi-Layer Networks**: Model different relationship types separately
3. **Advanced Analytics**: Calculate sophisticated metrics and detect patterns  
4. **Dynamic Updates**: Handle real-time changes with consistency and monitoring

Each pattern can be combined and adapted for specific use cases, providing a robust foundation for complex hypergraph applications.
