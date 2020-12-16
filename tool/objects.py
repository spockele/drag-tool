"""
Definition of all the object classes for the drag tool
"""

import numpy as np

from .shapes import ConeSideSurface, Rectangle, Circle


class Part:
    """
    The general aerodynamic model for all objects defined below
    """
    friction_coefficient = 0.02

    def __init__(self, density: float, velocity: float, position: tuple, wet_area: float):
        self.velocity = velocity
        self.dynamic_pressure = 0.5 * density * self.velocity ** 2

        self.slowdown = 1
        self.wake_slowdown = 1
        self.wake_factor = 1
        self.largest_intersection = 0

        self.wet_area = wet_area

        self.position = position
        self.x_centre = position[0]
        self.y_centre = position[1]
        self.z_centre = position[2]

        self._smallest_coordinate = None
        self._frontal_surface = None
        self._characteristic_length = None
        self.drag = None

        self.__name__ = "Part"

    def set_slowdown(self, slowdown: float, area: float):
        self.slowdown = slowdown
        self.wake_slowdown = ((self.slowdown * area +
                               self._frontal_surface.area - area) /
                              self._frontal_surface.area)
        self.wake_factor = (((self.slowdown ** 2) * area +
                             self._frontal_surface.area - area) /
                            self._frontal_surface.area)

    def apply_slowdown(self, direction: int):
        base_drag = self.calculate_base_drag(direction)
        friction_drag = min(self.friction_coefficient * self.wet_area * self.dynamic_pressure,
                            base_drag)
        pressure_drag = self.wake_factor * (base_drag - friction_drag)

        self.drag = friction_drag + pressure_drag

    def set_largest_intersection(self, area):
        self.largest_intersection = area if area > self.largest_intersection \
            else self.largest_intersection

    def set_frontal_surface(self, axis_1: int, axis_2: int):
        raise NotImplementedError("Cannot execute for base class Part")

    def get_frontal_surface(self):
        return self._frontal_surface

    def set_smallest_coordinate(self, axis: int):
        raise NotImplementedError("Cannot execute for base class Part")

    def get_smallest_coordinate(self):
        return self._smallest_coordinate

    def set_characteristic_length(self, axis: int):
        raise NotImplementedError("Cannot execute for base class Part")

    def get_characteristic_length(self):
        return self._characteristic_length

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
    drag_coefficient = 0.15

    def __init__(self, density: float, velocity: float, position: tuple, radius: float,
                 name="Sphere"):
        self.radius = radius
        wet_area = 4 * np.pi * self.radius ** 2

        super().__init__(density, velocity, position, wet_area)

        self.__name__ = name

    def __repr__(self):
        return f"{self.__name__}: [{self.position}, r={self.radius}]"

    def set_frontal_surface(self, axis_1: int, axis_2: int):
        """
        Determine the frontal surface on a given plane
        :param axis_1: First axis defining the plane
        :param axis_2: Second axis defining the plane
        :return: None
        """
        self._frontal_surface = Circle(round(self.position[axis_1], 3),
                                       round(self.position[axis_2], 3),
                                       self.radius)

    def set_smallest_coordinate(self, axis: int):
        self._smallest_coordinate = self.position[axis] - self.radius

    def set_characteristic_length(self, axis: int):
        self._characteristic_length = 2 * self.radius

    def calculate_base_drag(self, direction: int):
        return self.drag_coefficient * (np.pi * self.radius ** 2) * self.dynamic_pressure


class Cylinder(Part):
    """
    Aerodynamic model for a cylinder
        The reference area is the frontal area
        Orientation indicates along which axis the cylinder is aligned
    """
    drag_coefficient = 0.4

    def __init__(self, density: float, velocity: float, position: tuple, radius: float,
                 length: float, orientation: int, name="Cylinder"):
        self.radius = radius
        self.length = length
        self.orientation = orientation

        wet_area = 2 * np.pi * self.radius ** 2 + 2 * np.pi * self.radius * self.length

        super().__init__(density, velocity, position, wet_area)

        self.__name__ = name

    def __repr__(self):
        return f"{self.__name__}: [{self.position}, r={self.radius}, l={self.length}, {self.orientation}]"

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
            left = round(self.position[axis_1] - self.length / 2, 3)
            top = round(self.position[axis_2] + self.radius, 3)
            right = round(self.position[axis_1] + self.length / 2, 3)
            bottom = round(self.position[axis_2] - self.radius, 3)

            self._frontal_surface = Rectangle(left, right, top, bottom)

        elif self.orientation == axis_2:
            left = round(self.position[axis_1] - self.radius, 3)
            top = round(self.position[axis_2] + self.length / 2, 3)
            right = round(self.position[axis_1] + self.radius, 3)
            bottom = round(self.position[axis_2] - self.length / 2, 3)

            self._frontal_surface = Rectangle(left, right, top, bottom)

        else:
            self._frontal_surface = Circle(round(self.position[axis_1], 3),
                                           round(self.position[axis_2], 3),
                                           self.radius)

    def set_smallest_coordinate(self, axis: int):
        if self.orientation == axis:
            self._smallest_coordinate = self.position[axis] - self.length / 2

        else:
            self._smallest_coordinate = self.position[axis] - self.radius

    def set_characteristic_length(self, axis: int):
        if self.orientation == axis:
            self._characteristic_length = self.length
        else:
            self._characteristic_length = 2 * self.radius

    def calculate_base_drag(self, direction: int):
        if direction == self.orientation:
            return Cuboid.drag_coefficient * (np.pi * self.radius ** 2) * self.dynamic_pressure
        else:
            return self.drag_coefficient * (2 * self.length * self.radius) * self.dynamic_pressure


class Cuboid(Part):
    """
    Aerodynamic model for a cuboid part
        The reference area is the frontal area
    """
    drag_coefficient = 0.8

    def __init__(self, density: float, velocity: float, position: tuple, dimensions: tuple,
                 name="Cuboid"):
        self.dimensions = dimensions

        wet_area = 2 * (self.dimensions[0] * self.dimensions[1] +
                        self.dimensions[1] * self.dimensions[2] +
                        self.dimensions[0] * self.dimensions[2]
                        )

        super().__init__(density, velocity, position, wet_area)

        self.__name__ = name

    def __repr__(self):
        return f"{self.__name__}: [{self.position}, dims={self.dimensions}]"

    def set_frontal_surface(self, axis_1: int, axis_2: int):
        left = round(self.position[axis_1] - self.dimensions[axis_1] / 2, 3)
        top = round(self.position[axis_2] + self.dimensions[axis_2] / 2, 3)
        right = round(self.position[axis_1] + self.dimensions[axis_1] / 2, 3)
        bottom = round(self.position[axis_2] - self.dimensions[axis_2] / 2, 3)

        self._frontal_surface = Rectangle(left, right, top, bottom)

    def set_smallest_coordinate(self, axis: int):
        self._smallest_coordinate = self.position[axis] - self.dimensions[axis] / 2

    def set_characteristic_length(self, axis: int):
        self._characteristic_length = self.dimensions[axis]

    def calculate_base_drag(self, direction: int):
        [axis_1, axis_2] = [axis for axis in [0, 1, 2] if axis != direction]
        area = self.dimensions[axis_1] * self.dimensions[axis_2]
        return self.drag_coefficient * area * self.dynamic_pressure


class IceCreamCone(Part):
    """

    """
    drag_coefficient = 0.05

    def __init__(self, density: float, velocity: float, position: tuple, radius: float,
                 length_cylinder: float, length_cone: float, orientation: int, name="IceCreamCone"):
        self.radius = radius
        self.length_cylinder = length_cylinder
        self.length_cone = length_cone
        self.orientation = orientation

        wet_area = (2 * np.pi * self.radius ** 2 +
                    2 * np.pi * self.radius * self.length_cylinder +
                    np.pi * self.radius * np.sqrt(self.length_cone ** 2 + self.radius ** 2))

        super().__init__(density, velocity, position, wet_area)

        self.__name__ = name

    def __repr__(self):
        return f"{self.__name__}: [{self.position}, r={self.radius}, l_co={self.length_cylinder}, " \
               f"l_co={self.length_cone}, {self.orientation}]"

    def set_frontal_surface(self, axis_1: int, axis_2: int):
        if self.orientation not in (axis_1, axis_2):
            self._frontal_surface = Circle(round(self.position[axis_1], 3),
                                           round(self.position[axis_2], 3),
                                           self.radius)

        elif self.orientation in (axis_1, axis_2):
            area = (0.5 * np.pi * self.radius ** 2,
                    2 * self.radius * self.length_cylinder,
                    self.radius * self.length_cone)

            x = (-4 * self.radius / (3 * np.pi),
                 0.5 * self.length_cylinder,
                 self.length_cylinder + self.length_cone / 3)

            centroid = sum([a * x[i] for i, a in enumerate(area)]) / sum(area)

            if self.orientation == axis_1:
                left = self.position[axis_1] - self.radius
                right = self.position[axis_1] + self.length_cylinder + self.length_cone
                top = self.position[axis_2] + self.radius
                bottom = self.position[axis_2] - self.radius

            elif self.orientation == axis_2:
                bottom = self.position[axis_1] - self.radius
                top = self.position[axis_1] + self.length_cylinder + self.length_cone
                right = self.position[axis_2] + self.radius
                left = self.position[axis_2] - self.radius

            else:
                left, right, top, bottom = 0., 0., 0., 0.

            self._frontal_surface = ConeSideSurface(centroid, sum(area), left, right, top, bottom)

        else:
            raise ValueError(f"Frontal surface calculation in {axis_1}{axis_2} plane not "
                             f"supported for IceCreamCone")

    def set_smallest_coordinate(self, axis: int):
        self._smallest_coordinate = self.position[axis] - self.radius

    def set_characteristic_length(self, axis: int):
        if self.orientation == axis:
            self._characteristic_length = self.length_cone + self.length_cylinder + self.radius

        else:
            self._characteristic_length = 2 * self.radius

    def calculate_base_drag(self, direction: int):
        if self.orientation == direction:
            volume = (2 * np.pi * self.radius ** 3) / 3 + \
                     (np.pi * self.radius ** 2) * self.length_cylinder + \
                     (np.pi * self.length_cone * self.radius ** 2) / 3

            return self.drag_coefficient * (volume ** (2 / 3)) * self.dynamic_pressure

        else:
            return Cylinder.drag_coefficient * self._frontal_surface.area * self.dynamic_pressure


class Disk(Part):
    """

    """

    def __init__(self, density: float, velocity: float, position: tuple, radius: float,
                 orientation: tuple, name="Disk"):
        self.radius = radius
        self.orientation = orientation
        self.wet_area = 2 * np.pi * self.radius ** 2

        super().__init__(density, velocity, position, self.wet_area)

        self.friction_coefficient = 0.005

        self.__name__ = name

    def __repr__(self):
        return f"{self.__name__}: [{self.position}, r={self.radius}, {self.orientation}]"

    def set_frontal_surface(self, axis_1: int, axis_2: int):
        if axis_1 in self.orientation and axis_2 in self.orientation:
            self._frontal_surface = Circle(round(self.position[axis_1], 3),
                                           round(self.position[axis_2], 3),
                                           self.radius)
        elif axis_1 in self.orientation:
            left = round(self.position[axis_1] - self.radius, 3)
            right = round(self.position[axis_1] + self.radius, 3)
            top = round(self.position[axis_2] + 0.005, 3)
            bottom = round(self.position[axis_2] - 0.005, 3)
            self._frontal_surface = Rectangle(left, right, top, bottom)

        else:
            left = round(self.position[axis_2] - 0.005, 3)
            right = round(self.position[axis_2] + 0.005, 3)
            top = round(self.position[axis_1] + self.radius, 3)
            bottom = round(self.position[axis_1] - self.radius, 3)
            self._frontal_surface = Rectangle(left, right, top, bottom)

    def set_smallest_coordinate(self, axis: int):
        if axis in self.orientation:
            self._smallest_coordinate = self.position[axis] - self.radius
        else:
            self._smallest_coordinate = self.position[axis] - 0.005

    def set_characteristic_length(self, axis: int):
        if axis in self.orientation:
            self._characteristic_length = 2 * self.radius
        else:
            self._characteristic_length = 0.01

    def calculate_base_drag(self, direction: int):
        if direction in self.orientation:
            return self.friction_coefficient * self.wet_area * self.dynamic_pressure
        else:
            raise ValueError(f"Drag calculation along {direction} axis not supported for "
                             f"Disk")
