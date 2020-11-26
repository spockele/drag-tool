"""
Module with the Case class for the simulation case.
"""


from .objects import Sphere, Cylinder, Cuboid


class Case:
    """

    """
    def __init__(self, case: str):
        self.parts = list()
        self.dynamic_pressure = int()
        self.reynolds_number = int()

        self.load_case(case)

    def load_case(self, case: str):
        f = open(f"data/{case}.csv")
        lines = [line.strip(",\n").split(", ") for line in f.readlines()]
        f.close()

        self.dynamic_pressure, self.reynolds_number = (int(value) for value in lines[2])

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
        while line[0] != '':
            position = tuple(float(value) for value in line[0:3])
            dimensions = tuple(float(value) for value in line[3:6])
            self.parts.append(Cuboid(self.reynolds_number, self.dynamic_pressure,
                                     position, dimensions))

            count += 1
            line = lines[count]

        print(self.parts)
