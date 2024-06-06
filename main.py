import networks.roads.lines.Line as Line
import networks.roads.lanes.Lane as Lane
from gdpc import Editor, Block, geometry
import networks.geometry.curve_tools as curve_tools
import networks.geometry.Strip as Strip
import networks.geometry.segment_tools as segment_tools
import numpy as np
import json
from buildings.Building import Building
import random

from networks.roads import Road as Road
from networks.roads.intersections import Intersection as Intersection

from networks.geometry.point_tools import curved_corner_by_curvature, curved_corner_by_distance

editor = Editor(buffering=True)

# f = open('buildings\shapes.json')
# shapes = json.load(f)

# # F = Foundations((0,0), (20,20), shapes[0]['matrice'])
# # F.polygon.fill_polygon(editor, "stone", -60)
# geometry.placeCuboid(editor, (-10, -60, -10), (85, -55, 85), Block("air"))
# B = Building((0, 0), (75, 75), shapes[7]['matrice'])
# B.foundations.polygon.fill_vertice(editor, "pink_wool", -60)
# for collumn in B.foundations.collumns:
#     collumn.fill(editor, "white_concrete", -60, -55)
# B.foundations.polygon.fill_polygon(editor, "white_concrete", -60)

y = 25
block_list = ["blue_concrete", "red_concrete", "green_concrete",
              "yellow_concrete", "purple_concrete", "pink_concrete"]

# Over the hill
# coordinates = [(-854, 87+y, -210), (-770, 99+y, -207), (-736, 85+y, -184)]

# # Along the river
# # coordinates = [(-456, 69, -283), (-588, 106, -374), (-720, 71, -384), (-775, 67, -289), (-822, 84, -265), (-868, 77, -188), (-927, 96, -127),
# #                (-926, 65, -29), (-906, 98, 42), (-902, 137, 2), (-909, 115, -62), (-924, 76, -6), (-985, 76, 37), (-1043, 76, 28), (-1102, 66, 63)]

# # Though the loop
# # coordinates = [(-1005, 113+y, -19), (-896, 113+y, 7),
# #                (-807, 76+y, 54), (-738, 76+y, -10), (-678, 76+y, -86)]

# # Second zone
# coordinates = [(-805, 78, 128), (-881, 91, 104), (-950, 119, 69), (-1005, 114, 58), (-1052, 86, 30),
#                (-1075, 83, 40), (-1104, 77, 63), (-1161, 69, 157), (-1144, 62, 226), (-1189, 76, 265), (-1210, 79, 329)]

# resolution, distance = curve.resolution_distance(coordinates, 6)

# curve_points = curve.curve(coordinates, resolution)
# curve_surface = CurveSurface.CurveSurface(coordinates)
# curve_surface.compute_curvature()

# curvature = []
# for i in range(len(curve_surface.curvature)):
#     curvature.append((0, 1, 0))


# # Perpendicular
# curve_surface.compute_surface_perpendicular(10, curvature)
# for i in range(len(curve_surface.surface)):
#     for j in range(len(curve_surface.surface[i])):
#         # block = random.choice(block_list)
#         for k in range(len(curve_surface.surface[i][j])):
#             if k-16 < len(block_list) and k-16 >= 0:
#                 editor.placeBlock(
#                     curve_surface.surface[i][j][k], Block(block_list[k-16]))
#             else:
#                 editor.placeBlock(
#                     curve_surface.surface[i][j][k], Block("stone"))

# offset = curve.offset(curve_surface.curve, -9, curvature)
# for i in range(len(offset)-1):
#     line = segment.discrete_segment(offset[i], offset[i+1])
#     for coordinate in line:
#         editor.placeBlock(coordinate, Block("white_concrete"))

# offset = curve.offset(curve_surface.curve, 9, curvature)
# for i in range(len(offset)-1):
#     line = segment.discrete_segment(offset[i], offset[i+1])
#     for coordinate in line:
#         editor.placeBlock(coordinate, Block("white_concrete"))

# # for coordinate in curve_surface.surface:
# #     editor.placeBlock(coordinate, Block("black_concrete"))

# # for coordinate in curve_surface.curve:
# #     editor.placeBlock(coordinate, Block("red_concrete"))

# # # Parallel
# # curve_surface.compute_surface_parallel(0, 10, 8, curvature)

# # for current_range in range(len(curve_surface.left_side)):
# #     for coordinate in curve_surface.left_side[current_range]:
# #         editor.placeBlock(coordinate, Block("yellow_concrete"))

# ---

# coordinates = [(0, 0, 0), (0, 0, 10), (0, 0, 20)]

# with open('networks/roads/lines/lines.json') as f:
#     lines_type = json.load(f)
#     l = Line.Line(coordinates, lines_type.get('solid_white'))
#     print(l.get_surface())

# with open('networks/roads/lanes/lanes.json') as f:
#     lanes_type = json.load(f)
#     l = Lane.Lane(coordinates, lanes_type.get('classic_lane'), 5)
#     print(l.get_surface())


# circle = curved_corner(
#     ((-1365, 520), (-1326, 523)), ((-1344, 496), (-1336, 535)), 10, angle_adaptation=False, output_only_points=False)

# for coordinate in circle[0]:
#     editor.placeBlock(
#         (round(coordinate[0]), 125, round(coordinate[1])), Block("green_concrete"))

# ---

# r1 = Road.Road((-1341, 100, 439), "None")
# r2 = Road.Road((-1378, 100, 415), "None")

# i = Intersection.Intersection(
#     (-1352, 100, 405), [(-1345, 100, 426), (-1369, 100, 412)], [r1, r2])


# ---

# r1 = Road.Road((-1337, 71, 472), "None")
# r2 = Road.Road((-1269, 80, 574), "None")
# r3 = Road.Road((-1392, 79, 527), "None")

# i = Intersection.Intersection(
#     (-1327, 71, 533), [(-1335, 71, 494), (-1298, 75, 553), (-1366, 78, 530)], [r1, r2, r3])

# ---

# y = 150

# r1 = Road.Road((-1337, y, 472), "None")
# r2 = Road.Road((-1269, y, 574), "None")
# r3 = Road.Road((-1392, y, 527), "None")

# i = Intersection.Intersection(
#     (-1327, y, 533), [(-1335, y, 494), (-1298, y, 553), (-1366, y, 530)], [r1, r2, r3])


# ---

# y = 100
# x = -200

# r1 = Road.Road((-1380+x, 75, 406), "None")
# r2 = Road.Road((-1365+x, 75, 468), "None")
# r3 = Road.Road((-1411+x, 75, 501), "None")
# r4 = Road.Road((-1451+x, 75, 449), "None")
# r5 = Road.Road((-1432+x, 75, 423), "None")

# i = Intersection.Intersection(
#     (-1411+x, 75, 461), [(-1392+x, 75, 427), (-1385+x, 75, 465), (-1411+x, 75, 487), (-1435+x, 75, 454), (-1426+x, 75, 435)], [r1, r2, r3, r4, r5])

# i.compute_curved_corner()

# for j in range(len(i.orthogonal_delimitations)):

#     coordinates = segment_tools.discrete_segment(
#         i.orthogonal_delimitations[j][0][0], i.orthogonal_delimitations[j][0][1])
#     for coordinate in coordinates:
#         editor.placeBlock(coordinate, Block("purple_concrete"))

#     coordinates = segment_tools.discrete_segment(
#         i.orthogonal_delimitations[j][1][0], i.orthogonal_delimitations[j][1][1])
#     for coordinate in coordinates:
#         editor.placeBlock(coordinate, Block("pink_concrete"))

#     coordinates = segment_tools.discrete_segment(
#         i.parallel_delimitations[j][0][0], i.parallel_delimitations[j][0][1])
#     for coordinate in coordinates:
#         editor.placeBlock(coordinate, Block("orange_concrete"))

#     coordinates = segment_tools.discrete_segment(
#         i.parallel_delimitations[j][1][0], i.parallel_delimitations[j][1][1])
#     for coordinate in coordinates:
#         editor.placeBlock(coordinate, Block("yellow_concrete"))

# for coordinate in i.intersections:
#     if coordinate != None:
#         editor.placeBlock(coordinate, Block("black_concrete"))

# for k in range(len(i.intersections_curved)):
#     for coordinate in i.intersections_curved[k][0]:
#         if coordinate != None:
#             if k >= 0:
#                 editor.placeBlock(
#                     (coordinate[0], 75, coordinate[1]), Block("gray_concrete"))

#     editor.placeBlock(
#         (i.intersections_curved[k][1][0], 76, i.intersections_curved[k][1][1]), Block("black_concrete"))

#     coordinates = segment_tools.discrete_segment(
#         i.intersections_curved[k][-1][0], i.intersections_curved[k][-1][1])
#     for coordinate in coordinates:
#         editor.placeBlock(coordinate, Block("lime_concrete"))

#     coordinates = segment_tools.discrete_segment(
#         i.intersections_curved[k][-2][0], i.intersections_curved[k][-2][1])
#     for coordinate in coordinates:
#         editor.placeBlock(coordinate, Block("green_concrete"))

# ---

# intersection = (-1510, 94, 455)
# xyz0 = (-1545, 90, 537)
# xyz1 = (-1535, 162, 459)
# circle = curved_corner_by_distance(
#     intersection, xyz0, xyz1, 25, 0)

# line0 = segment_tools.discrete_segment(intersection, xyz0)
# line1 = segment_tools.discrete_segment(intersection, xyz1, pixel_perfect=False)

# editor.placeBlock(
#     circle[1], Block("black_concrete"))

# editor.placeBlock(
#     circle[3], Block("gray_concrete"))
# print(circle[3], "center")
# print(circle[4], "center")

# for coordinate in circle[0]:
#     editor.placeBlock(
#         coordinate, Block("white_concrete"))
#     print(coordinate)

# for coordinate in line0:
#     editor.placeBlock(
#         coordinate, Block("blue_concrete"))

# for coordinate in line1:
#     editor.placeBlock(
#         coordinate, Block("red_concrete"))

# ---

r = Road.Road(((-1829, 141, 553), (-1830, 110, 621), (-1711, 69, 625), (-1662,
              65, 627), (-1667, 65, 761), (-1683, 70, 800), (-1721, 70, 834)), "None")

r.place_roads()
