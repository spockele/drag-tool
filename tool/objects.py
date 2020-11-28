"""
Definition of all the object classes for the drag tool
"""

import numpy as np

from .equations import drag_coefficient_function
from .shapes import Rectangle, Circle


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

        self._smallest_coordinate = None
        self._frontal_surface = None

    def set_frontal_surface(self, axis_1: int, axis_2: int):
        raise NotImplementedError("Cannot execute for base class Part")

    def get_frontal_surface(self):
        return self._frontal_surface

    def set_smallest_coordinate(self, axis: int):
        raise NotImplementedError("Cannot execute for base class Part")

    def get_smallest_coordinate(self):
        return self._smallest_coordinate

    def calculate_base_drag(self, direction: int):
        raise NotImplementedError("Cannot execute for base class Part")

    def __lt__(self, other):
        if not isinstance(other, Part):
            raise TypeError(f"Cannot compare Part to {type(other)}")

        elif self._smallest_coordinate is None:
            return AttributeError(f"Smallest coordinate of first Part not determined yet")

        elif other.get_smallest_coordinate is None:
            return AttributeError(f"Smallest coordinate of first Part not determined yet")

        else:
            return self._smallest_coordinate < other._smallest_coordinate


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

    def set_frontal_surface(self, axis_1: int, axis_2: int):
        """
        Determine the frontal surface on a given plane
        :param axis_1: First axis defining the plane
        :param axis_2: Second axis defining the plane
        :return: None
        """
        self._frontal_surface = Circle(self.position[axis_1], self.position[axis_2], self.radius)

    def set_smallest_coordinate(self, axis: int):
        self._smallest_coordinate = self.position[axis] - self.radius

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

    def set_frontal_surface(self, axis_1: int, axis_2: int):
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
            left = self.position[axis_1] - self.length / 2,
            top = self.position[axis_2] + self.radius
            right = self.position[axis_1] + self.length / 2
            bottom = self.position[axis_2] - self.radius

            self._frontal_surface = Rectangle(left, right, top, bottom)

        elif self.orientation == axis_2:
            left = self.position[axis_1] - self.radius
            top = self.position[axis_2] + self.length / 2
            right = self.position[axis_1] + self.radius
            bottom = self.position[axis_2] - self.length / 2

            area = 2 * self.length * self.radius

            self._frontal_surface = Rectangle(left, right, top, bottom)

        else:
            self._frontal_surface = Circle(self.position[axis_1], self.position[axis_2],
                                           self.radius)

    def set_smallest_coordinate(self, axis: int):
        if self.orientation == axis:
            self._smallest_coordinate = self.position[axis] - self.length / 2

        else:
            self._smallest_coordinate = self.position[axis] - self.radius

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

    def set_frontal_surface(self, axis_1: int, axis_2: int):
        left = self.position[axis_1] - self.dimensions[axis_1] / 2
        top = self.position[axis_2] + self.dimensions[axis_2] / 2
        right = self.position[axis_1] + self.dimensions[axis_1] / 2
        bottom = self.position[axis_2] - self.dimensions[axis_2] / 2

        area = self.dimensions[axis_1] * self.dimensions[axis_2]

        self._frontal_surface = Rectangle(left, right, top, bottom)

    def set_smallest_coordinate(self, axis: int):
        self._smallest_coordinate = self.position[axis] - self.dimensions[axis] / 2

    def calculate_base_drag(self, direction: int):
        [axis_1, axis_2] = [axis for axis in [0, 1, 2] if axis != direction]
        area = self.dimensions[axis_1] * self.dimensions[axis_2]
        return self.drag_coefficient * area * self.dynamic_pressure


class IceCreamCone(Part):
    """

    """
    drag_range = (0.05, 0.07)

    def __init__(self, reynolds_number: int, dynamic_pressure: float,
                 position: tuple, radius: float, length_cylinder: float, length_cone: float,
                 orientation: int):
        self.radius = radius
        self.length_cylinder = length_cylinder
        self.length_cone = length_cone
        self.orientation = orientation

        super().__init__(self.drag_range, reynolds_number, dynamic_pressure,
                         position)

    def __repr__(self):
        return f"[IceCream cone: r={self.radius}, l_co={self.length_cylinder}, " \
               f"l_co={self.length_cone}, {self.orientation}]"

    def set_frontal_surface(self, axis_1: int, axis_2: int):
        if self.orientation not in (axis_1, axis_2):
            self._frontal_surface = Circle(self.position[axis_1], self.position[axis_2],
                                           self.radius)

        else:
            raise ValueError(f"Frontal surface calculation in {axis_1}{axis_2} plane not "
                             f"supported for IceCreamCone")

    def set_smallest_coordinate(self, axis: int):
        self._smallest_coordinate = self.position[axis] - self.radius

    def calculate_base_drag(self, direction: int):
        if self.orientation == direction:
            volume = (2 * np.pi * self.radius ** 3) / 3 + \
                     (np.pi * self.radius ** 2) * self.length_cylinder + \
                     (np.pi * self.length_cone * self.radius ** 2) / 3

            return self.drag_coefficient * (volume ** (2 / 3)) * self.dynamic_pressure

        else:
            raise ValueError(f"Drag calculation along {direction} axis not supported for "
                             f"IceCreamCone")
