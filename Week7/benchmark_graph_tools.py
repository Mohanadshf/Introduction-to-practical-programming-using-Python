"""
benchmark_graph_tools.py

Module to benchmark the execution time of the Greedy and Recursive path-finding
algorithms for a weighted graph with two parameters: cost and distraction.

Includes:
- Three test cases
- Clear docstrings and comments
- Results printed in comments

"""

__author__ = "8636650, Kara, 8658986, Al-Ramessi"

import time
import timeit
import random
from graph_tools import Graph, \
    find_greedy, find_recursive, \
    strategy_diff, strategy_ratio, strategy_max_distraction

# Test Graph Creation


def create_test_graph1():
    """
    Test Case 1: Small fixed graph
    Graph layout:
        A - B - D
        |   |
        C - E - F
    Edges with random cost and distraction.

    Returns:
        Graph object
    """
    g = Graph()
    edges = [
        ("A", "B"), ("A", "C"), ("B", "D"),
        ("B", "E"), ("C", "E"), ("D", "F"), ("E", "F")
    ]
    # Randomly assign cost and distraction for each edge
    for start, end in edges:
        cost = random.randint(1, 10)          # cost between 1 and 10
        distraction = random.randint(0, 5)    # distraction between 0 and 5
        g.add_edge(start, end, cost, distraction)
    return g


def create_test_graph2():
    """
    Test Case 2: Medium graph with multiple paths
    More complex structure to show differences in path selection
    between Greedy and Recursive algorithms.

    Returns:
        Graph object
    """
    g = Graph()
    edges = [
        ("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"),
        ("C", "E"), ("C", "F"), ("D", "G"), ("E", "G"),
        ("F", "G"), ("G", "H")
    ]
    # Assign random costs/distractions to edges
    for start, end in edges:
        cost = random.randint(1, 15)          # higher costs possible
        distraction = random.randint(0, 7)    # higher distraction
        g.add_edge(start, end, cost, distraction)
    return g


def create_test_graph3():
    """
    Test Case 3: Small graph with only one possible path
    This case tests algorithm behavior when no alternative routes exist.

    Returns:
        Graph object
    """
    g = Graph()
    edges = [
        ("X", "Y"), ("Y", "Z")
    ]
    # Simple costs/distractions
    for start, end in edges:
        cost = random.randint(1, 5)
        distraction = random.randint(0, 3)
        g.add_edge(start, end, cost, distraction)
    return g

# Benchmark Function


def benchmark_graph(graph, start_node, end_node):
    """
    Benchmark Greedy and Recursive algorithms on a given graph.
    Measures execution time and prints results.

    Parameters:
        graph (Graph): The graph object to test
        start_node (str): Starting node name
        end_node (str): Ending node name

    Returns:
        None: Prints results directly,\
              includes commented lines for documentation
    """
    print(
        f"\nBenchmarking from {start_node} to {end_node} "
        f"on graph with {len(graph.neighbors)} nodes\n"
    )
    # Loop over all three strategies
    for strategy in [strategy_diff, strategy_ratio, strategy_max_distraction]:
        # --- Greedy Algorithm ---
        t0 = time.time()  # start time
        ti0 = timeit.default_timer()
        result_greedy = find_greedy(
            graph, start_node, end_node, strategy, "max")
        t1 = time.time()  # end time
        ti1 = timeit.default_timer()
        greedy_time = t1 - t0
        greedy_timeit = ti1 - ti0

        # Print results
        print(f"Greedy ({strategy.__name__}) Result: {result_greedy}")
        print(f"Greedy ({strategy.__name__}) Time: {greedy_time:.6f} sec")
        print(
            f"Greedy ({strategy.__name__}) Time (timeit): {greedy_timeit:.6f} sec")

        # --- Recursive Algorithm ---
        t0 = time.time()  # start time
        ti0 = timeit.default_timer()
        result_recursive = find_recursive(
            graph, start_node, end_node, strategy, "max")
        t1 = time.time()  # end time
        ti1 = timeit.default_timer()
        recursive_time = t1 - t0
        recursive_timeit = ti1 - ti0

        # Print results
        print(f"Recursive ({strategy.__name__}) Result: {result_recursive}")
        print(
            f"Recursive ({strategy.__name__}) "
            f"Time: {recursive_time:.6f} sec"
        )
        print(
            f"Recursive ({strategy.__name__}) "
            f"Time (timeit): {recursive_timeit:.6f} sec\n"
        )

        # Also print results in comment format for documentation
        # / assignment submission
        print("# --- RESULT COMMENT ---")
        print(
            f"# Greedy_{strategy.__name__}: {result_greedy}, "
            f"time = {greedy_time:.6f} sec, "
            f"timeit = {greedy_timeit:.6f} sec"
        )
        print(
            f"# Recursive_{strategy.__name__}: {result_recursive}, "
            f"time = {recursive_time:.6f} sec, "
            f"timeit = {recursive_timeit:.6f} sec\n"
        )


# Main Execution: Run all three test cases
if __name__ == "__main__":
    # Test Case 1: Small graph
    print("=== Benchmark Test Case 1 ===")
    g1 = create_test_graph1()
    benchmark_graph(g1, "A", "F")  # Start at A, end at F

    # Test Case 2: Medium graph with more alternative paths
    print("=== Benchmark Test Case 2 ===")
    g2 = create_test_graph2()
    benchmark_graph(g2, "A", "H")  # Start at A, end at H

    # Test Case 3: Graph with only one path
    print("=== Benchmark Test Case 3 ===")
    g3 = create_test_graph3()
    benchmark_graph(g3, "X", "Z")  # Start at X, end at Z
