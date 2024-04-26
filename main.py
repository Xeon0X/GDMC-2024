from gdpc import Editor, Block, geometry
import networks.Curve as curve
import networks.CurveSurface as CurveSurface
import networks.Segment as segment
import numpy as np
import random

editor = Editor(buffering=True)

y = 25
block_list = ["blue_concrete", "red_concrete", "green_concrete",
              "yellow_concrete", "purple_concrete", "pink_concrete"]

# Over the hill
# coordinates = [(-854, 87+y, -210), (-770, 99+y, -207), (-736, 85+y, -184)]

# Along the river
# coordinates = [(-456, 69, -283), (-588, 106, -374), (-720, 71, -384), (-775, 67, -289), (-822, 84, -265), (-868, 77, -188), (-927, 96, -127),
#                (-926, 65, -29), (-906, 98, 42), (-902, 137, 2), (-909, 115, -62), (-924, 76, -6), (-985, 76, 37), (-1043, 76, 28), (-1102, 66, 63)]

# Though the loop
# coordinates = [(-1005, 113+y, -19), (-896, 113+y, 7),
#                (-807, 76+y, 54), (-738, 76+y, -10), (-678, 76+y, -86)]

# Second zone
coordinates = [(-805, 78, 128), (-881, 91, 104), (-950, 119, 69), (-1005, 114, 58), (-1052, 86, 30),
               (-1075, 83, 40), (-1104, 77, 63), (-1161, 69, 157), (-1144, 62, 226), (-1189, 76, 265), (-1210, 79, 329)]

resolution, distance = curve.resolution_distance(coordinates, 6)

curve_points = curve.curve(coordinates, resolution)
curve_surface = CurveSurface.CurveSurface(coordinates)
curve_surface.compute_curvature()

curvature = []
for i in range(len(curve_surface.curvature)):
    curvature.append((0, 1, 0))


# Perpendicular
curve_surface.compute_surface_perpendicular(10, curvature)
for i in range(len(curve_surface.surface)):
    for j in range(len(curve_surface.surface[i])):
        # block = random.choice(block_list)
        for k in range(len(curve_surface.surface[i][j])):
            if k-16 < len(block_list) and k-16 >= 0:
                editor.placeBlock(
                    curve_surface.surface[i][j][k], Block(block_list[k-16]))
            else:
                editor.placeBlock(
                    curve_surface.surface[i][j][k], Block("stone"))

offset = curve.offset(curve_surface.curve, -9, curvature)
for i in range(len(offset)-1):
    line = segment.discrete_segment(offset[i], offset[i+1])
    for coordinate in line:
        editor.placeBlock(coordinate, Block("white_concrete"))

offset = curve.offset(curve_surface.curve, 9, curvature)
for i in range(len(offset)-1):
    line = segment.discrete_segment(offset[i], offset[i+1])
    for coordinate in line:
        editor.placeBlock(coordinate, Block("white_concrete"))

# for coordinate in curve_surface.surface:
#     editor.placeBlock(coordinate, Block("black_concrete"))

# for coordinate in curve_surface.curve:
#     editor.placeBlock(coordinate, Block("red_concrete"))

# # Parallel
# curve_surface.compute_surface_parallel(0, 10, 8, curvature)

# for current_range in range(len(curve_surface.left_side)):
#     for coordinate in curve_surface.left_side[current_range]:
#         editor.placeBlock(coordinate, Block("yellow_concrete"))
