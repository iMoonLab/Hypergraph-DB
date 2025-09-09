# Interface Guide

The Hypergraph-DB visualization interface provides an intuitive web-based interface for exploring hypergraph data. This guide covers all interface components and their functionality.

## 🚀 Quick Start

To launch the visualization interface:

```python
import hyperdb
hg = hyperdb.HypergraphDB()
# Add your data...
hg.draw()  # Opens web interface at http://localhost:8080
```

## 📋 Interface Layout

The visualization interface consists of three main areas:

### 🏠 Top Header

| � **Section** | 🎯 **Function** | � **Description** |
|-----------|-----------|----------|
| **Logo & Title** | Brand Identity | "Hypergraph Visualization" title |
| **Database Info** | Statistics Card | Shows vertex and edge counts |
| **Search Bar** | Global Search | Find vertices by ID, type, or description |

**Database Information Display:**
```yaml
Database: "current_hypergraph"
Vertices: "1,234 vertices"  
Hyperedges: "567 hyperedges"
```

### 🔍 Search Functionality

- **Search by ID**: Enter vertex identifier
- **Search by Type**: Find vertices by entity type (PERSON, CONCEPT, etc.)
- **Search by Description**: Full-text search in descriptions
- **Real-time Results**: Updates as you type

## 📋 Left Sidebar - Vertex Explorer

### Vertex List Features

```text
🎯 Vertex Browser
├── 📊 Sorted by Degree (High to Low)
├── 🏷️ Entity Type Indicators
│   ├── � PERSON (teal color)
│   ├── � CONCEPT (purple color) 
│   ├── � ORGANIZATION (orange color)
│   ├── � LOCATION (green color)
│   └── ⚡ EVENT, PRODUCT (other colors)
├── � Degree Display (connection count)
└── � Description Preview (truncated to 100 chars)
```

### Vertex Card Information

Each vertex displays:
- **ID**: Unique identifier
- **Type Badge**: Color-coded entity type
- **Degree**: Number of connections
- **Description**: Brief text preview

### Interactive Features

- **🖱️ Click**: Select vertex and load its subgraph
- **� Search**: Filter vertices in real-time
- **� Auto-sort**: Ordered by connection degree
- **�️ Preview**: Hover to see full information

## 🎨 Main Canvas - Graph Visualization

### Visualization Modes

| 🎭 **Mode** | 📝 **Description** | 🎯 **Best For** |
|-----------|-----------|----------|
| **Hypergraph Mode** | Shows true hyperedge structure | Complex multi-way relationships |
| **Graph Mode** | Traditional node-link display | Simple binary relationships |

### Graph Elements

#### 🎯 Vertex Rendering

```javascript
// Vertex visual properties based on entity type
const vertexColors = {
  PERSON: "#00C9C9",      // Teal
  CONCEPT: "#a680ff",     // Purple  
  ORGANIZATION: "#F08F56", // Orange
  LOCATION: "#16f69c",    // Green
  EVENT: "#004ac9",       // Blue
  PRODUCT: "#f056d1"      // Pink
}

// Size scaled by degree (connections)
nodeSize = Math.max(8, Math.min(32, degree * 2))
```

#### 🔗 Hyperedge Display

```javascript
// Hyperedge visualization options
const edgeStyles = {
  // Binary edges (2 vertices)
  binary: {
    stroke: "#8b5cf6",
    strokeWidth: 2,
    strokeDasharray: null
  },
  
  // Multi-way hyperedges (3+ vertices)  
  multiway: {
    stroke: "#8b5cf6",
    strokeWidth: 3,
    strokeDasharray: "5,5"
  }
}
```

### Interactive Controls

| 🎮 **Control** | 🖱️ **Action** | 🎯 **Function** |
|-----------|-----------|----------|
| **Mouse Wheel** | Scroll | Zoom in/out |
| **Mouse Drag** | Left click + drag | Pan canvas |
| **Node Click** | Left click | Select/deselect vertex |
| **Node Hover** | Mouse over | Show vertex tooltip |
| **Canvas Click** | Click empty space | Clear selection |

### Layout Algorithms

The interface uses force-directed layout with these features:
- **Automatic positioning** based on graph structure
- **Collision detection** prevents node overlap  
- **Smooth animations** for layout changes
- **Responsive design** adapts to different screen sizes

## 📊 Right Panel - Vertex Details

### Information Display

When a vertex is selected, the right panel shows:

#### Basic Properties
```yaml
Vertex Details:
  ID: "person_123"
  Type: "PERSON"  
  Degree: 8 connections
  Description: "Full description text..."
```

#### Connection Analysis
- **Direct neighbors**: List of connected vertices
- **Hyperedge participation**: Which hyperedges contain this vertex
- **Connection statistics**: Degree distribution and patterns

#### Subgraph Visualization
- **Local view**: Shows vertex and its immediate neighborhood
- **Hyperedge structure**: Displays all hyperedges containing the vertex
- **Interactive exploration**: Click neighbors to explore further

## 🎛️ Control Options

### Visualization Mode Toggle

Switch between visualization modes:

```javascript
// Toggle between hypergraph and graph modes
const modes = {
  hyper: "Show true hyperedge structure",
  graph: "Traditional node-link display"  
}
```

### Loading States

The interface provides visual feedback:
- **Loading spinner** while processing large datasets
- **Error messages** for connection or data issues
- **Progress indicators** for long operations

## 🎨 Visual Themes

### Color Schemes

| 🎨 **Entity Type** | 🌈 **Color** | 🔍 **Hex Code** |
|-----------|-----------|----------|
| **PERSON** | Teal | `#00C9C9` |
| **CONCEPT** | Purple | `#a680ff` |
| **ORGANIZATION** | Orange | `#F08F56` |  
| **LOCATION** | Green | `#16f69c` |
| **EVENT** | Blue | `#004ac9` |
| **PRODUCT** | Pink | `#f056d1` |

### Responsive Design

The interface adapts to different screen sizes:

```text
Screen Breakpoints:
├── 📱 Mobile (< 768px): Stacked layout
├── 📟 Tablet (768-1024px): Sidebar toggle  
└── 🖥️ Desktop (> 1024px): Full three-panel layout
```

## 🚀 Performance Features

### Optimizations

- **Lazy loading**: Only renders visible elements
- **Virtual scrolling**: Efficient handling of large vertex lists
- **Canvas optimization**: WebGL-accelerated rendering via G6
- **Data streaming**: Progressive loading for large datasets

### Browser Compatibility

- **Modern browsers**: Chrome, Firefox, Safari, Edge
- **WebGL support**: Required for optimal performance
- **Responsive design**: Works on mobile and desktop

## ⚡ Keyboard Shortcuts

| ⌨️ **Shortcut** | 🎯 **Function** |
|-----------|----------|
| `Ctrl/Cmd + C` | Stop visualization server |
| `F` | Fit graph to screen |
| `Escape` | Clear selection |
| `Space` | Center graph |
| `+/-` | Zoom in/out |

---

Ready to explore? Check out our [Basic Operations](basic-operations.md) guide to start interacting with your hypergraph data!
