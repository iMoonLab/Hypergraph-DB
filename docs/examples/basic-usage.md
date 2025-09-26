# Basic Usage Examples

This page provides practical examples of using Hypergraph-DB for common scenarios.

## Example 1: Academic Collaboration Network

Model research collaborations between academics:

```python
from hyperdb import HypergraphDB

# Create the hypergraph
hg = HypergraphDB()

# Add researchers as vertices
researchers = {
    "alice": {"name": "Dr. Alice Smith", "field": "Machine Learning", "university": "MIT"},
    "bob": {"name": "Dr. Bob Johnson", "field": "Natural Language Processing", "university": "Stanford"},
    "charlie": {"name": "Dr. Charlie Brown", "field": "Computer Vision", "university": "CMU"},
    "diana": {"name": "Dr. Diana Wilson", "field": "Robotics", "university": "Berkeley"},
    "eve": {"name": "Dr. Eve Davis", "field": "Theory", "university": "Princeton"}
}

for researcher_id, info in researchers.items():
    hg.add_v(researcher_id, info)

# Add papers as hyperedges (connecting all co-authors)
papers = [
    (("alice", "bob"), {
        "title": "Deep Learning for Natural Language Understanding",
        "year": 2023,
        "venue": "ICML",
        "citations": 45
    }),
    (("alice", "charlie"), {
        "title": "Vision-Language Models for Scene Understanding",
        "year": 2023,
        "venue": "CVPR",
        "citations": 38
    }),
    (("bob", "charlie", "diana"), {
        "title": "Multimodal AI for Autonomous Systems",
        "year": 2024,
        "venue": "NeurIPS",
        "citations": 12
    }),
    (("alice", "bob", "charlie", "eve"), {
        "title": "Theoretical Foundations of Modern AI",
        "year": 2024,
        "venue": "JMLR",
        "citations": 23
    })
]

for authors, paper_info in papers:
    hg.add_e(authors, paper_info)

# Analysis
print(f"Network: {hg.num_v} researchers, {hg.num_e} papers")

# Find most collaborative researcher
most_collaborative = max(hg.all_v, key=lambda v: hg.degree_v(v))
print(f"Most collaborative: {hg.v(most_collaborative)['name']} "
      f"({hg.degree_v(most_collaborative)} papers)")

# Find largest collaboration
largest_paper = max(hg.all_e, key=lambda e: hg.degree_e(e))
num_authors = hg.degree_e(largest_paper)
print(f"Largest collaboration: {num_authors} authors")

# Visualize the network
hg.draw()
```

## Example 2: E-commerce Recommendation System

Model shopping patterns and product relationships:

```python
from hyperdb import HypergraphDB
from collections import defaultdict

# Create product catalog
hg = HypergraphDB()

# Add products as vertices
products = {
    "laptop_1": {"name": "Gaming Laptop", "category": "Electronics", "price": 1299.99, "brand": "TechCorp"},
    "mouse_1": {"name": "Wireless Mouse", "category": "Electronics", "price": 49.99, "brand": "TechCorp"},
    "keyboard_1": {"name": "Mechanical Keyboard", "category": "Electronics", "price": 129.99, "brand": "KeyMaster"},
    "monitor_1": {"name": "4K Monitor", "category": "Electronics", "price": 399.99, "brand": "DisplayPro"},
    "headset_1": {"name": "Gaming Headset", "category": "Electronics", "price": 89.99, "brand": "AudioMax"},
    "desk_1": {"name": "Standing Desk", "category": "Furniture", "price": 299.99, "brand": "ErgoFurn"},
    "chair_1": {"name": "Ergonomic Chair", "category": "Furniture", "price": 249.99, "brand": "ErgoFurn"}
}

for product_id, info in products.items():
    hg.add_v(product_id, info)

# Add shopping baskets as hyperedges
shopping_sessions = [
    (("laptop_1", "mouse_1", "keyboard_1"), {
        "session_id": "S001",
        "customer": "John Doe",
        "total": 1479.97,
        "date": "2024-01-15"
    }),
    (("monitor_1", "headset_1"), {
        "session_id": "S002", 
        "customer": "Jane Smith",
        "total": 489.98,
        "date": "2024-01-16"
    }),
    (("desk_1", "chair_1", "monitor_1"), {
        "session_id": "S003",
        "customer": "Bob Wilson",
        "total": 949.97,
        "date": "2024-01-17"
    }),
    (("laptop_1", "mouse_1", "headset_1", "monitor_1"), {
        "session_id": "S004",
        "customer": "Alice Brown",
        "total": 1839.96,
        "date": "2024-01-18"
    })
]

for products_in_basket, session_info in shopping_sessions:
    hg.add_e(products_in_basket, session_info)

# Recommendation analysis
def find_frequently_bought_together(product_id, min_frequency=2):
    """Find products frequently bought together with the given product."""
    # Find all shopping sessions containing this product
    sessions_with_product = hg.nbr_e_of_v(product_id)

    # Count co-occurrences
    co_occurrence = defaultdict(int)
    for session in sessions_with_product:
        other_products = hg.nbr_v_of_e(session) - {product_id}
        for other_product in other_products:
            co_occurrence[other_product] += 1

    # Filter by minimum frequency
    recommendations = {product: count for product, count in co_occurrence.items() if count >= min_frequency}

    return sorted(recommendations.items(), key=lambda x: x[1], reverse=True)


# Generate recommendations
laptop_recommendations = find_frequently_bought_together("laptop_1")
print("Products frequently bought with Gaming Laptop:")
for product, frequency in laptop_recommendations:
    product_name = hg.v(product)["name"]
    print(f"  {product_name}: {frequency} times")

# Find most popular product categories
category_popularity = defaultdict(int)
for edge in hg.all_e:
    products_in_session = hg.nbr_v_of_e(edge)
    for product in products_in_session:
        category = hg.v(product)["category"]
        category_popularity[category] += 1

print("\nCategory popularity:")
for category, count in sorted(category_popularity.items(), key=lambda x: x[1], reverse=True):
    print(f"  {category}: {count} purchases")

hg.draw()
```

## Example 3: Social Network Group Analysis

Analyze group dynamics in social networks:

```python
from hyperdb import HypergraphDB
from collections import defaultdict

# Create social network
hg = HypergraphDB()

# Add people
people = {
    1: {"name": "Alice", "age": 28, "city": "New York", "interests": ["tech", "music"]},
    2: {"name": "Bob", "age": 32, "city": "San Francisco", "interests": ["tech", "sports"]},
    3: {"name": "Charlie", "age": 25, "city": "Boston", "interests": ["music", "art"]},
    4: {"name": "Diana", "age": 30, "city": "Seattle", "interests": ["tech", "travel"]},
    5: {"name": "Eve", "age": 27, "city": "Austin", "interests": ["art", "food"]},
    6: {"name": "Frank", "age": 35, "city": "Chicago", "interests": ["sports", "food"]},
    7: {"name": "Grace", "age": 29, "city": "Portland", "interests": ["travel", "music"]},
    8: {"name": "Henry", "age": 31, "city": "Denver", "interests": ["tech", "art"]},
}

for person_id, info in people.items():
    hg.add_v(person_id, info)

# Add group activities as hyperedges
activities = [
    # Small groups
    ((1, 2), {"type": "coffee_meeting", "location": "Cafe Central", "date": "2024-01-10"}),
    ((3, 5), {"type": "art_gallery", "location": "MoMA", "date": "2024-01-12"}),
    # Medium groups
    ((1, 2, 4), {"type": "tech_meetup", "location": "TechHub", "date": "2024-01-15"}),
    ((3, 5, 7), {"type": "music_concert", "location": "Music Hall", "date": "2024-01-18"}),
    ((2, 6), {"type": "sports_game", "location": "Stadium", "date": "2024-01-20"}),
    # Large groups
    ((1, 2, 3, 4, 5), {"type": "birthday_party", "location": "Alice's House", "date": "2024-01-25"}),
    ((4, 6, 7, 8), {"type": "travel_planning", "location": "Online", "date": "2024-01-28"}),
    # Very large group
    ((1, 2, 3, 4, 5, 6, 7, 8), {"type": "company_picnic", "location": "Central Park", "date": "2024-02-01"}),
]

for participants, activity_info in activities:
    hg.add_e(participants, activity_info)


# Social network analysis
def analyze_social_network(hg):
    """Analyze the social network structure."""

    # Find most social person (highest degree)
    most_social = max(hg.all_v, key=lambda v: hg.degree_v(v))
    print(
        f"Most social person: {hg.v(most_social)['name']} " f"(participates in {hg.degree_v(most_social)} activities)"
    )

    # Analyze group sizes
    group_sizes = [hg.degree_e(e) for e in hg.all_e]
    avg_group_size = sum(group_sizes) / len(group_sizes)
    print(f"Average group size: {avg_group_size:.1f}")
    print(f"Largest group: {max(group_sizes)} people")
    print(f"Smallest group: {min(group_sizes)} people")

    # Find common interest groups
    interest_groups = defaultdict(set)
    for edge in hg.all_e:
        participants = hg.nbr_v_of_e(edge)
        # Find common interests
        if len(participants) >= 2:
            common_interests = set(hg.v(list(participants)[0])["interests"])
            for person in participants:
                common_interests &= set(hg.v(person)["interests"])

            for interest in common_interests:
                interest_groups[interest].update(participants)

    print("\nInterest-based communities:")
    for interest, community in interest_groups.items():
        if len(community) >= 3:  # Only show communities with 3+ people
            names = [hg.v(person)["name"] for person in community]
            print(f"  {interest}: {', '.join(names)}")


analyze_social_network(hg)


# Find bridges (people who connect different groups)
def find_bridges(hg):
    """Find people who act as bridges between groups."""
    bridges = []

    for person in hg.all_v:
        # Get all groups this person participates in
        person_groups = hg.nbr_e_of_v(person)

        if len(person_groups) >= 2:  # Person is in multiple groups
            # Check if removing this person would disconnect the groups
            other_connections = 0
            for group1 in person_groups:
                for group2 in person_groups:
                    if group1 != group2:
                        # Check if groups share other members
                        group1_members = set(hg.nbr_v_of_e(group1)) - {person}
                        group2_members = set(hg.nbr_v_of_e(group2)) - {person}
                        if group1_members & group2_members:
                            other_connections += 1
                            break

            if other_connections < len(person_groups) - 1:
                bridges.append(person)

    return bridges


bridges = find_bridges(hg)
print(f"\nBridge people (connect different groups):")
for bridge in bridges:
    name = hg.v(bridge)["name"]
    num_groups = hg.degree_v(bridge)
    print(f"  {name} (connects {num_groups} groups)")

# Visualize the social network
hg.draw()
```

## Example 4: Knowledge Graph

Model complex knowledge relationships:

```python
from hyperdb import HypergraphDB

# Create knowledge graph
kg = HypergraphDB()

# Add entities
entities = {
    # People
    "einstein": {"type": "person", "name": "Albert Einstein", "birth": 1879, "death": 1955},
    "curie": {"type": "person", "name": "Marie Curie", "birth": 1867, "death": 1934},
    "newton": {"type": "person", "name": "Isaac Newton", "birth": 1642, "death": 1727},
    # Concepts
    "relativity": {"type": "theory", "name": "Theory of Relativity", "year": 1915},
    "radioactivity": {"type": "phenomenon", "name": "Radioactivity", "discovered": 1896},
    "gravity": {"type": "force", "name": "Gravitational Force", "discovered": 1687},
    # Institutions
    "princeton": {"type": "university", "name": "Princeton University", "founded": 1746},
    "sorbonne": {"type": "university", "name": "University of Paris", "founded": 1150},
    # Awards
    "nobel_physics": {"type": "award", "name": "Nobel Prize in Physics"},
    "nobel_chemistry": {"type": "award", "name": "Nobel Prize in Chemistry"},
}

for entity_id, info in entities.items():
    kg.add_v(entity_id, info)

# Add complex relationships as hyperedges
relationships = [
    # Person-Theory relationships
    (("einstein", "relativity"), {"relation": "developed", "year": 1915}),
    (("curie", "radioactivity"), {"relation": "studied", "significance": "pioneering"}),
    (("newton", "gravity"), {"relation": "discovered", "year": 1687}),
    # Person-Institution relationships
    (("einstein", "princeton"), {"relation": "worked_at", "period": "1933-1955"}),
    (("curie", "sorbonne"), {"relation": "studied_at", "degree": "PhD"}),
    # Award relationships
    (("einstein", "nobel_physics"), {"relation": "won", "year": 1921, "for": "photoelectric effect"}),
    (("curie", "nobel_physics"), {"relation": "won", "year": 1903, "shared_with": "Pierre Curie"}),
    (("curie", "nobel_chemistry"), {"relation": "won", "year": 1911, "first_woman": True}),
    # Complex multi-way relationships
    (("einstein", "curie", "nobel_physics"), {"relation": "both_won", "significance": "two great physicists"}),
    (
        ("relativity", "gravity", "newton", "einstein"),
        {"relation": "theory_evolution", "description": "Newton's gravity evolved into Einstein's relativity"},
    ),
]

for entities_in_rel, rel_info in relationships:
    kg.add_e(entities_in_rel, rel_info)


# Knowledge graph queries
def find_related_entities(entity_id, relation_type=None):
    """Find all entities related to the given entity."""
    related = set()

    # Get all relationships involving this entity
    for edge in kg.nbr_e_of_v(entity_id):
        edge_info = kg.e(edge)

        # Filter by relation type if specified
        if relation_type and edge_info.get("relation") != relation_type:
            continue

        # Add all other entities in this relationship
        other_entities = kg.nbr_v_of_e(edge) - {entity_id}
        related.update(other_entities)

    return related


# Find entities related to Einstein
einstein_related = find_related_entities("einstein")
print("Entities related to Einstein:")
for entity in einstein_related:
    entity_info = kg.v(entity)
    print(f"  {entity_info['name']} ({entity_info['type']})")

# Find award winners
award_winners = find_related_entities("nobel_physics", "won")
print(f"\nNobel Physics winners in our graph:")
for winner in award_winners:
    winner_info = kg.v(winner)
    print(f"  {winner_info['name']}")

# Find theory developers
print(f"\nTheory developers:")
for theory in ["relativity", "radioactivity"]:
    developers = find_related_entities(theory, "developed") | find_related_entities(theory, "studied")
    theory_name = kg.v(theory)["name"]
    developer_names = [kg.v(dev)["name"] for dev in developers]
    print(f"  {theory_name}: {', '.join(developer_names)}")

# Visualize the knowledge graph
kg.draw()

```

## Tips for Effective Usage

### 1. Choose Meaningful IDs

```python
# Good: descriptive IDs
hg.add_v("user_123", {"name": "Alice"})
hg.add_v("product_laptop_001", {"name": "Gaming Laptop"})

# Less ideal: generic IDs without context
hg.add_v(1, {"name": "Alice"})
hg.add_v(2, {"name": "Gaming Laptop"})
```

### 2. Use Rich Attributes

```python
# Rich attributes provide more analysis possibilities
hg.add_v("paper_001", {
    "title": "Deep Learning Advances",
    "year": 2024,
    "venue": "ICML",
    "citations": 45,
    "keywords": ["deep learning", "neural networks"],
    "impact_factor": 3.2,
    "open_access": True
})
```

### 3. Leverage Hypergraph Structure

```python
# Instead of multiple binary edges:
hg.add_e((1, 2), {"type": "collaboration"})
hg.add_e((1, 3), {"type": "collaboration"})
hg.add_e((2, 3), {"type": "collaboration"})

# Use a single hyperedge for group relationships:
hg.add_e((1, 2, 3), {"type": "collaboration", "project": "AI Research"})
```

### 4. Plan for Analysis

```python
# Add metadata that supports your analysis goals
hg.add_e((author1, author2, author3), {
    "type": "research_paper",
    "title": "...",
    "domain": "machine_learning",  # For domain analysis
    "collaboration_type": "international",  # For collaboration analysis
    "funding_source": "NSF",  # For funding analysis
    "impact_score": 8.5  # For impact analysis
})
```
