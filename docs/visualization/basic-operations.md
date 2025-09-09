# Basic Operations Guide

This guide will help you master the basic operations of the hypergraph visualization interface.

## 🖱️ Mouse Operations

### Basic Interactions

| 🎯 **Operation** | 📝 **Description** | 💡 **Tips** |
|------------|-----------|----------|
| **Left Click** | Select vertex or hyperedge | Click empty area to deselect |
| **Left Drag** | Move view | Hold and drag to pan entire graph |
| **Right Click** | Open context menu | Quick access to common functions |
| **Mouse Hover** | Show detailed information | Hover over elements to view properties |

### Zoom Operations

```javascript
// Mouse wheel zoom
Scroll Up = Zoom in
Scroll Down = Zoom out

// Keyboard shortcuts
Ctrl + Mouse Wheel = Fine zoom control
Ctrl + 0 = Reset zoom
```

## ⌨️ Keyboard Shortcuts

### Navigation Shortcuts

| 🔑 **Key** | ⚡ **Function** | 📋 **Description** |
|-----------|-----------|----------|
| `Space` | Pan mode | Hold spacebar and drag to move view |
| `F` | Fit to window | Auto-adjust view to show all content |
| `R` | Reset view | Return to initial view state |
| `Ctrl + F` | Search | Open search box to find specific elements |

### Selection Shortcuts

| 🔑 **Key** | ⚡ **Function** | 📋 **Description** |
|-----------|-----------|----------|
| `Ctrl + A` | Select all | Select all visible elements |
| `Ctrl + Click` | Multi-select | Add or remove elements from selection |
| `Shift + Click` | Range select | Select all elements between two elements |
| `Esc` | Clear selection | Clear current selection |

## 🎯 Element Selection

### Vertex Selection

```python
# Create vertices with different types
hg.add_v("person_1", {"name": "Alice", "type": "Person", "age": 30})
hg.add_v("project_1", {"name": "AI Research", "type": "Project"})
hg.add_v("skill_1", {"name": "Machine Learning", "type": "Skill"})
```

**Selection Effects**:
- ✨ **Highlight**: Selected vertices change color
- 📊 **Info Panel**: Detailed properties shown on the right
- 🔗 **Associated Display**: Related hyperedges are also highlighted

### Hyperedge Selection

```python
# Create different types of hyperedges
hg.add_e(("person_1", "project_1"), {"relation": "leads", "start_date": "2024-01-01"})
hg.add_e(("person_1", "project_1", "skill_1"), {"relation": "applies_skill_in_project"})
```

**Selection Effects**:
- 🎨 **Edge Highlight**: Selected hyperedges become bold or change color
- 📋 **Relationship Info**: Shows hyperedge properties and connected vertices
- 🎯 **Endpoint Emphasis**: Connected vertices are also highlighted

## 🔍 View Navigation

### Zoom Levels

```text
🔍 Zoom Level Description:
├── 25% - Ultra wide view, suitable for overall overview
├── 50% - Wide view, for viewing large-scale structure
├── 100% - Standard view, default display level
├── 200% - Magnified view, for viewing details
└── 400% - Ultra magnified view, editing mode
```

### Auto Layout

The system provides multiple layout algorithms:

| 🎨 **Layout Type** | 📝 **Use Case** | ⚙️ **Features** |
|---------------|--------------|----------|
| **Force-directed** | General purpose | Natural distribution, good aesthetics |
| **Circular** | Small-scale data | Circular arrangement, clear structure |
| **Hierarchical** | Hierarchical data | Tree structure, clear levels |
| **Grid** | Regular data | Grid arrangement, neat alignment |

## 📊 Information Viewing

### Hover Tooltips

Hovering the mouse over any element shows:

```yaml
Vertex Information:
  - Unique identifier
  - All property key-value pairs
  - Number of connected hyperedges
  - Neighbor vertex statistics

Hyperedge Information:
  - List of connected vertices
  - Relationship type and properties
  - Weight and strength
  - Metadata like creation time
```

### Details Panel

After selecting an element, the right panel shows complete information:

- **🔍 Basic Info**: ID, type, label
- **📋 Property List**: All key-value pairs
- **🔗 Relationship Network**: Connected other elements
- **📊 Statistics**: Degree, centrality and other metrics

## 🎛️ Toolbar Functions

### Main Toolbar

```text
🧰 Toolbar Layout:
┌─────────────────────────────────────┐
│ [🏠] [🔍] [⚙️] [📁] [💾] [❓]    │
└─────────────────────────────────────┘
  │    │    │    │    │    │
  │    │    │    │    │    └─ Help
  │    │    │    │    └─ Export data
  │    │    │    └─ Load data
  │    │    └─ Settings panel
  │    └─ Search function
  └─ Return to home
```

### Secondary Toolbar

| 🔧 **Tool** | 📝 **Function** | 🎯 **Purpose** |
|-----------|-----------|----------|
| 🎨 **Style** | Change colors and sizes | Personalized display |
| 📏 **Measure** | Calculate distances and paths | Analysis tools |
| 🔍 **Filter** | Hide specific elements | Simplify view |
| 📸 **Screenshot** | Save current view | Sharing and recording |

## 💡 Operation Tips

### Efficient Navigation

1. **Quick Locate**: Use search function to quickly find specific elements
2. **Smart Zoom**: Double-click elements to auto-zoom to appropriate level
3. **Context Switching**: Right-click menu provides quick operations
4. **Batch Operations**: Use multi-select for batch processing

### Performance Optimization

```python
# Tips for large dataset visualization
viewer = hg.get_viewer()

# Show only vertices with high degree
viewer.filter_by_degree(min_degree=3)

# Limit display count
viewer.limit_vertices(max_count=100)

# Enable LOD (Level of Detail)
viewer.enable_lod(True)
```

---

After mastering these basic operations, you can efficiently use the hypergraph visualization features! Next, learn about the [Interface Guide](interface-guide.md) to deeply understand each functional area.
