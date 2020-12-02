"""

"""

import numpy as np


class ConeSideSurface:
    """

    """

    def __init__(self, geometric_centre, area):
        self.geometric_centre = geometric_centre
        self.area = area

    def intersection(self, other):
        raise NotImplementedError(f"The intersection with a general surface cannot be calculated.")


class Rectangle:
    """

    """

    def __init__(self, left, right, top, bottom):
        self.left, self.right, self.top, self.bottom = left, right, top, bottom

        self.area = round((self.right - self.left) * (self.top - self.bottom), 3)

        self.lines = (Line(self.left, self.top, self.right, self.top),
                      Line(self.left, self.bottom, self.right, self.bottom),
                      Line(self.left, self.bottom, self.left, self.top),
                      Line(self.right, self.bottom, self.right, self.top)
                      )

    def __repr__(self):
        return f"Rectangle: [lr=({self.left}, {self.right}), tb=({self.top}, {self.bottom})]"

    def in_rectangle_x(self, x):
        return self.left <= x <= self.right

    def in_rectangle_y(self, y):
        return self.bottom <= y <= self.top

    def intersection(self, other):
        if isinstance(other, Rectangle):
            return intersection_rectangles(other, self)
        elif isinstance(other, Circle):
            return intersection_rectangle_circle(self, other)
        else:
            raise TypeError(f"Cannot calculate intersection of Rectangle and {type(other)}")


class Circle:
    """

    """

    def __init__(self, x_centre, y_centre, radius):
        self.x_centre, self.y_centre, self.radius = x_centre, y_centre, radius

        self.area = round(np.pi * self.radius ** 2, 3)

    def __repr__(self):
        return f"Circle: [{(self.x_centre, self.y_centre)}, r={self.radius}]"

    def __eq__(self, other):
        if isinstance(other, Circle):
            return self.radius == other.radius
        else:
            raise TypeError(f"Cannot compare Circle to {type(other)}")

    def __lt__(self, other):
        if isinstance(other, Circle):
            return self.radius < other.radius
        else:
            raise TypeError(f"Cannot compare Circle to {type(other)}")

    def __le__(self, other):
        return self < other or self == other

    def transform(self, x_shift, y_shift):
        return self.x_centre + x_shift, self.y_centre + y_shift

    def in_circle_x(self, x):
        return self.x_centre - self.radius < x < self.x_centre + self.radius

    def in_circle_y(self, y):
        return self.y_centre - self.radius < y < self.y_centre + self.radius

    def on_circle(self, x, y):
        return line_length(self.x_centre, self.y_centre, x, y) <= self.radius

    def intersection(self, other):
        if isinstance(other, Rectangle):
            return intersection_rectangle_circle(other, self)
        elif isinstance(other, Circle):
            return intersection_circle_circle(other, self)
        else:
            raise TypeError(f"Cannot calculate intersection of Circle and {type(other)}")


class Line:
    """

    """

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2

        self.slope = None if self.x2 == self.x1 else (self.y2 - self.y1) / (self.x2 - self.x1)

    def __repr__(self):
        return f"Line: [{self.x1}, {self.y1}, {self.x2}, {self.y2}, s={self.slope}]"

    def transform(self, shift_x, shift_y):
        return self.x1 + shift_x, self.y1 + shift_y, self.x2 + shift_x, self.y2 + shift_y


def on_line(line: Line, x, y):
    return line.x1 <= x <= line.x2 and line.y1 <= y <= line.y2


def sign(x):
    return -1 if x < 0 else 1


def line_length(x1, y1, x2, y2):
    return round(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 3)


def intersection_line_circle(line: Line, circle: Circle):
    x1, y1, x2, y2 = line.transform(0 - circle.x_centre, 0 - circle.y_centre)

    if line.slope is None and np.abs(x1) < circle.radius:
        return (x1 + circle.x_centre, np.sqrt(circle.radius ** 2 - x1 ** 2) + circle.y_centre,
                x2 + circle.x_centre, -np.sqrt(circle.radius ** 2 - x1 ** 2) + circle.y_centre)

    elif line.slope is None:
        return np.abs(x1) == circle.radius

    else:
        a = line.slope ** 2 + 1
        b = 2 * (line.slope * y1 - x1 * line.slope ** 2)
        c = (line.slope * x1 - y1) ** 2 - circle.radius ** 2

        discriminant = b ** 2 - 4 * a * c

        if discriminant <= 0:
            return discriminant == 0
        else:
            x1_int = (np.sqrt(discriminant) - b) / (2 * a)
            x2_int = (-np.sqrt(discriminant) - b) / (2 * a)

            y1_int = line.slope * (x1_int - x1) + y1
            y2_int = line.slope * (x2_int - x1) + y1

            return (round(x1_int + circle.x_centre, 3), round(y1_int + circle.y_centre, 3),
                    round(x2_int + circle.x_centre, 3), round(y2_int + circle.y_centre, 3))


def area_circular_segment(intersection, circle: Circle):
    a = line_length(*intersection)
    r = np.sqrt(circle.radius ** 2 - 0.25 * a ** 2)
    theta = 2 * np.arcsin(0.5 * a / circle.radius)

    return round(circle.area * theta / (2 * np.pi) - 0.5 * r * a, 3)


def area_triangle(a, b, c):
    s = (a + b + c) / 2
    return round(np.sqrt(s * (s - a) * (s - b) * (s - c)), 3)


def find_inside_vertices(circle, rectangle):
    dx2_left = (rectangle.left - circle.x_centre) ** 2
    dx2_right = (rectangle.right - circle.x_centre) ** 2
    dy2_top = (rectangle.top - circle.y_centre) ** 2
    dy2_bottom = (rectangle.bottom - circle.y_centre) ** 2

    distances = (np.sqrt(dx2_left + dy2_top), np.sqrt(dx2_right + dy2_top),
                 np.sqrt(dx2_left + dy2_bottom), np.sqrt(dx2_right + dy2_bottom)
                 )

    vertices = ((rectangle.left, rectangle.top), (rectangle.right, rectangle.top),
                (rectangle.left, rectangle.bottom), (rectangle.right, rectangle.bottom)
                )

    inside_vertices = [vertices[i] for i, distance in enumerate(distances)
                       if distance < circle.radius]

    outside_vertices = [vertices[i] for i, distance in enumerate(distances)
                        if not distance >= circle.radius]

    return inside_vertices, outside_vertices


def find_intersection(circle, rectangle):
    intersection = []
    intersect_lines = []

    for line in rectangle.lines:
        intersect = intersection_line_circle(line, circle)

        if isinstance(intersect, tuple):

            if on_line(line, intersect[0], intersect[1]):
                intersection.append(intersect[0])
                intersection.append(intersect[1])
                intersect_lines.append(line)

            if on_line(line, intersect[2], intersect[3]):
                intersection.append(intersect[2])
                intersection.append(intersect[3])
                intersect_lines.append(line)

    result = find_double_intersections(intersection)

    return result, intersect_lines


def find_double_intersections(intersection):
    intersects = []
    result = []
    for index, _ in enumerate(intersection[::2]):
        intersect = round(intersection[2 * index], 3), round(intersection[2 * index + 1], 3)
        if intersect not in intersects:
            intersects.append(intersect)
            result += [*intersect]
    return result


def circle_no_intersection(circle1, circle2):
    distance_centres = line_length(circle1.x_centre, circle1.y_centre,
                                   circle2.x_centre, circle2.y_centre)
    if circle1 < circle2:
        area = circle1.area if distance_centres < circle2.radius else 0

    elif circle2 < circle1:
        area = circle2.area if distance_centres < circle1.radius else 0

    else:
        area = 0

    return area


def intersection_rectangle_circle(rectangle: Rectangle, circle: Circle):
    inside_vertices, outside_vertices = find_inside_vertices(circle, rectangle)

    if len(inside_vertices) == 0:
        intersection, _ = find_intersection(circle, rectangle)

        if len(intersection) == 4:
            area = area_circular_segment(intersection, circle)

        elif len(intersection) > 4:
            subtract_area = 0
            for index in range(len(intersection) // 4):
                intersect = intersection[4*index:4*index+4]
                subtract_area += area_circular_segment(intersect, circle)

            area = circle.area - subtract_area

        elif (rectangle.left < circle.x_centre < rectangle.right
              and rectangle.bottom < circle.y_centre < rectangle.top):
            area = circle.area

        else:
            area = 0

    elif len(inside_vertices) == 1:
        intersection, _ = find_intersection(circle, rectangle)

        circular_area = area_circular_segment(intersection, circle)
        p1 = intersection[0:2]
        p2 = intersection[2:4]
        p3 = inside_vertices[0]

        lengths = line_length(*intersection), line_length(*p2, *p3), line_length(*p1, *p3)
        triangle_area = area_triangle(*lengths)

        area = circular_area + triangle_area

    elif len(inside_vertices) == 2:
        intersection, intersect_lines = find_intersection(circle, rectangle)
        circular_area = area_circular_segment(intersection, circle)

        p1 = intersection[0], intersection[1]
        p2 = intersection[2], intersection[3]

        p3 = inside_vertices[0]
        p4 = inside_vertices[1]

        a1 = line_length(*intersection)
        b1 = line_length(*p1, *p4)
        c1 = line_length(*p2, *p4)
        triangle_area1 = area_triangle(a1, b1, c1)

        a2 = line_length(*p1, *p3)
        b2 = line_length(*p1, *p4)
        c2 = line_length(*p3, *p4)
        triangle_area2 = area_triangle(a2, b2, c2)

        area = circular_area + triangle_area1 + triangle_area2

    elif len(inside_vertices) == 3:
        intersection, _ = find_intersection(circle, rectangle)

        circular_area = area_circular_segment(intersection, circle)
        a = line_length(*intersection)
        b = line_length(intersection[0], intersection[1], *outside_vertices[0])
        c = line_length(intersection[2], intersection[3], *outside_vertices[0])
        triangle_area = area_triangle(a, b, c)

        area = rectangle.area - triangle_area + circular_area

    else:
        area = rectangle.area

    return round(area, 3)


def intersection_circle_circle(circle1: Circle, circle2: Circle):
    x1, y1 = circle1.transform(-circle2.x_centre, -circle2.y_centre)

    if x1 == y1 == 0:
        area = circle1.area if circle1 <= circle2 else circle2.area

    elif y1 == 0:
        x = (1 / (2 * x1)) * (x1 ** 2 + circle2.radius ** 2 - circle1.radius ** 2)

        if circle1.in_circle_x(x) and circle2.in_circle_x(x):
            y_abs1 = np.sqrt((circle1.radius ** 2) - (x - x1) ** 2)
            y_abs2 = np.sqrt((circle2.radius ** 2) - x ** 2)

            if y_abs1 == y_abs2 != 0:
                intersection = (x, y_abs1, x, -y_abs1)

                area = (area_circular_segment(intersection, circle1) +
                        area_circular_segment(intersection, circle2))

            else:
                area = circle_no_intersection(circle1, circle2)

        else:
            area = circle_no_intersection(circle1, circle2)

    else:
        p = (1 / (2 * y1) * (x1 ** 2 + y1 ** 2 - circle1.radius ** 2 + circle2.radius ** 2))

        a = 2
        b = -2 * p * (x1 / y1)
        c = p ** 2 - circle2.radius ** 2

        discriminant = b ** 2 - 4 * a * c

        if discriminant <= 0:
            area = circle_no_intersection(circle1, circle2)

        else:
            x1_int = (-b + np.sqrt(discriminant)) / (2 * a)
            y1_int = - (circle1.x_centre / circle1.y_centre) * x1_int + p

            x2_int = (-b - np.sqrt(discriminant)) / (2 * a)
            y2_int = - (circle1.x_centre / circle1.y_centre) * x2_int + p

            if (circle1.on_circle(x1_int, y1_int) and circle2.on_circle(x1_int, y1_int) and
                    circle1.on_circle(x2_int, y2_int) and circle2.on_circle(x2_int, y2_int)):

                intersection = [x1_int, y1_int, x2_int, y2_int]
                circular_area1 = area_circular_segment(intersection, circle1)
                circular_area2 = area_circular_segment(intersection, circle2)

                area = circular_area1 + circular_area2

            else:
                area = 0

    return round(area, 3)


def intersection_rectangles(rectangle_1: Rectangle, rectangle_2: Rectangle):
    left = max(rectangle_1.left, rectangle_2.left)
    right = min(rectangle_1.right, rectangle_2.right)
    bottom = max(rectangle_1.bottom, rectangle_2.bottom)
    top = min(rectangle_1.top, rectangle_2.top)

    in_rectangle1 = (rectangle_1.in_rectangle_x(left) and rectangle_1.in_rectangle_x(right) and
                     rectangle_1.in_rectangle_y(top) and rectangle_1.in_rectangle_y(bottom)
                     )
    in_rectangle2 = (rectangle_2.in_rectangle_x(left) and rectangle_2.in_rectangle_x(right) and
                     rectangle_2.in_rectangle_y(top) and rectangle_2.in_rectangle_y(bottom)
                     )

    if in_rectangle1 and in_rectangle2:
        overlap = Rectangle(left, right, top, bottom)
        area = overlap.area
    else:
        area = 0

    return area
