"""
Module with the Case class for the simulation case.
"""


from .objects import Sphere, Cylinder, Cuboid, IceCreamCone


class Case:
    """

    """
    def __init__(self, case: str):
        self.parts = list()
        self.dynamic_pressure = int()
        self.reynolds_number = int()
        self.flow_direction = int()

        self.load_case(case)

    def __repr__(self):
        return f"Drag Analysis Case: [q={self.dynamic_pressure}, Re={self.reynolds_number}, " \
               f"flow direction={self.flow_direction}] with parts: {self.parts}"

    def load_case(self, case: str):
        f = open(f"data/{case}.csv")
        lines = [line.strip(",\n").split(", ") for line in f.readlines()]
        f.close()

        self.dynamic_pressure, self.reynolds_number, self.flow_direction = \
            (int(value) for value in lines[2])

        line = lines[5]
        count = 5
        while line[0] != 'Cylinders':
            position = tuple(float(value) for value in line[0:3])
            radius = float(line[3])
            self.parts.append(Sphere(self.reynolds_number, self.dynamic_pressure,
                                     position, radius))

            count += 1
            line = lines[count]

        count += 2
        line = lines[count]
        while line[0] != 'Cuboids':
            position = tuple(float(value) for value in line[0:3])
            radius, length = tuple(float(value) for value in line[3:5])
            orientation = int(line[5])
            self.parts.append(Cylinder(self.reynolds_number, self.dynamic_pressure,
                                       position, radius, length, orientation))

            count += 1
            line = lines[count]

        count += 2
        line = lines[count]
        while line[0] != 'IceCream Cones':
            position = tuple(float(value) for value in line[0:3])
            dimensions = tuple(float(value) for value in line[3:6])
            self.parts.append(Cuboid(self.reynolds_number, self.dynamic_pressure,
                                     position, dimensions))

            count += 1
            line = lines[count]

        count += 2
        line = lines[count]
        while line[0] != '':
            position = tuple(float(value) for value in line[0:3])
            radius, length_cylinder, length_cone = tuple(float(value) for value in line[3:6])
            orientation = int(line[6])
            self.parts.append(IceCreamCone(self.reynolds_number, self.dynamic_pressure,
                                           position, radius, length_cylinder, length_cone,
                                           orientation))

            count += 1
            line = lines[count]

    def run_case(self):
        perpendicular_plane = [0, 1, 2]
        perpendicular_plane.remove(self.flow_direction)

        for part in self.parts:
            part.set_frontal_surface(*perpendicular_plane)

        self.parts.sort()
