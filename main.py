from gdpc import Editor, Block, geometry
import networks.Curve as curve
import networks.CurveSurface as CurveSurface
import networks.Segment as segment
import numpy as np

editor = Editor(buffering=True)

y = 20
coordinates = [(-854, 87+y, -210), (-770, 99+y, -207), (-736, 85+y, -184)]
resolution, distance = curve.resolution_distance(coordinates, 10)

curve_points = curve.curve(coordinates, resolution)
curve_surface = CurveSurface.CurveSurface(curve_points)
curve_surface.compute_curvature()
curve_surface.compute_surface(50, curve_surface.curvature, 1)

for line_range in range(len(curve_surface.offset_points[0])):
    for coordinate in curve_surface.offset_points[line_range]:
        editor.placeBlock(coordinate, Block("white_concrete"))

# offset = curve.offset(curve_points, i)

# for coordinate in offset:
#     editor.placeBlock(coordinate, Block("blue_concrete"))

# offset = curve.offset(curve_points, -i)

# for coordinate in offset:
#     editor.placeBlock(coordinate, Block("red_concrete"))

# for coordinate in curve_points:
#     editor.placeBlock(coordinate, Block("white_concrete"))

###
