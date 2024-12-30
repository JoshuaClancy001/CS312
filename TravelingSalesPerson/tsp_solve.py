import math
import random
from copy import deepcopy

from tsp_queues import StackQueue, PriorityQueue
from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver, score_partial_tour
from tsp_cuttree import CutTree


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    score: float = 0
    path: list = []
    solutions: list = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    for node in range(len(edges)): # Space: O(n) Time: O(n^2)
        n_nodes_expanded += 1
        current_node = node
        while not timer.time_out():
            path.append(current_node)
            if len(path) == len(edges):
                if score_tour(path, edges) != math.inf:
                    solutions.append(SolutionStats(deepcopy(path), score_tour(path, edges), timer.time(), len(path),
                                                   n_nodes_expanded, n_nodes_pruned, cut_tree.n_leaves_cut(),
                                                   cut_tree.fraction_leaves_covered()))
                return solutions

            row: list = deepcopy(edges[current_node])
            min_cost: float = min(row)
            while row.index(min_cost) in path:
                row[row.index(min_cost)] = math.inf
                min_cost = min(row)
                if min_cost == math.inf:
                    break
            node_traveled_to: int = row.index(min_cost)
            current_node = node_traveled_to
            score += min_cost
            if score == math.inf:
                cut_tree.cut(path)
                path = []
                score = 0
                n_nodes_pruned += 1
                break
        if timer.time_out():
            return solutions


def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stack: list[tuple[list, float]] = [([0], 0)]
    solutions: list[SolutionStats] = []
    bssf: float = math.inf
    while stack and not timer.time_out():
        path, score = stack.pop()
        current_node = path[-1]
        if len(path) == len(edges):
            score = score_tour(path, edges)
            if score != math.inf:
                if score < bssf:
                    bssf = score
                    solutions.append(SolutionStats(path, score, timer.time(), len(stack), 0, 0, 0, 0))
        else:
            for next_node, cost in enumerate(edges[current_node]):
                if next_node not in path and edges[current_node][next_node] != math.inf:
                    temp_path = deepcopy(path + [next_node])
                    stack.append((temp_path, score_partial_tour(temp_path, edges)))
    return solutions


def branch_and_bound_base(edges: list[list[float]], timer: Timer, starting_node: int, queue) -> list[SolutionStats]:
    state_number = 0
    solutions: list[SolutionStats] = greedy_tour(edges, timer)
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    if solutions:
        bssf = solutions[0].score
    else:
        bssf = math.inf

    current_state: State = State(state_number, [starting_node], 0, 0, edges, 0, 0)
    state_number += 1
    current_state.init_state_reduce()
    queue.push(current_state)

    while queue and not timer.time_out():
        current_state = queue.pop()
        if current_state.lower_bound + current_state.cost_to_take > bssf:
            n_nodes_pruned += 1
            cut_tree.cut(current_state.path)
            continue
        else:
            if len(current_state.path) == len(edges):

                score = score_tour(current_state.path, edges)
                if score < bssf:
                    bssf = deepcopy(score)
                    solutions.append(SolutionStats(current_state.path, bssf, timer.time(), len(queue), n_nodes_expanded,
                                                   n_nodes_pruned, cut_tree.n_leaves_cut(),
                                                   cut_tree.fraction_leaves_covered()))
                else:
                    n_nodes_pruned += 1
                    cut_tree.cut(current_state.path)
            else:
                if timer.time_out():
                    return solutions
                row = current_state.matrix[current_state.path[-1]]

                for node, cost in enumerate(row):
                    if timer.time_out():
                        return solutions
                    if cost == math.inf and node not in current_state.path:
                        cut_path = deepcopy(current_state.path + [node])
                        cut_tree.cut(cut_path)
                        n_nodes_pruned += 1
                        continue
                    if node not in current_state.path:
                        temp_path = deepcopy(current_state.path + [node])
                        if current_state.lower_bound + cost >= bssf:
                            n_nodes_pruned += 1
                            cut_tree.cut(temp_path)
                            continue

                        new_state = State(
                            state_number + 1, temp_path, current_state.lower_bound, current_state.matrix[current_state.path[-1]][node],
                            current_state.matrix, current_state.path[-1], node)
                        state_number += 1
                        if new_state.calculate_lower_bound() < bssf:
                            n_nodes_expanded += 1
                            queue.push(new_state)
                        else:
                            n_nodes_pruned += 1
                            cut_tree.cut(temp_path)

    return solutions


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return branch_and_bound_base(edges, timer, 0, StackQueue())


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    min_cost = math.inf
    best_node = 0
    for i in range(len(edges)):
        for j in range(len(edges)):
            edge = edges[i][j]
            if edges[i][j] < min_cost and edges[i][j] != 0:
                min_cost = edges[i][j]
                best_node = i
    return branch_and_bound_base(edges, timer, best_node, PriorityQueue())


class State:
    def __init__(self, state_number, path: list = [], lower_bound: float = 0, cost_to_take: float = 0, edges=None,
                 row: int = 0, col: int = 0):
        self.state_number = state_number
        if edges is None:
            edges = [[]]
        self.path: list[int] = path
        self.lower_bound: float = lower_bound
        self.cost_to_take: float = cost_to_take
        self.matrix: list[list[float]] = deepcopy(edges)
        self.row = row
        self.col = col

    def reduce_matrix(self):
        for i in range(len(self.matrix)):
            self.matrix[i][self.col] = math.inf

        for i in range(len(self.matrix[self.row])):
            self.matrix[self.row][i] = math.inf

        self.matrix[self.col][self.row] = math.inf

        for i, row in enumerate(self.matrix):
            min_val = min(row)
            if min_val != 0 and min_val != math.inf:
                for j in range(len(row)):
                    if row[j] != math.inf:
                        row[j] -= min_val
                self.lower_bound += min_val
        for col in range(len(self.matrix[0])):
            column = [row[col] for row in self.matrix]
            min_val = min(column)
            if min_val != 0 and min_val != math.inf:
                for row in range(len(column)):
                    if column[row] != math.inf:
                        self.matrix[row][col] -= min_val
                self.lower_bound += min_val

    def init_state_reduce(self):
        n = len(self.matrix)

        for i in range(n):
            self.matrix[i][i] = math.inf
            min_val = min(val for val in self.matrix[i] if val != math.inf)
            if min_val != 0:
                self.matrix[i] = [val - min_val if val != math.inf else math.inf for val in self.matrix[i]]
                self.lower_bound += min_val
        for j in range(n):
            min_val = min(self.matrix[i][j] for i in range(n) if self.matrix[i][j] != math.inf)
            if min_val != 0:
                for i in range(n):
                    if self.matrix[i][j] != math.inf:
                        self.matrix[i][j] -= min_val
                self.lower_bound += min_val

    def calculate_lower_bound(self) -> float:
        self.reduce_matrix()
        self.lower_bound += self.cost_to_take
        return self.lower_bound

# def test():
#     matrix = {
#         (r, c): w
#         for r, row in enumerate(edges)
#         for c, w in enumerate(row)
#         if not math.isinf(w)
#     }
# def reducedictmatrix(matrix: dict[tuple[int, int], float]) -> tuple[float, dict[int, int]]:
#     matrix = matrix.copy
#     score = 0
#     row_mins = {}
#     for (r, c), w in matrix.items():
#         if r not in row_mins or row_mins[r] > w:
#             row_mins[r] = w
#     score += sum(row_mins.values())
#     for r, c in matrix:
#         matrix[r, c] -= row_mins[r]
#
#     col_mins = {}
#     for (r,c), w in matrix.items():
#         if c not in col_mins or col_mins[c] > w:
#             col_mins[c] = w
#     score += sum(col_mins.values())
#
#     for r, c in matrix:
#         matrix[r, c] -= col_mins[c]
#
#     return score, matrix
#
#
# def test():
#     matrix = {
#         (0,1):8,
#         (0,2):12,
#         (0,3):4,
#
#     }
