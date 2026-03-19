__author__ = "8658986, Al-Ramessi"


"""
graph_main.py

This module handles all user interaction for creating a graph and
computing the shortest path between two selected nodes.

Only option (c) from the assignment is implemented here:
- Find the shortest path between two nodes using BFS.

All computations are performed in graph_operations.py.
"""

# import the BFS shortest path function
from graph_operations import shortest_path


def main():
    # 1. Directed or undirected?
    # Ask user whether the graph is directed or undirected
    while True:
        # normalize input to lowercase
        ans = input("Directed graph? (y/n): ").lower()
        if ans in ["y", "n"]:
            directed = ans == "y"  # convert 'y'/'n' to boolean True/False
            break
        print("Please type 'y' or 'n'.")  # error message if input is invalid

    # 2. Enter nodes
    # Ask the user how nodes should be added: automatically,
    # manually, or with positions
    while True:
        method = input(
            "Add nodes automatically, manually, or with positions? (a/m/p): ").lower()
        if method in ["a", "m", "p"]:
            break
        print("Please type 'a', 'm', or 'p'.")

    nodes = []              # list to store node names
    positions = None
    # dictionary to store node positions if chosen, not used in BFS

    # Automatic node names
    if method == "a":
        while True:
            try:
                n = int(input("Number of nodes: "))  # get number of nodes
                if n > 0:
                    break
                print("Number must be greater than 0.")
            except ValueError:
                print("Please type a valid integer.")

        # Automatically generate node names as strings "1", "2", ..., "n"
        nodes = [str(i + 1) for i in range(n)]

    # Manual node names
    elif method == "m":
        while True:
            nodes = input("Enter node names separated by spaces: ").split()
            if nodes:
                break
            print("Please enter at least one node.")

    # Nodes with positions
    elif method == "p":
        positions = {}
        while True:
            try:
                n = int(input("Number of nodes: "))
                if n > 0:
                    break
                print("Number must be greater than 0.")
            except ValueError:
                print("Please type a valid integer.")

        # Generate node names automatically and collect positions
        for i in range(n):
            name = str(i + 1)
            nodes.append(name)

            # Ask for X and Y coordinates for each node
            while True:
                try:
                    x = float(input(f"X coordinate for node {name}: "))
                    y = float(input(f"Y coordinate for node {name}: "))
                    positions[name] = (x, y)  # store coordinates
                    break
                except ValueError:
                    print("Please enter valid numbers for X and Y.")

    # 3. Enter edges
    edges = []
    print("Enter edges as 'start end', one per line. Leave empty to finish.")

    while True:
        line = input()
        if line == "":  # empty input finishes edge entry
            break

        parts = line.split()
        if len(parts) != 2:  # validate correct input format
            print("Please enter exactly two node names separated by space.")
            continue

        u, v = parts
        if u not in nodes or v not in nodes:  # ensure nodes exist
            print(f"Both nodes must exist. Current nodes: {nodes}")
            continue

        edges.append((u, v))  # add edge to list

    # 4. Shortest path calculation
    print("\nShortest path computation selected.")

    # Ask user for start and target nodes
    while True:
        start_input = input("Start node: ").strip()
        target_input = input("Target node: ").strip()

        # splits inputs by space to check if user
        # entered more that one node accidentally
        start_nodes = start_input.split()
        target_nodes = target_input.split()

        if len(start_nodes) != 1 or len(target_nodes) != 1:
            print("Please enter exactly one node for start and one node for target.")
            continue

        start = start_nodes[0]
        target = target_nodes[0]

        if start not in nodes or target not in nodes:
            # validate node existence
            print(f"Both nodes must exist. Current nodes: {nodes}")
            continue
        break

    # Compute the shortest path using BFS from graph_operations.py
    path = shortest_path(nodes, edges, directed, start, target)

    # Display result
    if path:
        # join nodes with arrows for clarity
        print("Shortest path:", " -> ".join(path))
    else:
        print("No path found.")  # no path exists between start and target

    """
    Example test cases (as comments):

    Test Case 1: Simple undirected chain
        Nodes: A, B, C, D
        Edges: A-B, B-C, C-D
        Directed: False
        Start: A, Target: D
        Expected Output: A -> B -> C -> D

    Test Case 2: Directed graph with multiple paths
        Nodes: 1, 2, 3, 4
        Edges: 1->2, 1->3, 2->4, 3->4
        Directed: True
        Start: 1, Target: 4
        Expected Output: 1 -> 2 -> 4  (BFS finds first shortest path)

    Test Case 3: No path
        Nodes: X, Y, Z
        Edges: X-Y
        Directed: False
        Start: Y, Target: Z
        Expected Output: No path found.
    """


if __name__ == "__main__":
    main()
