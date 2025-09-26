# Hypergraph-DB

<div align="center">
  <img src="assets/logo.svg" alt="Hypergraph-DB Logo" width="200"/>
</div>

[![PyPI version](https://img.shields.io/pypi/v/hypergraph-db?color=purple)](https://pypi.org/project/hypergraph-db/)
[![Python](https://img.shields.io/pypi/pyversions/hypergraph-db?color=purple)](https://pypi.org/project/hypergraph-db/)
[![License](https://img.shields.io/github/license/iMoonLab/Hypergraph-DB?color=purple)](https://github.com/iMoonLab/Hypergraph-DB/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/iMoonLab/Hypergraph-DB?color=purple)](https://github.com/iMoonLab/Hypergraph-DB)

Hypergraph-DB is a lightweight, flexible, and Python-based database designed to model and manage **hypergraphs**—a generalized graph structure where edges (hyperedges) can connect any number of vertices. This makes Hypergraph-DB an ideal solution for representing complex relationships between entities in various domains, such as knowledge graphs, social networks, and scientific data modeling.

## ✨ Features

- **🚀 Lightweight & Fast**: Pure Python implementation with minimal dependencies
- **🔗 Hypergraph Support**: Native support for hyperedges connecting multiple vertices
- **💾 Persistence**: Built-in serialization and loading capabilities
- **📊 Visualization**: Interactive hypergraph visualization in web browsers
- **🔍 Flexible Queries**: Rich query capabilities for vertices and hyperedges
- **🛠️ Simple API**: Intuitive and easy-to-use interface

## 🎯 Use Cases

- **Knowledge Graphs**: Model complex relationships between entities
- **Social Networks**: Represent group interactions and multi-party relationships
- **Scientific Data**: Model complex dependencies in research data
- **Recommendation Systems**: Capture multi-way interactions between users, items, and contexts

## 📈 Performance

Hypergraph-DB is designed for efficiency. Here are some performance benchmarks:

| Vertices  | Hyperedges | Add Vertices | Add Edges | Query Time | Total Time |
| --------- | ---------- | ------------ | --------- | ---------- | ---------- |
| 100,000   | 20,000     | 0.12s        | 0.17s     | 0.04s      | 0.58s      |
| 500,000   | 100,000    | 0.85s        | 1.07s     | 0.22s      | 3.34s      |
| 1,000,000 | 200,000    | 1.75s        | 1.82s     | 0.51s      | 6.60s      |

## 🚀 Quick Start

### Installation

```bash
pip install hypergraph-db
```

### Basic Usage

```python
from hyperdb import HypergraphDB

# Create a hypergraph
hg = HypergraphDB()

# Add vertices with attributes
hg.add_v(1, {"name": "Alice", "age": 30})
hg.add_v(2, {"name": "Bob", "age": 25})
hg.add_v(3, {"name": "Charlie", "age": 35})

# Add hyperedges connecting multiple vertices
hg.add_e((1, 2), {"relation": "friends"})
hg.add_e((1, 2, 3), {"relation": "project_team"})

# Query the hypergraph
print(f"Vertices: {hg.all_v}")
print(f"Edges: {hg.all_e}")

# Visualize the hypergraph
hg.draw()  # Opens visualization in web browser
```

## 📚 Documentation

- **[Getting Started](getting-started/installation.md)**: Installation and basic setup
- **[API Reference](api/index.md)**: Complete API documentation
- **[Visualization Guide](visualization/index.md)**: Interactive hypergraph visualization
- **[Examples](examples/basic-usage.md)**: Practical examples and tutorials

## 🤝 Contributing

We welcome contributions! Please see our [GitHub repository](https://github.com/iMoonLab/Hypergraph-DB) for more information.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](about/license.md) file for details.

## 📬 Contact

- **Author**: [Yifan Feng](https://fengyifan.site/)
- **Email**: evanfeng97@qq.com
- **GitHub**: [@iMoonLab](https://github.com/yifanfeng97)

---

*Built with ❤️ by the iMoonLab team*
