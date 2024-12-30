import math
from priority_queues import DictPQ, HeapPQ


def find_shortest_path_with_heap(graph: dict[int, dict[int, float]], source: int, target: int) -> tuple[
    list[int], float]:

    initial_weights: dict[int, float] = {node: math.inf for node in graph}  # Space: O(|v|) Time: O(|v|)
    prev: dict[int, float | None] = {node: None for node in graph}  # Space: O(|v|) Time: O(|v|)
    initial_weights[source] = 0
    PQ: HeapPQ = HeapPQ()
    PQ.make(initial_weights)  # Space: O(|v|) Time: O(|v|)*cost-to-insert
    while len(PQ.heap_array) != 0:
        current_node: int = PQ.pop_min()  # Space: O(1) Time: O(1)*cost-to-deletemin
        if current_node == target:
            break
        for adjacent_node, weight in graph[current_node].items():  # Space: O(1)
            updated_weight = initial_weights[current_node] + weight  # Space&Time: O(1)
            if updated_weight < initial_weights[adjacent_node]:
                initial_weights[adjacent_node] = updated_weight  # Space&Time: O(1)
                prev[adjacent_node] = current_node  # Space&Time: O(1)
                PQ.update_queue_key(adjacent_node, updated_weight)  # Time: O(1)*cost-to-update-key

    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()

    return path, initial_weights[target]


def find_shortest_path_with_array(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """

    initial_weights: dict[int, float] = {node: math.inf for node in graph}
    prev: dict[int, int | None] = {node: None for node in graph}
    initial_weights[source] = 0
    PQ: DictPQ = DictPQ({source: 0})
    while PQ.weights:
        current_node: int = PQ.pop_min()
        if current_node == target:
            break
        for neighbor, weight in graph[current_node].items():
            updated_weight = initial_weights[current_node] + weight
            if updated_weight < initial_weights[neighbor]:
                initial_weights[neighbor] = updated_weight
                prev[neighbor] = current_node
                PQ.update_queue_key(neighbor, updated_weight)

    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()

    return path, initial_weights[target]
