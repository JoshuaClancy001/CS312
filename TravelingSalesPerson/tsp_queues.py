import math



class StackQueue:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def __len__(self):
        return len(self.stack)


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        max_indexes = []
        chosen_node_index = 0
        max_path_length = len(self.queue[0].path)

        for i in range(1, len(self.queue)):
            current_path_length = len(self.queue[i].path)
            if current_path_length == max_path_length:
                max_indexes.append(i)
            if current_path_length > max_path_length:
                max_indexes = []
                max_path_length = current_path_length
                max_indexes.append(i)

        for index in max_indexes:
            if self.queue[index].lower_bound < self.queue[chosen_node_index].lower_bound:
                chosen_node_index = index

        return self.queue.pop(chosen_node_index)

    def is_empty(self):
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)
