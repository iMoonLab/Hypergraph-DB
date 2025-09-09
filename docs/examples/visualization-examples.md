# Hypergraph Visualization Examples

This guide provides comprehensive examples of visualizing hypergraphs using Hypergraph-DB's built-in visualization capabilities.

## ⚡ Important: Code Execution Order

When using visualization features, please pay attention to the following code execution order to ensure you see complete analysis results:

```python
# ✅ Recommended code organization
# 1. Create data
hg = HypergraphDB()
hg.add_v(...)
hg.add_e(...)

# 2. Perform analysis first (before visualization)
print("Analysis results:")
print(f"Network size: {hg.num_v} vertices, {hg.num_e} edges")
# Other analysis...

# 3. Start visualization last (program ends when user presses Ctrl+C)
print("Starting visualization...")
hg.draw()  # Blocks until user presses Ctrl+C
```

```python
# ❌ Code organization to avoid
hg.draw()  # Program exits immediately when user presses Ctrl+C
print("These analysis results will never be shown")  # Never executed
```

---

## 🎯 Example 1: Social Network Analysis

Let's create and visualize a social network where groups of friends participate in various activities together.

```python
from hyperdb import HypergraphDB

# Create the social network hypergraph
social_network = HypergraphDB()

# Add people as vertices
people = {
    "alice": {"name": "Alice", "age": 25, "city": "New York", "interests": ["reading", "music"]},
    "bob": {"name": "Bob", "age": 27, "city": "San Francisco", "interests": ["sports", "travel"]},
    "charlie": {"name": "Charlie", "age": 23, "city": "Boston", "interests": ["coding", "gaming"]},
    "diana": {"name": "Diana", "age": 26, "city": "Seattle", "interests": ["art", "photography"]},
    "eve": {"name": "Eve", "age": 24, "city": "Austin", "interests": ["music", "cooking"]},
    "frank": {"name": "Frank", "age": 28, "city": "Denver", "interests": ["hiking", "travel"]}
}

for person_id, info in people.items():
    social_network.add_v(person_id, info)

# Add social activities as hyperedges (connecting groups of friends)
activities = [
    # Small gatherings
    (("alice", "bob"), {
        "activity": "Coffee meetup",
        "date": "2024-01-15",
        "location": "Central Park",
        "duration": 2
    }),
    
    # Medium group activities
    (("alice", "charlie", "eve"), {
        "activity": "Music concert",
        "date": "2024-01-20",
        "location": "Madison Square Garden",
        "duration": 4
    }),
    
    # Large group activities
    (("bob", "diana", "frank", "eve"), {
        "activity": "Hiking trip",
        "date": "2024-02-01",
        "location": "Yosemite National Park",
        "duration": 48
    }),
    
    # Full group gathering
    (("alice", "bob", "charlie", "diana", "eve", "frank"), {
        "activity": "Birthday party",
        "date": "2024-02-14",
        "location": "Alice's apartment",
        "duration": 6
    })
]

for participants, activity_info in activities:
    social_network.add_e(participants, activity_info)

# Perform analysis first, then visualize
print("📊 Network Analysis Results:")
print("=" * 40)

# Analyze the network
print(f"👥 Network size: {social_network.num_v} people, {social_network.num_e} activities")

# Find most social person
most_social = max(social_network.all_v, key=lambda v: social_network.degree_v(v))
print(f"🌟 Most social person: {social_network.v(most_social)['name']} "
      f"({social_network.degree_v(most_social)} activities)")

# Show activity count for all participants
print("\n👥 All participants' activity statistics:")
for person_id in social_network.all_v:
    person_info = social_network.v(person_id)
    activity_count = social_network.degree_v(person_id)
    print(f"  • {person_info['name']}: {activity_count} activities")

print("\n" + "=" * 40)
print("🎨 Starting visualization (press Ctrl+C to close)")
social_network.draw()
```

## 🧬 Example 2: Scientific Collaboration Network

Visualize research collaborations in computational biology:

```python
from hyperdb import HypergraphDB

# Create research collaboration hypergraph
research_network = HypergraphDB()

# Add researchers as vertices
researchers = {
    "dr_smith": {
        "name": "Dr. Sarah Smith",
        "field": "Bioinformatics",
        "institution": "MIT",
        "h_index": 45,
        "experience": 15
    },
    "dr_jones": {
        "name": "Dr. Michael Jones", 
        "field": "Machine Learning",
        "institution": "Stanford",
        "h_index": 38,
        "experience": 12
    },
    "dr_garcia": {
        "name": "Dr. Maria Garcia",
        "field": "Genomics",
        "institution": "Harvard",
        "h_index": 52,
        "experience": 18
    },
    "dr_chen": {
        "name": "Dr. Wei Chen",
        "field": "Systems Biology",
        "institution": "UCSF",
        "h_index": 41,
        "experience": 14
    },
    "dr_taylor": {
        "name": "Dr. James Taylor",
        "field": "Computational Chemistry",
        "institution": "Caltech",
        "h_index": 36,
        "experience": 10
    }
}

for researcher_id, info in researchers.items():
    research_network.add_v(researcher_id, info)

# Add research papers as hyperedges
publications = [
    # Duo collaborations
    (("dr_smith", "dr_jones"), {
        "title": "Deep Learning for Protein Structure Prediction",
        "journal": "Nature Biotechnology",
        "year": 2023,
        "citations": 127,
        "impact_factor": 46.9
    }),
    
    # Trio collaborations
    (("dr_garcia", "dr_chen", "dr_taylor"), {
        "title": "Multi-omics Integration for Disease Prediction",
        "journal": "Cell",
        "year": 2023,
        "citations": 98,
        "impact_factor": 66.9
    }),
    
    # Large collaboration
    (("dr_smith", "dr_jones", "dr_garcia", "dr_chen"), {
        "title": "AI-Driven Drug Discovery Pipeline",
        "journal": "Science",
        "year": 2024,
        "citations": 45,
        "impact_factor": 56.9
    }),
    
    # Cross-institutional mega-collaboration
    (("dr_smith", "dr_jones", "dr_garcia", "dr_chen", "dr_taylor"), {
        "title": "The Future of Personalized Medicine",
        "journal": "Nature Reviews Drug Discovery",
        "year": 2024,
        "citations": 23,
        "impact_factor": 112.3
    })
]

for authors, paper_info in publications:
    research_network.add_e(authors, paper_info)

# Perform research impact analysis first
print("� Research Collaboration Network Analysis:")
print("=" * 50)

# Basic network statistics
print(f"� Network size: {research_network.num_v} researchers, {research_network.num_e} publications")

# Find most collaborative researcher
most_collaborative = max(research_network.all_v, 
                        key=lambda v: research_network.degree_v(v))
researcher_info = research_network.v(most_collaborative)
print(f"🤝 Most collaborative: {researcher_info['name']} "
      f"({research_network.degree_v(most_collaborative)} papers)")

# Find highest-impact publication
highest_impact = max(research_network.all_e, 
                    key=lambda e: research_network.e(e)['impact_factor'])
impact_factor = research_network.e(highest_impact)['impact_factor']
print(f"⭐ Highest impact publication: {impact_factor} impact factor")

# Show detailed information for each researcher
print("\n👨‍🔬 Researcher collaboration statistics:")
for researcher_id in research_network.all_v:
    info = research_network.v(researcher_id)
    collab_count = research_network.degree_v(researcher_id)
    print(f"  • {info['name']} ({info['institution']})")
    print(f"    Field: {info['field']}, H-index: {info['h_index']}, Collaborations: {collab_count}")

print("\n" + "=" * 50)
print("🔬 Starting research network visualization (press Ctrl+C to close)")
research_network.draw()
```

## 🛒 Example 3: E-commerce Purchase Patterns

Analyze customer purchase behaviors and product relationships:

```python
from hyperdb import HypergraphDB
import random

# Create e-commerce hypergraph
ecommerce = HypergraphDB()

# Add products as vertices
products = {
    "laptop": {"name": "Gaming Laptop", "category": "Electronics", "price": 1299.99, "rating": 4.5},
    "mouse": {"name": "Wireless Mouse", "category": "Electronics", "price": 49.99, "rating": 4.3},
    "keyboard": {"name": "Mechanical Keyboard", "category": "Electronics", "price": 129.99, "rating": 4.6},
    "monitor": {"name": "4K Monitor", "category": "Electronics", "price": 399.99, "rating": 4.4},
    "headset": {"name": "Gaming Headset", "category": "Electronics", "price": 89.99, "rating": 4.2},
    "desk": {"name": "Standing Desk", "category": "Furniture", "price": 299.99, "rating": 4.1},
    "chair": {"name": "Ergonomic Chair", "category": "Furniture", "price": 249.99, "rating": 4.7},
    "lamp": {"name": "LED Desk Lamp", "category": "Furniture", "price": 79.99, "rating": 4.0}
}

for product_id, info in products.items():
    ecommerce.add_v(product_id, info)

# Add purchase baskets as hyperedges
purchase_baskets = [
    # Gaming setup purchase
    (("laptop", "mouse", "keyboard", "headset"), {
        "customer_id": "cust_001",
        "purchase_date": "2024-01-15",
        "total_amount": 1569.96,
        "customer_type": "Gaming Enthusiast"
    }),
    
    # Office setup purchase
    (("monitor", "desk", "chair", "lamp"), {
        "customer_id": "cust_002", 
        "purchase_date": "2024-01-18",
        "total_amount": 929.96,
        "customer_type": "Remote Worker"
    }),
    
    # Minimal gaming setup
    (("mouse", "keyboard", "headset"), {
        "customer_id": "cust_003",
        "purchase_date": "2024-01-20",
        "total_amount": 269.97,
        "customer_type": "Budget Gamer"
    }),
    
    # Luxury workspace
    (("laptop", "monitor", "desk", "chair", "lamp"), {
        "customer_id": "cust_004",
        "purchase_date": "2024-01-25",
        "total_amount": 2229.95,
        "customer_type": "Professional"
    }),
    
    # Accessories only
    (("mouse", "lamp"), {
        "customer_id": "cust_005",
        "purchase_date": "2024-01-28",
        "total_amount": 129.98,
        "customer_type": "Casual Buyer"
    })
]

for products_in_basket, purchase_info in purchase_baskets:
    ecommerce.add_e(products_in_basket, purchase_info)

# Perform market basket analysis first
print("� E-commerce Purchase Pattern Analysis:")
print("=" * 45)

# Basic statistics
print(f"🛍️ Store overview: {ecommerce.num_v} products, {ecommerce.num_e} purchases")

# Find most popular product
most_popular = max(ecommerce.all_v, key=lambda v: ecommerce.degree_v(v))
product_info = ecommerce.v(most_popular)
print(f"🏆 Most popular product: {product_info['name']} "
      f"({ecommerce.degree_v(most_popular)} purchases)")

# Find largest purchase
largest_purchase = max(ecommerce.all_e, key=lambda e: len(ecommerce.e_v(e)))
num_items = len(ecommerce.e_v(largest_purchase))
purchase_info = ecommerce.e(largest_purchase)
print(f"💰 Largest purchase: {num_items} items, ${purchase_info['total_amount']:.2f}")

# Show product popularity ranking
print(f"\n📈 Product popularity ranking:")
products_by_popularity = sorted(ecommerce.all_v, 
                               key=lambda v: ecommerce.degree_v(v), 
                               reverse=True)
for i, product_id in enumerate(products_by_popularity, 1):
    info = ecommerce.v(product_id)
    purchases = ecommerce.degree_v(product_id)
    print(f"  {i}. {info['name']} - {purchases} purchases (${info['price']})")

# Analyze customer types
print(f"\n👥 Customer type analysis:")
customer_types = {}
for edge_id in ecommerce.all_e:
    edge_data = ecommerce.e(edge_id)
    customer_type = edge_data.get('customer_type', 'Unknown')
    if customer_type not in customer_types:
        customer_types[customer_type] = 0
    customer_types[customer_type] += 1

for customer_type, count in customer_types.items():
    print(f"  • {customer_type}: {count} purchases")

print("\n" + "=" * 45)
print("🛒 Starting purchase pattern visualization (press Ctrl+C to close)")
ecommerce.draw()
```

## 🎨 Visualization Customization Tips

### 1. **Color Coding by Properties**

The visualization automatically uses different colors for different types of vertices and hyperedges based on their properties.

### 2. **Size Representation**

- **Vertex size**: Often represents degree (number of connections)
- **Hyperedge thickness**: Represents the number of vertices it connects

### 3. **Interactive Features**

- **Hover**: View detailed information about vertices and hyperedges
- **Click**: Select elements to highlight related components
- **Drag**: Rearrange the layout for better viewing
- **Zoom**: Use mouse wheel to zoom in/out

### 4. **Layout Algorithms**

The visualization uses force-directed layout by default, which:
- Groups related vertices together
- Minimizes edge crossings
- Creates aesthetically pleasing arrangements

### 5. **Cross-Platform Compatibility** 🆕

#### Windows Users Note

On Windows systems, we've optimized Ctrl+C handling for the `draw()` function:

```python
# Basic usage (blocking mode)
hg.draw()  # Press Ctrl+C to stop server

# Non-blocking mode (recommended for scripts and automation)
viewer = hg.draw(blocking=False)
# Do other work...
viewer.stop_server()  # Manually stop server
```

#### Platform Differences

| Operating System | Ctrl+C Behavior | Recommended Usage |
|-----------------|----------------|-------------------|
| **Windows** | ✅ Works well after optimization | Both modes available |
| **macOS/Linux** | ✅ Native support excellent | Default blocking mode |

#### Usage Recommendations

```python
# 1. Interactive exploration (recommended blocking mode)
hg.draw(port=8080, blocking=True)

# 2. Script automation (recommended non-blocking mode)
viewer = hg.draw(port=8080, blocking=False)
# Perform other analysis...
time.sleep(30)  # Give users time to view
viewer.stop_server()

# 3. Jupyter Notebook usage
viewer = hg.draw(blocking=False)  # Don't block cell execution
```

## 🔍 Analysis Through Visualization

### Identifying Patterns

1. **Clusters**: Groups of tightly connected vertices
2. **Hubs**: Vertices with many connections (high degree)
3. **Bridges**: Hyperedges that connect different clusters
4. **Outliers**: Isolated or rarely connected vertices

### Network Metrics Visualization

```python
# Example: Analyze network centrality through visualization
def analyze_network_visually(hg):
    print("🎯 Network Analysis:")
    
    # Degree distribution
    degrees = [hg.degree_v(v) for v in hg.all_v]
    print(f"📊 Average degree: {sum(degrees)/len(degrees):.2f}")
    
    # Hub identification
    hubs = [v for v in hg.all_v if hg.degree_v(v) > sum(degrees)/len(degrees)]
    print(f"🌟 Network hubs: {len(hubs)} vertices")
    
    # Hyperedge size distribution
    edge_sizes = [hg.degree_e(e) for e in hg.all_e]
    print(f"🔗 Average hyperedge size: {sum(edge_sizes)/len(edge_sizes):.2f}")
    
    # Visualize with analysis
    hg.draw()

# Apply to any of the above examples
analyze_network_visually(social_network)
```

## 🚀 Advanced Visualization Techniques

### Dynamic Visualization

For time-series data, you can create multiple snapshots:

```python
# Example: Evolving social network
def create_network_snapshots(base_network, time_periods):
    snapshots = []
    for period in time_periods:
        # Create filtered network for each time period
        period_network = HypergraphDB()
        
        # Add vertices (people don't change)
        for v in base_network.all_v:
            period_network.add_v(v, base_network.v(v))
        
        # Add only hyperedges from this time period
        for e in base_network.all_e:
            edge_data = base_network.e(e)
            if edge_data.get('date', '') >= period['start'] and edge_data.get('date', '') <= period['end']:
                period_network.add_e(base_network.e_v(e), edge_data)
        
        snapshots.append((period['name'], period_network))
    
    return snapshots

# Create quarterly snapshots
quarters = [
    {"name": "Q1 2024", "start": "2024-01-01", "end": "2024-03-31"},
    {"name": "Q2 2024", "start": "2024-04-01", "end": "2024-06-30"}
]

# Visualize evolution
for quarter_name, network in create_network_snapshots(social_network, quarters):
    print(f"📅 {quarter_name}:")
    network.draw()
```

This visualization approach helps you understand the structure and evolution of complex relationships in your hypergraph data!
