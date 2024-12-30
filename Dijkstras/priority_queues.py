from copy import deepcopy
class HeapPQ:
    def __init__(self):
        self.heap_array: list[int] = []
        self.priority_dict: dict[int, float] = {}
        self.location_dict: dict[int, float] = {}

    def make(self, weights: dict[int, float]) -> None:
        min_node = min(weights, key=weights.get) # Space: O(1) Time: O(|v|)
        self.heap_array.append(min_node)
        self.priority_dict[min_node] = weights[min_node]
        self.location_dict[min_node] = 0
        for node, weight in weights.items(): # Space: O(|v|) Time: O(|v|)
            if node != min_node:
                self.heap_array.append(node)
                self.priority_dict[node] = weight
                self.location_dict[node] = len(self.heap_array) - 1

    def pop_min(self) -> int:
        min_val = self.heap_array[0]
        last_val = self.heap_array[-1]
        self.heap_array[0] = last_val
        self.location_dict[last_val] = 0
        self.heap_array.pop()

        ## All of the above Space: O(1) Time: O(1)

        if self.heap_array:  # Space: O(1) Time: O(log|v|)
            self.trickle_down(0)

        ## All below Space: O(1) Time: O(1)
        del self.priority_dict[min_val]
        del self.location_dict[min_val]

        return min_val

    def update_queue_key(self, node: int, changed_weight: float):
        self.priority_dict[node] = changed_weight
        index: int = self.location_dict[node]
        parent: int = self.parent(index)
        if index > 0 and self.priority_dict[self.heap_array[parent]] > self.priority_dict[node]:
            self.trickle_up(index)
        else:
            self.trickle_down(index)

    def trickle_down(self, parent_index: int):
        while True:
            left_child_index: int = parent_index * 2 + 1
            right_child_index: int = parent_index * 2 + 2
            smallest_child: int = parent_index

            if left_child_index < len(self.heap_array) and self.priority_dict[self.heap_array[left_child_index]] < \
                    self.priority_dict[self.heap_array[smallest_child]]:
                smallest_child = left_child_index
            if right_child_index < len(self.heap_array) and self.priority_dict[self.heap_array[right_child_index]] < \
                    self.priority_dict[self.heap_array[smallest_child]]:
                smallest_child = right_child_index
            if smallest_child == parent_index:
                break
            self.swap(parent_index, smallest_child)
            parent_index = smallest_child

    def trickle_up(self, index: int):
        while index > 0:
            parent_index: int = self.parent(index)
            if self.priority_dict[self.heap_array[parent_index]] > self.priority_dict[self.heap_array[index]]:
                self.swap(parent_index, index)
                index = parent_index
            else:
                break

    def parent(self, child_index: int):
        return (child_index - 1) // 2

    def swap(self, parent: int, child: int):
        self.heap_array[parent], self.heap_array[child] = self.heap_array[child], self.heap_array[parent]
        self.location_dict[self.heap_array[parent]], self.location_dict[self.heap_array[child]] = parent, child


class DictPQ:
    def __init__(self, weights: dict[int, float]):  # Space: O(|v|) Time: O(1)
        self.weights: dict[int, float] = weights

    def pop_min(self) -> int: # Space: O(1) Time: O(|v|)
        min_node = min(self.weights.items(), key=lambda item: item[1])[0]
        del self.weights[min_node]
        return min_node

    def update_queue_key(self, node: int, changed_weight: float): # Space: O(1) Time: O(1)
        self.weights[node] = changed_weight
