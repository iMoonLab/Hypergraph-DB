import http.server
import json
import os
import socketserver
import threading
import webbrowser
from pathlib import Path
from typing import Any, Dict
from urllib.parse import parse_qs, urlparse

from .hypergraph import HypergraphDB


class HypergraphAPIHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler with API endpoints"""

    def __init__(self, hypergraph_db: HypergraphDB, *args, **kwargs):
        self.hypergraph_db = hypergraph_db
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        """Disable default logging"""
        pass

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        # CORS headers
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        # Route handling
        if path == "/" or path == "/index.html":
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self._get_html_template().encode("utf-8"))

        elif path == "/api/database/info":
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            response = self._get_database_info()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/vertices":
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()

            # Parse query parameters
            page = int(query_params.get("page", ["1"])[0])
            page_size = int(query_params.get("page_size", ["50"])[0])
            search = query_params.get("search", [""])[0]
            sort_by = query_params.get("sort_by", ["degree"])[0]
            sort_order = query_params.get("sort_order", ["desc"])[0]

            response = self._get_vertices(page, page_size, search, sort_by, sort_order)
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))

        elif path == "/api/graph":
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()

            vertex_id = query_params.get("vertex_id", [""])[0]
            if vertex_id:
                response = self._get_graph_data(vertex_id)
            else:
                response = {"error": "vertex_id parameter is required"}

            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))

        else:
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _get_database_info(self) -> Dict[str, Any]:
        """Get database information"""
        return {
            "name": "current_hypergraph",
            "vertices": self.hypergraph_db.num_v,
            "edges": self.hypergraph_db.num_e,
        }

    def _get_vertices(self, page: int, page_size: int, search: str, sort_by: str, sort_order: str) -> Dict[str, Any]:
        """Get vertices with pagination and search"""
        hg = self.hypergraph_db

        # Get all vertices
        all_vertices = list(hg.all_v)

        # Prepare vertex data with search scoring
        vertex_data = []
        search_lower = search.lower() if search else ""

        for v_id in all_vertices:
            v_data = hg.v(v_id, {})
            degree = hg.degree_v(v_id)
            entity_type = v_data.get("entity_type", "")
            description = v_data.get("description", "")

            # Calculate search score
            score = 0
            if search_lower:
                if search_lower in str(v_id).lower():
                    score += 3
                if search_lower in entity_type.lower():
                    score += 2
                if search_lower in description.lower():
                    score += 1

                # Skip if no match
                if score == 0:
                    continue

            vertex_data.append(
                {
                    "id": v_id,
                    "degree": degree,
                    "entity_type": entity_type,
                    "description": (description[:100] + "..." if len(description) > 100 else description),
                    "score": score,
                }
            )

        # Sort vertices
        if search_lower:
            # Sort by search score if searching (no degree filtering)
            vertex_data.sort(key=lambda x: x["score"], reverse=True)
        elif sort_by == "degree":
            # First, separate by degree threshold (degree > 50 goes to the end)
            vertex_data.sort(key=lambda x: (x["degree"] > 50, -x["degree"] if sort_order == "desc" else x["degree"]))
        elif sort_by == "id":
            # First, separate by degree threshold (degree > 50 goes to the end)
            vertex_data.sort(key=lambda x: (x["degree"] > 50, str(x["id"])), reverse=(sort_order == "desc"))

        # Remove score from output
        for v in vertex_data:
            v.pop("score", None)

        # Pagination
        total = len(vertex_data)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_data = vertex_data[start:end]

        return {
            "data": paginated_data,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size,
            },
        }

    def _get_graph_data(self, vertex_id: str) -> Dict[str, Any]:
        """Get graph data for a vertex"""
        hg = self.hypergraph_db

        if not hg.has_v(vertex_id):
            return {"error": f"Vertex {vertex_id} not found"}

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
                "weight": len(edge_tuple),
                **edge_data,
            }

        # Get data for all vertices
        vertices_data = {}
        for v_id in all_vertices:
            v_data = hg.v(v_id, {})
            vertices_data[v_id] = {
                "entity_name": v_data.get("entity_name", v_id),
                "entity_type": v_data.get("entity_type", ""),
                "description": v_data.get("description", ""),
                "additional_properties": v_data.get("additional_properties", ""),
            }

        return {"vertices": vertices_data, "edges": edges_data}

    def _get_html_template(self) -> str:
        """Get HTML template without embedded data"""
        template_path = Path(__file__).parent / "templates" / "hypergraph_viewer.html"

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                html_template = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"HTML template file not found: {template_path}")

        # Replace placeholder with empty object (data will be loaded via API)
        html_content = html_template.replace("{{DATA_JSON}}", "{}")

        return html_content


class HypergraphViewer:
    """Hypergraph visualization tool"""

    def __init__(self, hypergraph_db: HypergraphDB, port: int = 8080):
        self.hypergraph_db = hypergraph_db
        self.port = port

    def start_server(self, open_browser: bool = True):
        """Start HTTP server with API endpoints"""

        def run_server():
            handler = lambda *args, **kwargs: HypergraphAPIHandler(self.hypergraph_db, *args, **kwargs)
            self.httpd = socketserver.TCPServer(("127.0.0.1", self.port), handler)
            self.httpd.serve_forever()

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

    def stop_server(self):
        """Stop the HTTP server"""
        if hasattr(self, "httpd"):
            self.httpd.shutdown()
            self.httpd.server_close()


def draw_hypergraph(hypergraph_db: HypergraphDB, port: int = 8080, open_browser: bool = True, blocking: bool = True):
    """
    Main function to draw hypergraph

    Args:
        hypergraph_db: HypergraphDB instance
        port: Server port
        open_browser: Whether to automatically open browser
        blocking: Whether to block main thread. If False, returns immediately.

    Returns:
        HypergraphViewer instance
    """
    import signal
    import sys

    print("🎨 Starting hypergraph visualization...")
    print(f"📁 Vertices: {hypergraph_db.num_v}, Hyperedges: {hypergraph_db.num_e}")

    viewer = HypergraphViewer(hypergraph_db=hypergraph_db, port=port)

    # Start server
    server_thread = viewer.start_server(open_browser=open_browser)

    if not blocking:
        print(f"🚀 Server started in non-blocking mode on port {port}")
        print("💡 Use viewer.stop_server() to stop the server manually")
        return viewer

    def signal_handler(sig, frame):
        print("\n🛑 Server stopping...")
        viewer.stop_server()
        sys.exit(0)

    # Register signal handler for Windows and Unix
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, signal_handler)

    try:
        print("⌨️  Press Ctrl+C to stop server")

        # For Windows compatibility - use a polling loop instead of join()
        import time

        while server_thread.is_alive():
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        viewer.stop_server()

    return viewer


# Convenience function
def draw(hypergraph_db: HypergraphDB, port: int = 8899, blocking: bool = True):
    """
    Convenient hypergraph drawing function

    Args:
        hypergraph_db: HypergraphDB instance
        port: Server port
        blocking: Whether to block main thread
    """
    return draw_hypergraph(hypergraph_db, port, True, blocking)
