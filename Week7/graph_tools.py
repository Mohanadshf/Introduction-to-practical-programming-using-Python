"""
graph_tools.py

This module contains the definitions for graphs with weighted edges and
various multi-objective strategies for path optimization. It implements:

- Strategies:
    1. strategy_diff: Minimize costs, maximize distraction
    2. strategy_ratio: Maximize distraction per cost unit
    3. strategy_max_distraction: Maximize distraction, ignore costs

- Graph class: Representation of an undirected
graph with nodes and edges

- Algorithm:
    - find_greedy: Greedy algorithm for local path selection
    - find_recursive: Recursive algorithm for global optimal path

"""

__author__ = "8636650, Kara, 8658986, Al-Ramessi"


# multiple objective strategies
def strategy_diff(cost, distraction):
    '''
    Strategy 1.:
    Goal: The cost should be minimized but the distraction maximized.
    ==> A smaller value is better.
    Formula: Strategy 1 = cost - distraction

    Parameter:
        cost (int): the cost of the edge or path.
        distraction (int): the distraction of the edge or path.

    Return:
        int: The calculated value of strategy 1.

    Doctests:
    >>> strategy_diff(10, 5) # cost = 10, distraction = 5
    5
    >>> strategy_diff(7, 10) # cost = 7, distraction = 10
    -3
    >>> strategy_diff(20, 5) # cost = 20, distraction = 5
    15
    >>> strategy_diff("a", 5)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError
    '''

    return cost - distraction


def strategy_ratio(cost, distraction):
    '''
    Strategy 2.:
    Here the ratio or quotient of the parameters is important.
    Goal: The maximum distraction per cost unit.
    Formula: Strategy 2 = distraction / cost
    ==> A higher value is better.
    Special case: If the cost is 0, the value is considered infinite.

    Parameter:
        cost (int): The cost of the edge or path.
        distraction (int): The distraction of the edge or path
    Return:
        float: The calculated value of strategy 2.

    Doctests:
    >>> strategy_ratio(10, 5) # distraction = 5 / cost = 10
    0.5
    >>> strategy_ratio(20, 2) # distraction = 2 / cost = 20
    0.1
    >>> strategy_ratio(0, 5) # distraction = 5 / cost = 0
    inf
    >>> strategy_ratio("cost", 5)   # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError
    '''

    if cost == 0:
        return float('inf')
    return distraction / cost


def strategy_max_distraction(cost, distraction):
    '''
    Strategy 3.:
    Goal: The distraction should be maximized, and costs are ignored.
    ==> A higher value is better.
    Formula: Strategy 3 = distraction

    Parameter:
        distraction (int): The distraction of the edge or path.

    Return:
        int: distraction (int)

    Doctests:
    >>> strategy_max_distraction(77,10) # distraction = 10
    10
    >>> strategy_max_distraction(8, 0) # distraction = 0
    0
    >>> strategy_max_distraction(43, 7) # distraction = 7
    7

    # could not find a suitable negative example
    '''
    # Ignoring cost parameter, because of the strategy definition
    return distraction


class Graph:
    '''
    Represents an undirected graph with weighted edges.
    Each edge is associated with two values:
        - cost (int)
        - distraction (int)
    '''

    def __init__(self):
        '''
        We initialize an empty graph, in
        which the nodes and edges are added.
        These are stored in a dictionary named "neighbors".
        Key: node name (str)
        Value: List of tuples [(neighbor node, cost, distraction),...]
        '''
        self.neighbors = {}

    def add_edge(self, start, end, cost, distraction):
        '''
            Here we add an edge between the start and end node.

            Parameter:
                start (str): Node name of the start node.
                end (str): Node name of the end node.
                cost (int): The cost of the edge.
                distraction (int): The distraction of the edge.
        '''
        # We check if the start and end nodes already exist in the graph
        if start not in self.neighbors:
            self.neighbors[start] = []

        if end not in self.neighbors:
            self.neighbors[end] = []

        # We add the edge in both directions
        self.neighbors[start].append((end, cost, distraction))
        self.neighbors[end].append((start, cost, distraction))


# the Algorithms
def find_greedy(graph, start, target, strategy_func, mode):
    '''
    In this function, the greedy algorithm is implemented.
    The cat chooses locally at each node the edge without planning ahead
    and based on the passed strategy function.

    Parameter:
        graph (Graph): The Graph object
        start (str): The name of the start node
        target (str): The name of the target node
        strategy_func (function): The desired strategy function
        mode (str): "min" for minimization when using strategy_diff,
                    "max" for maximization when using strategy_ratio
                    "max" for maximization when using strategy_max_distraction

    Return:
        tuple: (path, total_cost, total_distraction)
            path (list): The list of nodes in the found path
            total_cost (int): The total cost of the path
            total_distraction (int): The total distraction of the path
        Or None, if no path was found.

    Doctests:
    Existing path:
    >>> g = Graph()
    >>> g.add_edge("A", "B", 5, 10)
    >>> find_greedy(g, "A", "B", strategy_diff, "min")
    (['A', 'B'], 5, 10)

    No existing path:
    >>> g = Graph()
    >>> g.add_edge("A", "B", 5, 10)
    >>> find_greedy(g, "A", "C", strategy_diff, "min") is None
    True

    Existing path with multiple steps (locally best choice for 'min'):
    >>> g = Graph()
    >>> g.add_edge("A", "B", 5, 10)  # Diff: 5 - 10 = -5 (locally minimal)
    >>> g.add_edge("B", "C", 2, 1)   # Diff: 2 - 1 = 1
    >>> g.add_edge("A", "C", 8, 12)  # Diff: 8 - 12 = -4
    >>> # Greedy chooses at A the edge A->B, because -5 < -4 ('min' mode).
    >>> # The resulting path is A->B->C.
    >>> find_greedy(g, "A", "C", strategy_diff, "min")
    (['A', 'B', 'C'], 7, 11)

    Negative example:
    >>> g = Graph()
    >>> g.add_edge("A", "B", 5, 10)
    >>> find_greedy(g, "A", "B", strategy_diff, "invalid") \
        # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError
    '''
    # to check the negative example
    if mode not in ["min", "max"]:
        raise ValueError("Mode must be 'min' or 'max'")

    # we set the current node as the start node
    current = start

    # the list to store the path
    path = [start]

    # a set to avoid cycles or infinite loops
    visited = {start}

    total_cost = 0  # total cost of the path
    total_distraction = 0  # total distraction of the path
    while current != target:
        # Gets all the neighbors of the current node
        option = graph.neighbors.get(current, [])

        # List of all possible next steps
        candidates = []

        # Step 1: Give each neighbor a value
        for neighbor, c, d in option:
            # Only consider unvisited neighbors
            if neighbor not in visited:
                # Calculate the value based on the strategy function
                value = strategy_func(c, d)
                # Update candidates list
                candidates.append((value, neighbor, c, d))

        if not candidates:
            # No further step possible, path does not exist
            # So we reached a dead end
            return None

        # Step 2.: Choose the best candidate based on the mode
        if mode == "min":
            candidates.sort(key=lambda x: x[0])  # Sort ascending
        else:  # mode == "max"
            candidates.sort(key=lambda x: x[0], reverse=True)  # Sort desc.

        best = candidates[0]  # Choose the best neighbor
        # Step 3: Update the path
        current = best[1]  # Next node
        total_cost += best[2]  # Update costs
        total_distraction += best[3]  # Update distraction

        path.append(current)  # Add node to path
        # Mark node as visited to avoid cycles
        visited.add(current)

    # Target node was reached
    return (path, total_cost, total_distraction)


def find_recursive(graph, start, target, strategy_func, mode):
    '''
    In this function the recursive algorithm is implemented.
    The cat plans ahead and chooses the best path,
    based on the passed strategy function.
    Here a path is searched for that is globally optimal.
    The cat tries all possible paths and remembers the best one.
    The optimization strategy is applied to aggregated path values (total cost
    and total distraction).

    Parameter:
        graph (Graph): The Graph object.
        start (str): The name of the start node.
        target (str): The name of the target node.
        strategy_func (function): The desired strategy function.
        mode (str): "min" for minimization with strategy_diff
                    "max" for maximization with strategy_ratio
                    "max" for maximization with strategy_max_distraction

    Return:
        tuple: (path, total_cost, total_distraction)
            path (list): The list of nodes in the found path
            total_cost (int): The total cost of the path
            total_distraction (int): The total distraction of the path
        Or None, if no path was found.

    Doctests:
    1. Optimal path is found:
    >>> g = Graph()
    >>> # Direct path: A =>B
    >>> # cost = 10, distraction = 4.
    >>> #Score (cost - distraction) = 6
    >>> g.add_edge("A", "B", 10, 4)
    >>> # Detour: A => C => B
    >>> # A => C: cost = 2, distraction = 0
    >>> # C => B: cost = 2, distraction = 0
    >>> # Total cost: 4, total distraction: 0
    >>> # Score = (cost - distraction) = 4 - 0 = 4
    >>> g.add_edge("A", "C", 2, 0)
    >>> g.add_edge("C", "B", 2, 0)
    >>> # The recursive algorithm should choose the detour because 4 < 6
    >>> path, c, d = find_recursive(g, "A", "B", strategy_diff, "min")
    >>> path
    ['A', 'C', 'B']
    >>> c
    4

    2. An unreachable path
    >>> g = Graph()
    >>> g.add_edge("A", "B", 5, 10)
    >>> find_recursive(g, "A", "C", strategy_diff, "min") is None
    True

    3. Maximization of distraction (strategy_max_distraction):
    >>> g = Graph()
    >>> # Direct path: A => B
    >>> # Distraction: 3
    >>> g.add_edge("A", "B", 1, 3)
    >>> # Detour: A => C => B
    >>> # Distraction: 5 + 5 = 10
    >>> g.add_edge("A", "C", 10, 5)
    >>> g.add_edge("C", "B", 10, 5)
    >>> path, c, d = find_recursive(g, "A", "B", \
        strategy_max_distraction, "max")
    >>> path
    ['A', 'C', 'B']
    >>> d
    10

    4. Negative example:
    >>> g = Graph()
    >>> g.add_edge("A", "B", 5, 10)
    >>> find_recursive(g, "A", "B", strategy_diff, "invalid") \
            # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError

    '''

    if mode not in ["min", "max"]:
        raise ValueError("Mode must be 'min' or 'max'")

    # we initialize the variable for the best path
    # float('inf') for minimization, float('-inf') for maximization
    start_value = float('inf') if mode == "min" else float('-inf')

    # [value, path, total_cost, total_distraction]
    best_result = [start_value, None, 0, 0]

    # Step 1.: Start of the recursion
    # We use a helper function _recursion_step
    # Overwrites the global best path
    # if a target node is reached with a better value.
    _recursion_step(
        graph, start, target,
        [start], 0, 0,
        strategy_func, mode, best_result  # Pass the shared state
    )

    # Step 2.: Return the best found path
    # We check if the marker [1] has been updated
    if best_result[1] is not None:
        return (best_result[1], best_result[2], best_result[3])
    else:
        return None  # no path found


def _recursion_step(graph, current, target, path, cost, dist,
                    strategy_func, mode, best):
    '''
    This is a helper function for the recursion in the find_recursive.
    This function is called recursively to search all possible paths.
    Parameter:
        graph (Graph): The Graph object.
        current (str): The current node name.
        target (str): The target node name.
        path (list): The current path as a list of nodes.
        cost (int): The current total cost of the path.
        dist (int): The current total distraction of the path.
        strategy_func (function): The desired strategy function.
        mode (str): "min" for minimization, "max" for maximization.
        best (list): Shared state for storing the best path.

    Doctests:
    1. Base case: current == target (minimize)
    >>> g = Graph()
    >>> best = [float('inf'), None, 0, 0]
    >>> _recursion_step(g, "A", "A", ["A"], 5, 2, strategy_diff, "min", best)
    >>> best[1]
    ['A']
    >>> best[2]
    5

    2. Simple path with one step
    >>> g = Graph()
    >>> g.add_edge("A", "B", 3, 1)
    >>> best = [float('inf'), None, 0, 0]
    >>> _recursion_step(g, "A", "B", ["A"], 0, 0, strategy_diff, "min", best)
    >>> best[1]
    ['A', 'B']
    >>> best[2]
    3

    3. Maximization (strategy_max_distraction)
    >>> g = Graph()
    >>> g.add_edge("A", "B", 1, 7)
    >>> best = [float('-inf'), None, 0, 0]
    >>> _recursion_step(g, "A", "B", ["A"], 0, \
        0, strategy_max_distraction, "max", best)
    >>> best[3]
    7

    4. Negative example (function not valid)
    >>> g = Graph()
    >>> best = [float('inf'), None, 0, 0]
    >>> _recursion_step(g, "A", "B", ["A"], 0, \
        0, "not_a_function", "min", best) \
        # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError
    '''

    # Check if strategy_func is callable
    if not callable(strategy_func):
        raise TypeError("strategy_func must be a callable function")

    # Base case: If the current node is the target node
    if current == target:
        score = strategy_func(cost, dist)

        improved = False
        # Check if the best path has been improved
        if mode == "min" and score < best[0]:
            improved = True
        elif mode == "max" and score > best[0]:
            improved = True

        if improved:
            # Update the best path found so far
            best[0] = score
            best[1] = list(path)   # Create a copy of the current path
            best[2] = cost
            best[3] = dist
        return  # End of recursion, as target reached

    # recursive step: Explore all neighbors
    # Sort the neighbors by node name
    neighbors = sorted(graph.neighbors.get(current, []), key=lambda x: x[0])

    for node, c, d in neighbors:
        # Avoid cycles by only considering unvisited nodes
        if node not in path:
            _recursion_step(
                graph, node, target,
                path + [node],  # Create a new path
                cost + c,       # Add the costs
                dist + d,       # Add the distraction
                strategy_func, mode, best
            )


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print("All Doctests were successfully passed.")
