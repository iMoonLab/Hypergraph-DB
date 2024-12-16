import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import time
import random
import logging

from hyperdb.hypergraph import HypergraphDB


# Configure log directory and file
log_root = Path(__file__).parent / "logs"
if not log_root.exists():
    log_root.mkdir()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_root / "stress_test.log",
    filemode="w",
)
logger = logging.getLogger(__name__)


def add_vertices(hg, num_vertices):
    """Add multiple vertices to the hypergraph."""
    start_time = time.time()
    for i in range(1, num_vertices + 1):
        hg.add_v(i, {"name": f"Vertex-{i}"})
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Added {num_vertices} vertices in {total_time:.2f} seconds.")
    return total_time


def add_edges(hg, num_edges, max_vertices):
    """Add multiple hyperedges to the hypergraph."""
    start_time = time.time()
    for _ in range(num_edges):
        edge_size = random.randint(2, min(5, max_vertices))  # Each hyperedge contains 2 to 5 vertices
        vertices = random.sample(range(1, max_vertices + 1), edge_size)
        hg.add_e(tuple(vertices), {"relation": "random_edge"})
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Added {num_edges} edges in {total_time:.2f} seconds.")
    return total_time


def query_vertices(hg, num_queries, max_vertices):
    """Randomly query vertex data."""
    start_time = time.time()
    for _ in range(num_queries):
        v_id = random.randint(1, max_vertices)
        hg.v(v_id)
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Queried {num_queries} vertices in {total_time:.2f} seconds.")
    return total_time


def query_edges(hg, num_queries, max_vertices):
    """Randomly query hyperedge data."""
    start_time = time.time()
    for _ in range(num_queries):
        edge_size = random.randint(2, min(5, max_vertices))
        vertices = random.sample(range(1, max_vertices + 1), edge_size)
        hg.e(tuple(vertices), default=None)
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Queried {num_queries} edges in {total_time:.2f} seconds.")
    return total_time


def stress_test(num_vertices=5000, num_edges=1000, num_queries=2000, scale_factor=1):
    """
    Single-threaded stress test for HypergraphDB.
    - Add vertices
    - Add hyperedges
    - Query vertices and hyperedges
    """
    hg = HypergraphDB()

    # Adjust the number of vertices and edges based on the scale factor
    vertices = num_vertices * scale_factor
    edges = num_edges * scale_factor
    queries = num_queries * scale_factor

    logger.info(f"Starting stress test with scale factor {scale_factor}...")

    # Step 1: Add vertices
    vertex_add_time = add_vertices(hg, vertices)

    # Step 2: Add hyperedges
    edge_add_time = add_edges(hg, edges, vertices)

    # Step 3: Query vertices
    vertex_query_time = query_vertices(hg, queries, vertices)

    # Step 4: Query hyperedges
    edge_query_time = query_edges(hg, queries, vertices)

    total_time = vertex_add_time + edge_add_time + vertex_query_time + edge_query_time

    # Collect test results
    result = {
        "vertices_added": vertices,
        "edges_added": edges,
        "vertex_queries": queries,
        "edge_queries": queries,
        "vertex_add_time": vertex_add_time,
        "edge_add_time": edge_add_time,
        "vertex_query_time": vertex_query_time,
        "edge_query_time": edge_query_time,
        "total_time": total_time,
    }

    # Log test results
    logger.info(f"Stress Test Completed for Scale Factor {scale_factor}:")
    logger.info(f"  - Vertices added: {result['vertices_added']} in {result['vertex_add_time']:.2f} seconds")
    logger.info(f"  - Edges added: {result['edges_added']} in {result['edge_add_time']:.2f} seconds")
    logger.info(f"  - Vertex queries: {result['vertex_queries']} in {result['vertex_query_time']:.2f} seconds")
    logger.info(f"  - Edge queries: {result['edge_queries']} in {result['edge_query_time']:.2f} seconds")
    logger.info(f"  - Total Time: {result['total_time']:.2f} seconds")

    # Return results for summary
    return result


def stress_increasing_scales_test():
    """
    Perform stress tests on hypergraphs with increasing scales.
    """
    scale_factors = [1, 2, 5, 10, 20, 50, 100, 200]  # Increasing scale factors
    results = []

    # Collect results for each scale factor
    for scale in scale_factors:
        logger.info(f"Starting stress test for scale factor: {scale}")
        result = stress_test(num_vertices=5000, num_edges=1000, num_queries=2000, scale_factor=scale)
        results.append(result)

    # Output test results as a table
    logger.info("\nSummary of Stress Test Results:\n")
    logger.info(f"{'num v':<10}{'num e':<10}{'add v':<10}{'add e':<10}{'query v':<15}{'query e':<15}{'total time':<10}")
    logger.info("-" * 80)
    for result in results:
        logger.info(
            f"{result['vertices_added']:<10}"
            f"{result['edges_added']:<10}"
            f"{result['vertex_add_time']:<10.2f}"
            f"{result['edge_add_time']:<10.2f}"
            f"{result['vertex_query_time']:.2f}/{result['vertex_queries']:<10}"
            f"{result['edge_query_time']:.2f}/{result['edge_queries']:<10}"
            f"{result['total_time']:<10.2f}"
        )


if __name__ == "__main__":
    stress_increasing_scales_test()