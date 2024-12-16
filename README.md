<div align="center" id="top"> 
  <img src="docs/_static/logo.svg" alt="Hyper DB"  width="30%" height="50%" />

  &#xa0;

  <!-- <a href="https://hyperdb.netlify.app">Demo</a> -->
</div>

<h1 align="center">Hypergraph-DB</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/iMoonLab/Hypergraph-DB?color=800080">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/iMoonLab/Hypergraph-DB?color=800080">

  <img alt="PyPI version" src="https://img.shields.io/pypi/v/hypergraph-db?color=purple">
  
  <!-- <img alt="Downloads" src="https://pepy.tech/badge/hypergraph-db?color=purple"> -->

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/iMoonLab/Hypergraph-DB?color=800080">

  <img alt="License" src="https://img.shields.io/github/license/iMoonLab/Hypergraph-DB?color=800080">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/iMoonLab/Hypergraph-DB?color=800080" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/iMoonLab/Hypergraph-DB?color=800080" /> -->

  <img alt="Github stars" src="https://img.shields.io/github/stars/iMoonLab/Hypergraph-DB?color=800080" />
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  Hyper DB 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-installation">Installation</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="#email-contact">Contact</a> &#xa0; | &#xa0;
  <a href="https://github.com/yifanfeng97" target="_blank">Author</a>
</p>

<br>

## :dart: About 

Hypergraph-DB is a lightweight, flexible, and Python-based database designed to model and manage **hypergraphs**—a generalized graph structure where edges (hyperedges) can connect any number of vertices. This makes Hypergraph-DB an ideal solution for representing complex relationships between entities in various domains, such as knowledge graphs, social networks, and scientific data modeling.

Hypergraph-DB provides a high-level abstraction for working with vertices and hyperedges, making it easy to add, update, query, and manage hypergraph data. With built-in support for persistence, caching, and efficient operations, Hypergraph-DB simplifies the management of hypergraph data structures.

**:bar_chart: Performance Test Results**

To demonstrate the performance of **Hypergraph-DB**, let’s consider an example:

- Suppose we want to construct a **hypergraph** with **1,000,000 vertices** and **200,000 hyperedges**.
- Using Hypergraph-DB, it takes approximately:
  - **1.75 seconds** to add **1,000,000 vertices**.
  - **1.82 seconds** to add **200,000 hyperedges**.
- Querying this hypergraph:
  - Retrieving information for **400,000 vertices** takes **0.51 seconds**.
  - Retrieving information for **400,000 hyperedges** takes **2.52 seconds**.

This example demonstrates the efficiency of Hypergraph-DB, even when working with large-scale hypergraphs. Below is a detailed table showing how the performance scales as the size of the hypergraph increases.

**Detailed Performance Results**

The following table shows the results of stress tests performed on Hypergraph-DB with varying scales. The tests measure the time taken to add vertices, add hyperedges, and query vertices and hyperedges.

| **Number of Vertices** | **Number of Hyperedges** | **Add Vertices (s)** | **Add Edges (s)** | **Query Vertices (s/queries)** | **Query Edges (s/queries)** | **Total Time (s)** |
|-------------------------|--------------------------|-----------------------|-------------------|-------------------------------|----------------------------|--------------------|
| 5,000                  | 1,000                   | 0.01                 | 0.01             | 0.00/2,000                   | 0.01/2,000                | 0.02               |
| 10,000                 | 2,000                   | 0.01                 | 0.01             | 0.00/4,000                   | 0.02/4,000                | 0.05               |
| 25,000                 | 5,000                   | 0.03                 | 0.04             | 0.01/10,000                  | 0.05/10,000               | 0.13               |
| 50,000                 | 10,000                  | 0.06                 | 0.07             | 0.02/20,000                  | 0.12/20,000               | 0.26               |
| 100,000                | 20,000                  | 0.12                 | 0.17             | 0.04/40,000                  | 0.24/40,000               | 0.58               |
| 250,000                | 50,000                  | 0.35                 | 0.40             | 0.11/100,000                 | 0.61/100,000              | 1.47               |
| 500,000                | 100,000                 | 0.85                 | 1.07             | 0.22/200,000                 | 1.20/200,000              | 3.34               |
| 1,000,000              | 200,000                 | 1.75                 | 1.82             | 0.51/400,000                 | 2.52/400,000              | 6.60               |

---

**Key Observations:**

1. **Scalability**:  
   Hypergraph-DB scales efficiently with the number of vertices and hyperedges. The time to add vertices and hyperedges grows linearly with the size of the hypergraph.

2. **Query Performance**:  
   Querying vertices and hyperedges remains fast, even for large-scale hypergraphs. For instance:
   - Querying **200,000 vertices** takes only **0.22 seconds**.
   - Querying **200,000 hyperedges** takes only **1.20 seconds**.

3. **Total Time**:  
   The total time to construct and query a hypergraph with **1,000,000 vertices** and **200,000 hyperedges** is only **6.60 seconds**, showcasing the overall efficiency of Hypergraph-DB.

This performance makes **Hypergraph-DB** a great choice for applications requiring fast and scalable hypergraph data management.

---

## :sparkles: Features 

:heavy_check_mark: **Flexible Hypergraph Representation**  
   - Supports vertices (`v`) and hyperedges (`e`), where hyperedges can connect any number of vertices.
   - Hyperedges are represented as sorted tuples of vertex IDs, ensuring consistency and efficient operations.

:heavy_check_mark: **Vertex and Hyperedge Management**  
   - Add, update, delete, and query vertices and hyperedges with ease.
   - Built-in methods to retrieve neighbors, incident edges, and other relationships.

:heavy_check_mark: **Neighbor Queries**  
   - Get neighboring vertices or hyperedges for a given vertex or hyperedge.

:heavy_check_mark: **Persistence**  
   - Save and load hypergraphs to/from disk using efficient serialization (`pickle`).
   - Ensures data integrity and supports large-scale data storage.

:heavy_check_mark: **Customizable and Extensible**  
   - Built on Python’s `dataclasses`, making it easy to extend and customize for specific use cases.

---

## :rocket: Installation 


Hypergraph-DB is a Python library. You can install it directly from PyPI using `pip`.

```bash
pip install hypergraph-db
```

You can also install it by cloning the repository or adding it to your project manually. Ensure you have Python 3.10 or later installed.

```bash
# Clone the repository
git clone https://github.com/iMoonLab/Hypergraph-DB.git
cd Hypergraph-DB

# Install dependencies (if any)
pip install -r requirements.txt
```

---

## :checkered_flag: Starting 

This section provides a quick guide to get started with Hypergraph-DB, including iusage, and running basic operations. Below is an example of how to use Hypergraph-DB, based on the provided test cases.

#### **1. Create a Hypergraph**

```python
from hyperdb import HypergraphDB

# Initialize the hypergraph
hg = HypergraphDB()

# Add vertices
hg.add_v(1, {"name": "Alice"})
hg.add_v(2, {"name": "Bob"})
hg.add_v(3, {"name": "Charlie"})

# Add hyperedges
hg.add_e((1, 2), {"relation": "knows"})
hg.add_e((1, 3, 2), {"relation": "collaborates"})
```

#### **2. Query Vertices and Hyperedges**

```python
# Get all vertices and hyperedges
print(hg.all_v)  # Output: {1, 2, 3}
print(hg.all_e)  # Output: {(1, 2), (1, 2, 3)}

# Query a specific vertex
print(hg.v(1))  # Output: {'name': 'Alice'}

# Query a specific hyperedge
print(hg.e((1, 2)))  # Output: {'relation': 'knows'}
```

#### **3. Update and Remove Vertices/Hyperedges**

```python
# Update a vertex
hg.update_v(1, {"name": "Alice Smith"})
print(hg.v(1))  # Output: {'name': 'Alice Smith'}

# Remove a vertex
hg.remove_v(2)
print(hg.all_v)  # Output: {1, 3}
print(hg.all_e)  # Output: {(1, 3)}

# Remove a hyperedge
hg.remove_e((1, 3))
print(hg.all_e)  # Output: set()
```

#### **4. Calculate Degrees**

```python
# Get the degree of a vertex
print(hg.degree_v(1))  # Output: 1

# Get the degree of a hyperedge
print(hg.degree_e((1, 2)))  # Output: 2
```

#### **5. Neighbor Queries**

```python
# Get neighbors of a vertex
hg.add_e((1, 3, 4), {"relation": "team"})
print(hg.nbr_v(1))  # Output: {3, 4}

# Get incident hyperedges of a vertex
print(hg.nbr_e_of_v(1))  # Output: {(1, 3, 4)}
```

#### **6. Persistence (Save and Load)

```python
# Save the hypergraph to a file
hg.save("my_hypergraph.hgdb")

# Load the hypergraph from a file
hg2 = HypergraphDB(storage_file="my_hypergraph.hgdb")
print(hg2.all_v)  # Output: {1, 3, 4}
print(hg2.all_e)  # Output: {(1, 3, 4)}
```


--- 


## :memo: License 

Hypergraph-DB is open-source and licensed under the [Apache License 2.0](LICENSE). Feel free to use, modify, and distribute it as per the license terms.


---

## :email: Contact 

Hypergraph-DB is maintained by [iMoon-Lab](http://moon-lab.tech/), Tsinghua University. If you have any questions, please feel free to contact us via email: [Yifan Feng](mailto:evanfeng97@gmail.com).


Made with :heart: by <a href="https://github.com/yifanfeng97" target="_blank">Yifan Feng</a>

&#xa0;

<a href="#top">Back to top</a>


