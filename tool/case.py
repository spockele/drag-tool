"""
Module with the Case class for the simulation case.
"""

import numpy as np
import matplotlib.pyplot as plt


from .objects import Part, Sphere, Cylinder, Cuboid, IceCreamCone, Disk


class Case:
    """

    """
    def __init__(self, case: str):
        self.parts = list()
        self.density = float()
        self.velocity = float()
        self.reynolds_number = int()
        self.flow_direction = int()

        self.slowdown_xp = (0, 3, 10, 100)
        self.slowdown_fp = (0, .8, .9, 1)

        self.name = case
        self.load_case()

        self.result = tuple()

    def __repr__(self):
        return f"Drag Analysis Case {self.name}: [rho={self.density}, v={self.velocity} " \
               f"Re={self.reynolds_number}, flow direction={self.flow_direction}] " \
               f"with parts: {self.parts}"

    def write_to_file(self, filename: str = None):
        lines = [f"Case, {self.name},\n",
                 f"Drag, {self.result[0]} N,\n",
                 f"Drag Area, {self.result[1]} m2,\n\n"]

        for part in self.parts:
            lines.append(f"{part.__name__}, D = {round(part.drag, 3)}N ,"
                         f" V/V_flow = {round(part.wake_factor, 3)},\n")

        path = f"data/result_{self.name}.csv" if filename is None else f"data/{filename}.csv"
        f = open(path, "w")
        f.writelines(lines)
        f.close()

    def plot_slowdown(self):
        plt.plot(self.slowdown_xp, self.slowdown_fp, marker='o', markersize=5, linestyle='dashed')
        plt.xlabel("$x/L_{char}$")
        plt.ylabel("$V/V_{flow}$")
        plt.ylim(0)
        plt.xlim(0)
        plt.grid()
        plt.show()

    def load_case(self):
        f = open(f"data/{self.name}.csv")
        lines = [line.strip(",\n").split(", ") for line in f.readlines()]
        f.close()

        self.density, self.velocity = (float(value) for value in lines[2][0:2])
        self.reynolds_number, self.flow_direction = (int(value) for value in lines[2][2:4])

        line = lines[5]
        count = 5
        while line[0] != 'Cylinders':
            if "#" not in line[0]:
                name = str(line[0])
                position = tuple(float(value) for value in line[1:4])
                radius = float(line[4])
                self.parts.append(Sphere(self.density, self.velocity, position, radius, name=name))

            count += 1
            line = lines[count]

        count += 2
        line = lines[count]
        while line[0] != 'Cuboids':
            if "#" not in line[0]:
                name = str(line[0])
                position = tuple(float(value) for value in line[1:4])
                radius, length = tuple(float(value) for value in line[4:6])
                orientation = int(line[6])
                self.parts.append(
                    Cylinder(self.density, self.velocity, position, radius, length, orientation,
                             name=name))

            count += 1
            line = lines[count]

        count += 2
        line = lines[count]
        while line[0] != 'IceCream Cones':
            if "#" not in line[0]:
                name = str(line[0])
                position = tuple(float(value) for value in line[1:4])
                dimensions = tuple(float(value) for value in line[4:7])
                self.parts.append(Cuboid(self.density, self.velocity, position, dimensions,
                                         name=name))

            count += 1
            line = lines[count]

        count += 2
        line = lines[count]
        while line[0] != 'Disks':
            if "#" not in line[0]:
                name = str(line[0])
                position = tuple(float(value) for value in line[1:4])
                radius, length_cylinder, length_cone = tuple(float(value) for value in line[4:7])
                orientation = int(line[7])
                self.parts.append(
                    IceCreamCone(self.density, self.velocity, position, radius, length_cylinder,
                                 length_cone, orientation, name=name))

            count += 1
            line = lines[count]

        count += 2
        line = lines[count]
        while line[0] != '':
            if "#" not in line[0]:
                name = str(line[0])
                position = tuple(float(value) for value in line[1:4])
                radius = float(line[4])
                orientation = tuple(int(value) for value in line[5:7])

                self.parts.append(Disk(self.density, self.velocity, position, radius,
                                       orientation, name=name))

            count += 1
            line = lines[count]

    def run_case(self):
        perpendicular_plane = [0, 2, 1]
        perpendicular_plane.remove(self.flow_direction)

        part: Part
        for part in self.parts:
            part.set_frontal_surface(*perpendicular_plane)
            part.set_characteristic_length(self.flow_direction)
            part.set_smallest_coordinate(self.flow_direction)

        self.parts.sort()

        for index_1, part in enumerate(self.parts):
            surface = part.get_frontal_surface()

            other_part: Part
            for index_2, other_part in enumerate(self.parts[index_1+1:]):
                slowdown = part.wake_slowdown

                other_surface = other_part.get_frontal_surface()
                area = surface.intersection(other_surface)

                if area > other_part.largest_intersection:
                    # print(part.__name__, other_part.__name__, area / other_surface.area)
                    # print("\t", surface, other_surface)
                    distance = (other_part.position[self.flow_direction] -
                                part.position[self.flow_direction])
                    x = distance / part.get_characteristic_length()

                    slowdown *= round(np.interp(x, self.slowdown_xp, self.slowdown_fp), 4)
                    # print("\t", distance, x, slowdown)

                    other_part.set_slowdown(slowdown, area)
                    other_part.set_largest_intersection(area)

        total_drag = 0.
        for part in self.parts:
            part.apply_slowdown(self.flow_direction)
            total_drag += part.drag

        drag_area = total_drag / (0.5 * self.density * self.velocity ** 2)

        self.result = round(total_drag, 3), round(drag_area, 3)

        return self.velocity, self.result
