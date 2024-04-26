from gdpc import Editor, Block, geometry
import networks.Curve as curve
import networks.CurveSurface as CurveSurface
import networks.Segment as segment
import numpy as np

editor = Editor(buffering=True)

y = 20

# Over the hill
# coordinates = [(-854, 87+y, -210), (-770, 99+y, -207), (-736, 85+y, -184)]

# Along the river
# coordinates = [(-456, 69, -283), (-588, 106, -374), (-720, 71, -384), (-775, 67, -289), (-822, 84, -265), (-868, 77, -188), (-927, 96, -127),
#                (-926, 65, -29), (-906, 98, 42), (-902, 137, 2), (-909, 115, -62), (-924, 76, -6), (-985, 76, 37), (-1043, 76, 28), (-1102, 66, 63)]

# Though the loop
coordinates = [(-1005, 113, -19), (-896, 113, 7),
               (-807, 76, 54), (-738, 76, -10), (-678, 76, -86)]

resolution, distance = curve.resolution_distance(coordinates, 6)

curve_points = curve.curve(coordinates, resolution)
curve_surface = CurveSurface.CurveSurface(coordinates)
curve_surface.compute_curvature()

curvature = []
for i in range(len(curve_surface.curvature)):
    curvature.append((0, 1, 0))

curve_surface.compute_surface(10, curvature)

# for coordinate in curve_surface.offset_points:
#     editor.placeBlock(coordinate, Block("white_concrete"))

for coordinate in curve_surface.surface:
    editor.placeBlock(coordinate, Block("black_concrete"))

for coordinate in curve_surface.curve:
    editor.placeBlock(coordinate, Block("red_concrete"))


# for line_range in range(len(curve_surface.offset_points[0])):
#     for coordinate in curve_surface.offset_points[line_range]:
#         editor.placeBlock(coordinate, Block("red_concrete"))

# offset = curve.offset(curve_points, i)

# for coordinate in offset:
#     editor.placeBlock(coordinate, Block("blue_concrete"))

# offset = curve.offset(curve_points, -i)

# for coordinate in offset:
#     editor.placeBlock(coordinate, Block("red_concrete"))

# for coordinate in curve_points:
#     editor.placeBlock(coordinate, Block("white_concrete"))

###
