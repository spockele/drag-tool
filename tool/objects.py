"""
Definition of all the object classes for the drag tool
"""


from .equations import drag_coefficient_function


class Object:
    """
    The general aerodynamic model for all objects defined below
    """
    def __init__(self, drag_range: tuple, reynolds_number: int, position: tuple):
        self.drag_coefficient = drag_coefficient_function(reynolds_number, drag_range)

        self.x_centre = position[0]
        self.y_centre = position[1]
        self.z_centre = position[2]


class Sphere(Object):
    """
    Aerodynamic model for a sphere
        The reference area is the frontal area
    """
    drag_range = (0.09, 0.18)

    def __init__(self, reynolds_number: int, position: tuple):
        super().__init__(self.drag_range, reynolds_number, position)


class Cylinder(Object):
    """
    Aerodynamic model for a cylinder
        The reference area is the frontal area
    """
    drag_range = (0.3, 0.7)

    def __init__(self, reynolds_number: int, position: tuple):
        super().__init__(self.drag_range, reynolds_number, position)


class Cuboid(Object):
    """
    Aerodynamic model for a cuboid part
        The reference area is the frontal area
    """
    drag_range = (0.9, 0.9)

    def __init__(self, reynolds_number: int, position: tuple):
        super().__init__(self.drag_range, reynolds_number, position)


class Disk(Object):
    """
    Aerodynamic model for a disk-like part
        The reference area is the disk surface area
    """
    drag_range = (0.05, 0.05)

    def __init__(self, reynolds_number: int, position: tuple):
        super().__init__(self.drag_range, reynolds_number, position)
