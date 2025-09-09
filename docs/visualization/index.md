# Visualization Guide

Hypergraph-DB provides powerful interactive visualization capabilities to help you intuitively explore and understand hypergraph data structures.

## 🎨 Visualization Overview

<div align="center">
  <img src="../assets/vis_hg.jpg" alt="Hypergraph Visualization" width="800"/>
</div>

### ✨ Core Features

- **🌐 Interactive Web Interface**: Real-time visualization based on modern browsers
- **🔍 Multi-level Exploration**: Seamless switching from global views to local details
- **📊 Smart Layout**: Adaptive graph layout algorithms
- **🎯 Real-time Data**: Direct reflection of current hypergraph state
- **📱 Responsive Design**: Support for desktop and mobile devices

## 🚀 Quick Start

### Basic Usage

```python
from hyperdb import HypergraphDB

# Create hypergraph
hg = HypergraphDB()

# Add data
hg.add_v(1, {"name": "Alice", "type": "Person"})
hg.add_v(2, {"name": "Bob", "type": "Person"}) 
hg.add_v(3, {"name": "Project A", "type": "Project"})

# Add hyperedges
hg.add_e((1, 2), {"relation": "friends"})
hg.add_e((1, 2, 3), {"relation": "collaboration"})

# Launch visualization
hg.draw()  # Automatically opens browser
```

### Visualization Configuration

```python
# Custom port
hg.draw(port=8888)

# Generate HTML without opening browser
viewer = hg.get_viewer(auto_open=False)
html_content = viewer.get_html()
```

## 📚 Detailed Feature Guide

| 📖 **Section** | 📋 **Content** |
|------------|-----------|
| [Basic Operations](basic-operations.md) | Navigation, zooming, selection and other basic operations |
| [Interface Guide](interface-guide.md) | Detailed description of user interface components |
| [Advanced Customization](advanced-customization.md) | Advanced customization options and techniques |

## 🎯 Use Cases

### 📊 Data Exploration
- **Relationship Analysis**: Understanding complex multi-way relationships
- **Pattern Discovery**: Identifying important patterns in data
- **Anomaly Detection**: Finding outliers in data

### 📈 Research Applications
- **Social Networks**: Analyzing multi-person group interactions
- **Knowledge Graphs**: Visualizing complex relationships between concepts
- **Biological Networks**: Displaying protein interaction networks

### 🎓 Teaching and Demonstration
- **Algorithm Visualization**: Showing graph algorithm execution
- **Concept Explanation**: Intuitive explanation of hypergraph theory
- **Case Studies**: Demonstration of real-world applications

## 🔧 Technical Architecture

### Frontend Technology Stack
- **React 18**: Modern user interface
- **G6 Graph Library**: Professional graph visualization engine
- **Tailwind CSS**: Elegant styling system

### Backend Integration
- **Python HTTP Server**: Lightweight local server
- **JSON Data Transfer**: Efficient data exchange format
- **Real-time Sync**: Instant reflection of data changes

## 📱 Browser Compatibility

| 🌐 **Browser** | ✅ **Supported Version** | 📋 **Notes** |
|-------------|--------------|----------|
| Chrome | 90+ | Recommended, best performance |
| Firefox | 88+ | Fully supported |
| Safari | 14+ | Fully supported |
| Edge | 90+ | Fully supported |

## 🚨 Important Notes

### Performance Considerations
- **Large-scale Data**: For more than 1000 vertices, filtering is recommended
- **Memory Usage**: Visualization consumes browser memory
- **Network Ports**: Ensure specified port is not occupied

### Security Reminders
- **Local Server**: For local development only, not recommended for public exposure
- **Data Sensitivity**: Visualization displays all data in browser

---

Ready to start exploring the visual world of hypergraphs? Begin your visualization journey with the [Basic Operations Guide](basic-operations.md)!
