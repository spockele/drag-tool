# Drag tool for Personal Air Transportation System
[Original github repository](https://github.com/spockele/drag-tool)\
Current version: 1.3.1\
Branch with this version: main (commit [main fb059c2](https://github.com/spockele/drag-tool/commit/fb059c2842d0f4ef4f0c5fc00c5116d6196b2906))

## Template case.csv file
The case file should use the following template. Put your values for your case in the appropriate place. Case files should be named: `[case_name].csv`.
```
Case Definition,
Density, Velocity, Reynolds number, flow_direction,
rho, V, Re, integer
Spheres,
name, centre x, centre y, centre z, radius,
#
[your values go here]
#
Cylinders,
name, centre x, centre y, centre z, radius, length, orientation,
#
[your values go here]
#
Cuboids,
name, centre x, centre y, centre z, dimension x, dimension y, dimension z,
#
[your values go here]
#
IceCream Cones,
name, centre x, centre y, centre z, radius, length_cylinder, length_cone, orientation,
#
[your values go here]
#
Disks,
name, centre x, centre y, centre z, radius, orientation1, orientation2,
#
[your values go here]
#
,

```

## Results
The program will output the results of a calculation in the `data/` folder as `result_[case_name].csv`. These csv files are recommended to be opened with a spreadsheet reader, as they are formatted for that purpose.
