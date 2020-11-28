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
    def test_no_inside_intersection(self):
        rectangle = shapes.Rectangle(0, 2, 2, 0)
        circle = shapes.Circle(1, 0, 1)

        expected_area = round(circle.area / 2, 3)

        self.assertEqual(shapes.intersection_rectangle_circle(rectangle, circle), expected_area)


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


if __name__ == '__main__':
    unittest.main()
