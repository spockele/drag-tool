# Drag tool for Personal Air Transportation System
[Original github repository](https://github.com/spockele/drag-tool)\
Current version: 1.2\
Branch with this version: version-1.2

## Template case.csv file
```
Case Definition,
Density, Velocity, Reynolds number, flow_direction,
rho, V, Re, integer
Spheres,
name, centre x, centre y, centre z, radius,
#
name, x, y, z, r
#
Cylinders,
name, centre x, centre y, centre z, radius, length, orientation,
#
name, x, y, z, r, l, integer
#
Cuboids,
name, centre x, centre y, centre z, dimension x, dimension y, dimension z,
#
name, x, y, z, dimension in x, dimension in y, dimension in z
#
IceCream Cones,
name, centre x, centre y, centre z, radius, length_cylinder, length_cone, orientation,
#
name, x, y, z, r, l_cylinder, l_cone, integer
#
Disks,
name, centre x, centre y, centre z, radius, orientation1, orientation2,
#
name, x, y, z, r, integer, integer
#
,

```
