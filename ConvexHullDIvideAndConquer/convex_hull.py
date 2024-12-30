# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point


class Point:
    def __init__(self, x: float, y: float):
        self.counter_clockwise = None
        self.clockwise = None
        self.value = (x, y)


class Tangent:
    def __init__(self, left: Point, right: Point):
        self.left_point: Point = left
        self.right_point: Point = right
        self.slope = compute_point_slope(left, right)
        self.left_point_done = False
        self.right_point_done = False

    def upper_piv_right(self, rounds_past: int) -> 'Tangent':
        while 1:
            temp_slope = compute_float_slope(self.left_point.counter_clockwise.value,
                                             self.right_point.value)  # Time: O(1) Space: O(1)
            if temp_slope < self.slope:  # Time: O(1) Space: O(1) everything inside the if else statement is O(1)
                self.left_point = self.left_point.counter_clockwise
                self.slope = temp_slope
                rounds_past = 0
                self.left_point_done = False
            else:
                rounds_past += 1
            if rounds_past == 2:
                return self  # Time: O(1) Space: O(1)
            else:
                return self.upper_piv_left(rounds_past)  # Time: O(n) Space: O(n)
        rounds_past += 1
        return self.upper_piv_left(rounds_past)  # Time: O(n) Space: O(n)

    def upper_piv_left(self, rounds_past: int) -> 'Tangent':
        while 1:
            temp_slope = compute_float_slope(self.left_point.value, self.right_point.clockwise.value)
            if temp_slope > self.slope:
                self.right_point = self.right_point.clockwise
                self.slope = temp_slope
                rounds_past = 0
                self.right_point_done = False
                # draw_line(self.left_point.value, self.right_point.value)
            else:
                self.right_point_done = True
                rounds_past += 1
            if rounds_past == 2:
                return self
            else:
                return self.upper_piv_right(rounds_past)
        rounds_past += 1
        return self.upper_piv_right(rounds_past)

    def lower_piv_right(self, rounds_past: int) -> 'Tangent':
        while 1:
            # draw_line(self.left_point.value, self.right_point.value)
            temp_slope = compute_float_slope(self.left_point.clockwise.value, self.right_point.value)
            if temp_slope > self.slope:
                self.left_point = self.left_point.clockwise
                self.slope = temp_slope
                rounds_past = 0
                self.left_point_done = False
                # draw_line(self.left_point.value, self.right_point.value)
            else:
                rounds_past += 1
            if rounds_past == 2:
                return self
            else:
                return self.lower_piv_left(rounds_past)
        rounds_past += 1
        return self.lower_piv_left(rounds_past)

    def lower_piv_left(self, rounds_past: int) -> 'Tangent':
        while 1:
            # draw_line(self.left_point.value, self.right_point.value)
            temp_slope = compute_float_slope(self.left_point.value, self.right_point.counter_clockwise.value)
            if temp_slope < self.slope:
                self.right_point = self.right_point.counter_clockwise
                self.slope = temp_slope
                rounds_past = 0
                self.right_point_done = False
                # draw_line(self.left_point.value, self.right_point.value)
            else:
                self.right_point_done = True
                rounds_past += 1
            if rounds_past == 2:
                return self
            else:
                return self.lower_piv_right(rounds_past)
        rounds_past += 1
        return self.lower_piv_right(rounds_past)


class Hull:
    def __init__(self, points: list[Point]):
        self.points: list[Point] = points
        self.upper_tangent = None
        self.lower_tangent = None
        self.left_most_point = None
        self.right_most_point = None

    def draw_hull(self):
        draw_hull([point.value for point in self.points])

    def to_tuple_list(self) -> list[tuple[float, float]]:
        return [point.value for point in self.points]


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    sorted_points: list[tuple[float, float]] = sorted(points, key=lambda point: point[0])  # O(nlogn)
    if len(sorted_points) < 4:
        return sorted_points  # O(1)
    else:
        #O(nlogn)
        left_hull = divide_and_conquer(sorted_points[:len(sorted_points) // 2])
        right_hull = divide_and_conquer(sorted_points[len(sorted_points) // 2:])

        return merge_final_hulls(left_hull, right_hull)  # O(n)


def compute_point_slope(left: Point, right: Point) -> float:
    return (right.value[1] - left.value[1]) / (right.value[0] - left.value[0])


def compute_float_slope(left: tuple[float, float], right: tuple[float, float]) -> float:
    return (right[1] - left[1]) / (right[0] - left[0])


def divide_and_conquer(float_points: list[tuple[float, float]]) -> Hull:
    if len(float_points) == 2:
        # draw_hull(float_points)   Time: O(1) Space: O(1)
        return compute_two_point_hull(float_points)
    elif len(float_points) == 3:
        # draw_hull(float_points)   Time: O(1) Space: O(1)
        return compute_three_point_hull(float_points)
    else:
        # Time: O(n) Space: O(n)
        left_hull = divide_and_conquer(float_points[:len(float_points) // 2])
        right_hull = divide_and_conquer(float_points[len(float_points) // 2:])
        return merge_hulls(left_hull, right_hull)  # Time: O(n) Space: O(n)


def compute_three_point_hull(float_points: list[tuple[float, float]]):
    points: list[Point] = []
    for point in float_points:
        x: float = point[0]
        y: float = point[1]
        points.append(Point(x, y))

    if compute_point_slope(points[0], points[1]) > compute_point_slope(points[0], points[2]):
        points[0].clockwise = points[1]
        points[0].counter_clockwise = points[2]
        points[1].clockwise = points[2]
        points[1].counter_clockwise = points[0]
        points[2].clockwise = points[0]
        points[2].counter_clockwise = points[1]
    elif compute_point_slope(points[0], points[1]) < compute_point_slope(points[0], points[2]):
        points[0].clockwise = points[2]
        points[0].counter_clockwise = points[1]
        points[1].clockwise = points[0]
        points[1].counter_clockwise = points[2]
        points[2].clockwise = points[1]
        points[2].counter_clockwise = points[0]
    hull: Hull = Hull(points)
    hull.left_most_point = points[0]
    hull.right_most_point = points[2]
    return hull


def compute_two_point_hull(float_points: list[tuple[float, float]]):
    points: list[Point] = []
    points.append(Point(float_points[0][0], float_points[0][1]))  # add most left point
    points.append(Point(float_points[1][0], float_points[1][1]))  # add most right point
    points[0].clockwise = points[1]
    points[0].counter_clockwise = points[1]
    points[1].clockwise = points[0]
    points[1].counter_clockwise = points[0]
    hull: Hull = Hull(points)
    hull.left_most_point = points[0]
    hull.right_most_point = points[1]
    return hull


def merge_hulls(left_hull: Hull, right_hull: Hull) -> Hull:
    merged_hull: Hull = Hull([])
    merged_hull.left_most_point = left_hull.left_most_point
    merged_hull.right_most_point = right_hull.right_most_point
    upper_tangent: Tangent = Tangent(left_hull.right_most_point, right_hull.left_most_point)
    lower_tangent: Tangent = Tangent(left_hull.right_most_point, right_hull.left_most_point)
    # everything above is constant time and space complexity
    upper_tangent = upper_tangent.upper_piv_right(0)  # Time: O(n) Space: O(n)
    lower_tangent = lower_tangent.lower_piv_right(0)  # Time: O(n) Space: O(n)
    point: Point = left_hull.left_most_point
    while point != upper_tangent.left_point:  # Time: O(n) Space: O(1)
        merged_hull.points.append(point)
        point = point.clockwise
    upper_tangent.left_point.clockwise = upper_tangent.right_point
    upper_tangent.right_point.counter_clockwise = upper_tangent.left_point
    merged_hull.points.append(upper_tangent.left_point)

    point = upper_tangent.right_point
    while point != lower_tangent.right_point:  # Time: O(n) Space: O(1)
        merged_hull.points.append(point)
        point = point.clockwise
    lower_tangent.right_point.clockwise = lower_tangent.left_point
    lower_tangent.left_point.counter_clockwise = lower_tangent.right_point
    merged_hull.points.append(lower_tangent.right_point)

    point = lower_tangent.left_point
    while point != left_hull.left_most_point:  # Time: O(n) Space: O(1)
        merged_hull.points.append(point)
        point = point.clockwise
    return merged_hull  # Time: O(1) Space: O(1)


def merge_final_hulls(left_hull: Hull, right_hull: Hull) -> list[tuple[float, float]]:
    hull: Hull = merge_hulls(left_hull, right_hull)
    return hull.to_tuple_list()
    # return hull
