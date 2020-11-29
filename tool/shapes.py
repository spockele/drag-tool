"""

"""

import numpy as np


class Rectangle:
    """

    """

    def __init__(self, left, right, top, bottom):
        self.left, self.right, self.top, self.bottom = left, right, top, bottom

        self.area = (self.right - self.left) * (self.top - self.bottom)

        self.lines = (Line(self.left, self.top, self.right, self.top),
                      Line(self.left, self.bottom, self.right, self.bottom),
                      Line(self.left, self.bottom, self.left, self.top),
                      Line(self.right, self.bottom, self.right, self.top)
                      )

    def __repr__(self):
        return f"Rectangle: [lr=({self.left}, {self.right}), tb=({self.top}, {self.bottom})]"


class Circle:
    """

    """

    def __init__(self, x_centre, y_centre, radius):
        self.x_centre, self.y_centre, self.radius = x_centre, y_centre, radius

        self.area = np.pi * self.radius ** 2


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


def intersection_rectangles(rectangle_1: Rectangle, rectangle_2: Rectangle):
    return


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


def on_line(line: Line, x, y):
    return line.x1 <= x <= line.x2 and line.y1 <= y <= line.y2


def intersection_rectangle_circle(rectangle: Rectangle, circle: Circle):
    inside_vertices, outside_vertices = find_inside_vertices(circle, rectangle)
    area = 0

    if len(inside_vertices) == 0:
        intersection, _ = find_intersection(circle, rectangle)

        if len(intersection) == 4:
            area = area_circular_segment(intersection, circle)

        elif len(intersection) == 8:
            circular_area1 = area_circular_segment(intersection[0:4], circle)
            circular_area2 = area_circular_segment(intersection[4:8], circle)

            area = circle.area - circular_area1 - circular_area2

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
                        if not distance < circle.radius]

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

    return intersection, intersect_lines
