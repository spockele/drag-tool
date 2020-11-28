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
                      Line(self.left, self.top, self.left, self.bottom),
                      Line(self.right, self.top, self.right, self.bottom)
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

        self.slope = 0 if self.x2 == self.x1 else (self.y2 - self.y1) / (self.x2 - self.x1)

    def transform(self, shift_x, shift_y):
        return self.x1 + shift_x, self.y1 + shift_y, self.x2 + shift_x, self.y2 + shift_y


def intersection_rectangles(rectangle_1: Rectangle, rectangle_2: Rectangle):
    return


def sign(x):
    return -1 if x < 0 else 1


def line_length(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def intersection_line_circle(line: Line, circle: Circle):
    x1, y1, x2, y2 = line.transform(0 - circle.x_centre, 0 - circle.y_centre)

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
    return np.sqrt(s * (s - a) * (s - b) * (s - c))


def intersection_rectangle_circle(rectangle: Rectangle, circle: Circle):
    dx2_left = (rectangle.left - circle.x_centre) ** 2
    dx2_right = (rectangle.right - circle.x_centre) ** 2
    dy2_top = (rectangle.top - circle.y_centre) ** 2
    dy2_bottom = (rectangle.bottom - circle.y_centre) ** 2

    distances = (np.sqrt(dx2_left + dy2_top), np.sqrt(dx2_right + dy2_top),
                 np.sqrt(dx2_left + dy2_bottom), np.sqrt(dx2_right + dy2_bottom)
                 )

    inside_vertices = len([distance for distance in distances if distance < circle.radius])

    print(inside_vertices)

    if inside_vertices == 0:
        intersections = []
        for line in rectangle.lines:
            intersections.append(intersection_line_circle(line, circle))

        intersections = [intersection for intersection in intersections
                         if not isinstance(intersection, bool)]

        if intersections:
            return area_circular_segment(intersections[0], circle)
