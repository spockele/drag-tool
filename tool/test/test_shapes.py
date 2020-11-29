import unittest


import numpy as np

from .. import shapes


class TestIntersectionLineCircle(unittest.TestCase):
    def test_does_intersect(self):
        line = shapes.Line(0, 0, 2, 0)
        circle = shapes.Circle(1, 0, 0.5)

        intersection = shapes.intersection_line_circle(line, circle)

        self.assertEqual(intersection, (1.5, 0, 0.5, 0))

        line = shapes.Line(0, 2, 2, 0)
        circle = shapes.Circle(1, 1, 1)

        intersection = shapes.intersection_line_circle(line, circle)
        expected_intersection = (round(1 + np.cos(np.pi/4), 3), round(1 - np.sin(np.pi/4), 3),
                                 round(1 - np.cos(np.pi/4), 3), round(1 + np.sin(np.pi/4), 3)
                                 )

        self.assertEqual(intersection, expected_intersection)

        line = shapes.Line(0, 0, 0, 2)
        circle = shapes.Circle(0, 1, 0.5)

        intersection = shapes.intersection_line_circle(line, circle)

        self.assertEqual(intersection, (0, 1.5, 0, 0.5))

    def test_tangent(self):
        line = shapes.Line(0, 0, 2, 0)
        circle = shapes.Circle(1, 1, 1)

        intersection = shapes.intersection_line_circle(line, circle)

        self.assertTrue(intersection)

    def test_no_intersection(self):
        line = shapes.Line(0, 2, 3, 3)
        circle = shapes.Circle(1, 0, 1)

        intersection = shapes.intersection_line_circle(line, circle)

        self.assertFalse(intersection)


class TestIntersectionRectangleCircle(unittest.TestCase):
    def test_no_vertex_with_intersection(self):
        rectangle = shapes.Rectangle(0, 2, 2, 0)
        circle = shapes.Circle(1, 0, 1)

        expected_area = round(circle.area / 2, 3)

        self.assertEqual(shapes.intersection_rectangle_circle(rectangle, circle), expected_area)

    def test_no_vertex_double_intersection(self):
        rectangle = shapes.Rectangle(-1, 1, 4, -4)
        circle = shapes.Circle(0, 0, 2)

        expected_area = 4 * np.sqrt(3) + 2 * (circle.area * 1.047 / (2 * np.pi) - np.sqrt(3))

        self.assertEqual(round(shapes.intersection_rectangle_circle(rectangle, circle), 2),
                         round(expected_area, 2))

        rectangle = shapes.Rectangle(-4, 4, 1, -1)
        self.assertEqual(round(shapes.intersection_rectangle_circle(rectangle, circle), 2),
                         round(expected_area, 2))

    def test_no_vertex_circle_inside(self):
        rectangle = shapes.Rectangle(-2, 2, 2, -2)
        circle = shapes.Circle(0, 0, 1)

        self.assertEqual(shapes.intersection_rectangle_circle(rectangle, circle),
                         round(circle.area, 3))

    def test_one_inside_vertex(self):
        rectangle = shapes.Rectangle(0, 2, 2, 0)
        circle = shapes.Circle(0, 0, 1)

        self.assertEqual(shapes.intersection_rectangle_circle(rectangle, circle),
                         round(0.25 * circle.area, 3))

    def test_two_inside_vertex(self):
        rectangle = shapes.Rectangle(0, 3, 1, 0)
        circle = shapes.Circle(0, 0, 2)

        helper_rectangle1 = shapes.Rectangle(0, 3, 3, 0)
        helper_rectangle2 = shapes.Rectangle(0, 3, 3, 1)
        expected_area = shapes.intersection_rectangle_circle(helper_rectangle1, circle) -\
            shapes.intersection_rectangle_circle(helper_rectangle2, circle)

        self.assertEqual(shapes.intersection_rectangle_circle(rectangle, circle), expected_area)

    def test_three_inside_vertex(self):
        rectangle = shapes.Rectangle(0, 1.8, 1.8, 0)
        circle = shapes.Circle(0, 0, 2)

        expected_area = rectangle.area - 0.431 + 0.1064 * circle.area - 1.2397

        self.assertEqual(round(shapes.intersection_rectangle_circle(rectangle, circle), 2),
                         round(expected_area, 2))

    def test_four_inside_vertex(self):
        rectangle = shapes.Rectangle(-1, 1, 1, -1)
        circle = shapes.Circle(0, 0, 2)

        self.assertEqual(shapes.intersection_rectangle_circle(rectangle, circle),
                         round(rectangle.area, 3))


class TestAreaCircularSegment(unittest.TestCase):
    def test_half_area(self):
        circle = shapes.Circle(0, 0, 1)
        intersection = (-1, 0, 1, 0)

        expected_area = round(0.5 * circle.area, 3)

        self.assertEqual(shapes.area_circular_segment(intersection, circle), expected_area)

    def test_quarter_area(self):
        circle = shapes.Circle(0, 0, 1)
        intersection = (-np.cos(np.pi/4), np.sin(np.pi/4), np.cos(np.pi/4), np.sin(np.pi/4))

        expected_area = round(0.25 * circle.area - 0.5 * np.sin(np.pi/4) * 2 * np.cos(np.pi/4), 3)

        self.assertEqual(shapes.area_circular_segment(intersection, circle), expected_area)


class TestAreaTriangle(unittest.TestCase):
    def test_equilateral(self):
        sides = 1, 1, 1

        self.assertEqual(shapes.area_triangle(*sides), round(0.25 * np.sqrt(3), 3))

    def test_isosceles(self):
        sides = 1, 2, 2

        self.assertEqual(shapes.area_triangle(*sides), round(0.25 * np.sqrt(15), 3))

    def test_other(self):
        sides = 3, 4, 5

        self.assertEqual(shapes.area_triangle(*sides), 6)


if __name__ == '__main__':
    unittest.main()
