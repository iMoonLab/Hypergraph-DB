<div align="center" id="top"> 
  <img src="docs/_static/logo.svg" alt="Hyper DB"  width="30%" height="50%" />

  &#xa0;

  <!-- <a href="https://hyperdb.netlify.app">Demo</a> -->
</div>

<h1 align="center">Hyper-DB</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/iMoonLab/Hyper-DB?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/iMoonLab/Hyper-DB?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/iMoonLab/Hyper-DB?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/iMoonLab/Hyper-DB?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/iMoonLab/Hyper-DB?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/iMoonLab/Hyper-DB?color=56BEB8" /> -->

  <img alt="Github stars" src="https://img.shields.io/github/stars/iMoonLab/Hyper-DB?color=56BEB8" />
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

## :dart: About ##

Hyper-DB is a lightweight, flexible, and Python-based database designed to model and manage **hypergraphs**—a generalized graph structure where edges (hyperedges) can connect any number of vertices. This makes Hyper-DB an ideal solution for representing complex relationships between entities in various domains, such as knowledge graphs, social networks, and scientific data modeling.

Hyper-DB provides a high-level abstraction for working with vertices and hyperedges, making it easy to add, update, query, and manage hypergraph data. With built-in support for persistence, caching, and efficient operations, Hyper-DB simplifies the management of hypergraph data structures.

---

## :sparkles: Features ##

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

## :rocket: Installation ##


Hyper-DB is a Python library. You can install it directly from PyPI using `pip`.

```bash
pip install Hyper-DB
```

You can also install it by cloning the repository or adding it to your project manually. Ensure you have Python 3.10 or later installed.

```bash
# Clone the repository
git clone https://github.com/iMoonLab/Hyper-DB.git
cd Hyper-DB

# Install dependencies (if any)
pip install -r requirements.txt
```

---

## :checkered_flag: Starting ##

This section provides a quick guide to get started with Hyper-DB, including iusage, and running basic operations. Below is an example of how to use Hyper-DB, based on the provided test cases.

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

#### **6. Persistence (Save and Load)**

```python
# Save the hypergraph to a file
hg.save("my_hypergraph.hgdb")

# Load the hypergraph from a file
hg2 = HypergraphDB(storage_file="my_hypergraph.hgdb")
print(hg2.all_v)  # Output: {1, 3, 4}
print(hg2.all_e)  # Output: {(1, 3, 4)}
```


--- 


## :memo: License ##

Hyper-DB is open-source and licensed under the [Apache License 2.0](LICENSE). Feel free to use, modify, and distribute it as per the license terms.


---

## :email: Contact ##

Hyper-DB is maintained by [iMoon-Lab](http://moon-lab.tech/), Tsinghua University. If you have any questions, please feel free to contact us via email: [Yifan Feng](mailto:evanfeng97@gmail.com).


Made with :heart: by <a href="https://github.com/yifanfeng97" target="_blank">Yifan Feng</a>

&#xa0;

<a href="#top">Back to top</a>


