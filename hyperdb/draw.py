import os
import webbrowser
import threading
import json
from pathlib import Path
from typing import Dict, Any
import http.server
import socketserver
from urllib.parse import urlparse

from .hypergraph import HypergraphDB


class HypergraphViewer:
    """Hypergraph visualization tool"""
    
    def __init__(self, hypergraph_db: HypergraphDB, port: int = 8080):
        self.hypergraph_db = hypergraph_db
        self.port = port
        self.html_content = self._generate_html_with_data()
        
    def _generate_html_with_data(self):
        """Generate HTML content with embedded data"""
        # Get all data
        database_info = {
            "name": "current_hypergraph",
            "vertices": self.hypergraph_db.num_v,
            "edges": self.hypergraph_db.num_e
        }
        
        # Get vertex list
        vertices = list(self.hypergraph_db.all_v)[:100]
        vertex_data = []
        
        for v_id in vertices:
            v_data = self.hypergraph_db.v(v_id, {})
            vertex_data.append({
                "id": v_id,
                "degree": self.hypergraph_db.degree_v(v_id),
                "entity_type": v_data.get("entity_type", ""),
                "description": v_data.get("description", "")[:100] + "..." if len(v_data.get("description", "")) > 100 else v_data.get("description", "")
            })
        
        # Sort by degree
        vertex_data.sort(key=lambda x: x["degree"], reverse=True)
        
        # Get graph data for all vertices
        graph_data = {}
        for vertex in vertex_data:
            vertex_id = vertex["id"]
            graph_data[vertex_id] = self._get_vertex_neighbor_data(self.hypergraph_db, vertex_id)
        
        # Embed data into HTML
        return self._get_html_template(database_info, vertex_data, graph_data)
    

    def _get_vertex_neighbor_data(self, hypergraph_db: HypergraphDB, vertex_id: str) -> Dict[str, Any]:
        """Get vertex neighbor data"""
        hg = hypergraph_db
        
        if not hg.has_v(vertex_id):
            raise ValueError(f"Vertex {vertex_id} not found")
        
        # Get all neighbor hyperedges of the vertex
        neighbor_edges = hg.nbr_e_of_v(vertex_id)
        
        # Collect all related vertices
        all_vertices = {vertex_id}
        edges_data = {}
        
        for edge_tuple in neighbor_edges:
            # Add all vertices in the hyperedge
            all_vertices.update(edge_tuple)
            
            # Get hyperedge data
            edge_data = hg.e(edge_tuple, {})
            edge_key = "|#|".join(str(item) for item in edge_tuple)
            edges_data[edge_key] = {
                "keywords": edge_data.get("keywords", ""),
                "summary": edge_data.get("summary", ""),
                "weight": len(edge_tuple)  # Hyperedge weight equals the number of vertices it contains
            }
        
        # Get data for all vertices
        vertices_data = {}
        for v_id in all_vertices:
            v_data = hg.v(v_id, {})
            vertices_data[v_id] = {
                "entity_name": v_data.get("entity_name", v_id),
                "entity_type": v_data.get("entity_type", ""),
                "description": v_data.get("description", ""),
                "additional_properties": v_data.get("additional_properties", "")
            }
        
        return {
            "vertices": vertices_data,
            "edges": edges_data
        }
    
    def _get_html_template(self, database_info: Dict, vertex_data: list, graph_data: Dict) -> str:
        """Get HTML template with embedded data"""
        # Serialize data to JSON string
        embedded_data = {
            "database": database_info,
            "vertices": vertex_data,
            "graphs": graph_data
        }
        data_json = json.dumps(embedded_data, ensure_ascii=False)
        
        # Read HTML template file
        template_path = Path(__file__).parent / "templates" / "hypergraph_viewer.html"
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_template = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"HTML template file not found: {template_path}")
        
        # Replace placeholders in template
        html_content = html_template.replace("{{DATA_JSON}}", data_json)
        
        return html_content

    def start_server(self, open_browser: bool = True):
        """Start simple HTTP server"""
        
        class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
            def __init__(self, html_content, *args, **kwargs):
                self.html_content = html_content
                super().__init__(*args, **kwargs)
                
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(self.html_content.encode('utf-8'))
                
            def log_message(self, format, *args):
                # Disable log output
                pass
        
        def run_server():
            handler = lambda *args, **kwargs: CustomHTTPRequestHandler(self.html_content, *args, **kwargs)
            with socketserver.TCPServer(("127.0.0.1", self.port), handler) as httpd:
                httpd.serve_forever()
        
        # Start server in new thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        if open_browser:
            # Wait for server to start
            import time
            time.sleep(1)
            
            # Open browser
            url = f"http://127.0.0.1:{self.port}"
            print(f"🚀 Hypergraph visualization server started: {url}")
            webbrowser.open(url)
        
        return server_thread


def draw_hypergraph(hypergraph_db: HypergraphDB, port: int = 8080, open_browser: bool = True):
    """
    Main function to draw hypergraph
    
    Args:
        hypergraph_db: HypergraphDB instance
        port: Server port
        open_browser: Whether to automatically open browser
    
    Returns:
        HypergraphViewer instance
    """
    print("🎨 Starting hypergraph visualization...")
    print(f"📁 Vertices: {hypergraph_db.num_v}, Hyperedges: {hypergraph_db.num_e}")
    
    viewer = HypergraphViewer(hypergraph_db=hypergraph_db, port=port)
    
    # Start server
    server_thread = viewer.start_server(open_browser=open_browser)
    
    try:
        print("⌨️  Press Ctrl+C to stop server")
        # Keep main thread running
        server_thread.join()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    
    return viewer


# Convenience function
def draw(hypergraph_db: HypergraphDB, port: int = 8899):
    """
    Convenient hypergraph drawing function
    
    Args:
        hypergraph_db: HypergraphDB instance
        port: Server port
    """
    return draw_hypergraph(hypergraph_db, port, True)

