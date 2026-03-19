__author__ = "8658986, Al-Ramessi"


"""
graph_operations.py

This module implements the functionality required for option (c) of the
assignment: computing the shortest path between two nodes in a graph.

It provides:
- Construction of an adjacency list
- Shortest path computation using Breadth-First Search (BFS)

This module performs no user interaction and is called by graph_main.py.
"""

from collections import deque  # deque is used for BFS queue (FIFO structure)


# Adjacency List Construction


def build_adj_list(nodes, edges, directed):
    """
    Build an adjacency list representation of the graph.

    For directed graphs, an edge (u, v) means u -> v.
    For undirected graphs, edges are added in both directions.

    Args:
        nodes (list[str]): List of node names.
        edges (list[tuple[str, str]]): List of (start, end) edges.
        directed (bool): Whether the graph is directed.

    Returns:
        dict[str, list[str]]: Mapping of node → list of neighbors.
    """
    # Initialize adjacency list with empty neighbor lists for each node
    adj = {n: [] for n in nodes}

    # Iterate through all edges and add them to the adjacency list
    for u, v in edges:
        adj[u].append(v)  # always add u -> v

        if not directed:
            # If graph is undirected, also add the reverse edge v -> u
            adj[v].append(u)

    # Return the complete adjacency list
    return adj


# Shortest Path via Breadth-First Search (BFS)


def shortest_path(nodes, edges, directed, start, target):
    """
    Compute the shortest path between two nodes using BFS.

    BFS explores nodes in layers, guaranteeing that the first time the
    target node is reached, the path is the shortest possible.

    Instead of storing only nodes in the queue, we store entire paths.
    This allows immediate return of the full path once the target is found.

    Args:
        nodes (list[str]): All node names.
        edges (list[tuple[str, str]]): Edges as (start, end) pairs.
        directed (bool): Whether the graph is directed.
        start (str): Starting node.
        target (str): Target node.

    Returns:
        list[str] | None:
            The shortest path including start and target,
            or None if no path exists.
    """
    # Step 1: Build adjacency list for efficient neighbor lookups
    adj = build_adj_list(nodes, edges, directed)

    # Step 2: Set of visited nodes to prevent revisiting
    visited = {start}

    # Step 3: BFS queue; each element is a full path from start to current node
    queue = deque([[start]])

    # Step 4: Main BFS loop
    while queue:
        path = queue.popleft()      # get the oldest path (FIFO)
        current = path[-1]          # current node is last element of path

        # Step 5: Check if target reached
        if current == target:
            return path             # return full path immediately

        # Step 6: Explore neighbors of current node
        for neighbor in adj[current]:
            if neighbor not in visited:
                visited.add(neighbor)      # mark neighbor as visited
                # append new path including this neighbor to queue
                queue.append(path + [neighbor])

    # Step 7: Target not reachable
    return None
