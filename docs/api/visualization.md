# Visualization

Hypergraph-DB provides built-in visualization capabilities through web-based interactive displays.

## HypergraphViewer Class

::: hyperdb.draw.HypergraphViewer
    options:
      show_root_heading: true
      show_source: true
      members_order: source
      show_if_no_docstring: true

## Usage Example

```python
from hyperdb import HypergraphDB

# Create and populate hypergraph
hg = HypergraphDB()
hg.add_v(1, {"name": "Alice"})
hg.add_v(2, {"name": "Bob"})
hg.add_v(3, {"name": "Charlie"})

hg.add_e((1, 2), {"relation": "friends"})
hg.add_e((1, 2, 3), {"relation": "team"})

# Visualize - opens in browser
hg.draw()
```

## Visualization Features

- **Interactive Display**: Click and drag to explore the hypergraph structure
- **Vertex Information**: Hover over vertices to see their attributes
- **Hyperedge Visualization**: Visual representation of multi-way connections
- **Web-based**: Runs in your default web browser
- **Real-time Updates**: Reflects current hypergraph state

## Customization

The visualization can be customized by modifying the HTML template located in:
```
hyperdb/templates/hypergraph_viewer.html
```

### Available Options

When calling `draw()`, you can specify:

- `port`: Port number for the web server (default: 8080)
- `open_browser`: Whether to automatically open the browser (default: True)

```python
# Use custom port
hg.draw(port=9000)

# Don't automatically open browser
hg.draw(open_browser=False)
```

## Technical Details

The visualization system:

1. **Converts** hypergraph data to JSON format
2. **Generates** HTML with embedded data and D3.js visualization
3. **Starts** a local web server
4. **Opens** the visualization in your default browser

The visualization uses:
- **D3.js** for interactive graphics
- **Local HTTP server** for serving content
- **JSON data embedding** for efficient data transfer

## Troubleshooting

### Common Issues

**Port already in use:**
```python
# Try a different port
hg.draw(port=8081)
```

**Browser doesn't open:**
- Manually navigate to `http://localhost:8080` (or your specified port)
- Check firewall settings

**Visualization appears empty:**
- Ensure your hypergraph has vertices and edges
- Check browser console for JavaScript errors

### Performance Considerations

- Large hypergraphs (>1000 vertices) may render slowly
- Consider filtering or sampling for very large datasets
- The visualization loads all data into browser memory

## Future Enhancements

Planned improvements include:

- **Export capabilities** (PNG, SVG, PDF)
- **Layout algorithms** for better visualization
- **Filtering options** for large graphs
- **Custom styling** and themes
- **Interactive editing** capabilities
