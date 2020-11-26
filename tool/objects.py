"""
Definition of all the object classes for the drag tool
"""

import numpy as np

from .equations import drag_coefficient_function


class Part:
    """
    The general aerodynamic model for all objects defined below
    """

    def __init__(self, drag_range: tuple, reynolds_number: int, dynamic_pressure: float,
                 position: tuple):
        self.dynamic_pressure = dynamic_pressure
        self.drag_coefficient = drag_coefficient_function(reynolds_number, drag_range)

        self.position = position
        self.x_centre = position[0]
        self.y_centre = position[1]
        self.z_centre = position[2]

    def frontal_surface(self, axis_1: int, axis_2: int):
        raise NotImplementedError("Cannot execute for base class Part")

    def smallest_coordinate(self, axis: int):
        raise NotImplementedError("Cannot execute for base class Part")

    def calculate_base_drag(self, direction: int):
        raise NotImplementedError("Cannot execute for base class Part")


class Sphere(Part):
    """
    Aerodynamic model for a sphere
        The reference area is the frontal area
    """
    drag_range = (0.09, 0.18)

    def __init__(self, reynolds_number: int, dynamic_pressure: float,
                 position: tuple, radius: float):
        self.radius = radius

        super().__init__(self.drag_range, reynolds_number, dynamic_pressure, position)

    def __repr__(self):
        return f"Sphere: [{self.position}, r={self.radius}]"

    def frontal_surface(self, axis_1: int, axis_2: int):
        """
        Determine the frontal surface on a given plane
        :param axis_1: First axis defining the plane
        :param axis_2: Second axis defining the plane
        :return: (The shape of the surface,
                The centre,
                The radius,
                The surface area)
        """
        centre = self.position[axis_1], self.position[axis_2]
        return "circle", centre, self.radius, np.pi * self.radius ** 2

    def smallest_coordinate(self, axis: int):
        return self.position[axis] - self.radius

    def calculate_base_drag(self, direction: int):
        return self.drag_coefficient * (np.pi * self.radius ** 2) * self.dynamic_pressure


class Cylinder(Part):
    """
    Aerodynamic model for a cylinder
        The reference area is the frontal area
        Orientation indicates along which axis the cylinder is aligned
    """
    drag_range = (0.3, 0.7)

    def __init__(self, reynolds_number: int, dynamic_pressure: float,
                 position: tuple, radius: float, length: float, orientation: int):
        self.radius = radius
        self.length = length
        self.orientation = orientation

        super().__init__(self.drag_range, reynolds_number, dynamic_pressure, position)

    def __repr__(self):
        return f"[Cylinder: {self.position}, r={self.radius}, l={self.length}, {self.orientation}]"

    def frontal_surface(self, axis_1: int, axis_2: int):
        """
        Determine the frontal surface on a given plane
        :param axis_1: First axis defining the plane
        :param axis_2: Second axis defining the plane
        :return: (The shape of the surface,
                Either the centre or the top left corner,
                Either the radius or the bottom right corner,
                The surface area)
        """
        if self.orientation == axis_1:
            top_left = (self.position[axis_1] - self.length / 2,
                        self.position[axis_2] + self.radius
                        )
            bottom_right = (self.position[axis_1] + self.length / 2,
                            self.position[axis_2] - self.radius
                            )

            return "rectangle", top_left, bottom_right, 2 * self.length * self.radius

        elif self.orientation == axis_2:
            top_left = (self.position[axis_1] - self.radius,
                        self.position[axis_2] + self.length / 2
                        )
            bottom_right = (self.position[axis_1] + self.radius,
                            self.position[axis_2] - self.length / 2
                            )

            return "rectangle", top_left, bottom_right, 2 * self.length * self.radius

        else:
            centre = self.position[axis_1], self.position[axis_2]
            return "circle", centre, self.radius, np.pi * self.radius ** 2

    def smallest_coordinate(self, axis: int):
        if self.orientation == axis:
            return self.position[axis] - self.length / 2

        else:
            return self.position[axis] - self.radius

    def calculate_base_drag(self, direction: int):
        if direction == self.orientation:
            return 0.9 * (np.pi * self.radius ** 2) * self.dynamic_pressure
        else:
            return self.drag_coefficient * (2 * self.length * self.radius) * self.dynamic_pressure


class Cuboid(Part):
    """
    Aerodynamic model for a cuboid part
        The reference area is the frontal area
    """
    drag_range = (0.9, 0.9)

    def __init__(self, reynolds_number: int, dynamic_pressure: float,
                 position: tuple, dimensions: tuple):
        self.dimensions = dimensions

        super().__init__(self.drag_range, reynolds_number, dynamic_pressure, position)

    def __repr__(self):
        return f"[Cuboid: {self.position}, dims={self.dimensions}]"

    def frontal_surface(self, axis_1: int, axis_2: int):
        top_left = (self.position[axis_1] - self.dimensions[axis_1] / 2,
                    self.position[axis_2] + self.dimensions[axis_2] / 2
                    )

        bottom_right = (self.position[axis_1] + self.dimensions[axis_1] / 2,
                        self.position[axis_2] - self.dimensions[axis_2] / 2
                        )

        return ("rectangle", top_left, bottom_right,
                self.dimensions[axis_1] * self.dimensions[axis_2]
                )

    def smallest_coordinate(self, axis: int):
        return self.position[axis] - self.dimensions[axis] / 2

    def calculate_base_drag(self, direction: int):
        [axis_1, axis_2] = [axis for axis in [0, 1, 2] if axis != direction]
        area = self.dimensions[axis_1] * self.dimensions[axis_2]
        return self.drag_coefficient * area * self.dynamic_pressure


class IceCreamCone(Part):
    """

    """
    drag_range = (0.05, 0.07)

    def __init__(self, reynolds_number: int, dynamic_pressure: float,
                 position: tuple, radius: float, ):
        super().__init__(self.drag_range, reynolds_number, dynamic_pressure,
                         position)
