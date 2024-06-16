import networks.geometry.curve_tools as curve_tools
import networks.geometry.Strip as Strip
import networks.roads.lanes.Lane as Lane
import networks.roads.lines.Line as Line
import json
import random

from gdpc import Editor, Block, geometry


class Road:
    def __init__(self, coordinates, road_configuration):
        self.coordinates = coordinates
        self.road_configuration = road_configuration 	# 'road', 'highway'
        self.width = 10  # TODO

    def place_roads(self):
        editor = Editor(buffering=True)

        self.resolution, self.distance = curve_tools.resolution_distance(
            self.coordinates, 12)

        self.curve_points = curve_tools.curve(
            self.coordinates, self.resolution)
        self.curve_surface = Strip.Strip(self.coordinates)
        self.curve_surface.compute_curvature()

        self.curvature = []
        for i in range(len(self.curve_surface.curvature)):
            self.curvature.append((0, 1, 0))

        with open('networks/roads/lanes/lanes.json') as lanes_materials:
            lane_type = json.load(lanes_materials).get('classic_lane')

        # for coordinate, block in surface:
        #     editor.placeBlock(coordinate, Block(block))

        with open('networks/roads/lines/lines.json') as lines_materials:
            line_type = json.load(lines_materials).get('solid_white')
        with open('networks/roads/lines/lines.json') as lines_materials:
            middle_line_type = json.load(lines_materials).get('broken_white')

        print(line_type, lane_type)

        # for coordinate, block in surface:
        #     editor.placeBlock(coordinate, Block(block))

        lines_coordinates = []
        middle_lines_coordinates = []

        # Perpendicular
        self.curve_surface.compute_surface_perpendicular(10, self.curvature)
        for i in range(len(self.curve_surface.surface)):
            for j in range(len(self.curve_surface.surface[i])):
                for k in range(len(self.curve_surface.surface[i][j])):
                    for l in range(len(self.curve_surface.surface[i][j][k])):
                        editor.placeBlock(
                            self.curve_surface.surface[i][j][k][l], Block(random.choices(
                                list(lane_type.keys()),
                                weights=lane_type.values(),
                                k=1,)[0]))
                        editor.placeBlock(
                            (self.curve_surface.surface[i][j][k][l][0], self.curve_surface.surface[i][j][k][l][1]-1, self.curve_surface.surface[i][j][k][l][2]), Block(random.choices(
                                list(lane_type.keys()),
                                weights=lane_type.values(),
                                k=1,)[0]))
                    if k == 0 or k == len(self.curve_surface.surface[i][j])-1:
                        lines_coordinates.extend(
                            self.curve_surface.surface[i][j][k])
                    if k == round((len(self.curve_surface.surface[i][j])-1)/2):
                        middle_lines_coordinates.extend(
                            self.curve_surface.surface[i][j][k])

        line = Line.Line(lines_coordinates, line_type)
        line.get_blocks()
        middle_line = Line.Line(middle_lines_coordinates, middle_line_type)
        middle_line.get_blocks()
        for i in range(len(line.coordinates_with_blocks)):
            editor.placeBlock(
                line.coordinates_with_blocks[i][0], Block(line.coordinates_with_blocks[i][1]))
        for i in range(len(middle_line.coordinates_with_blocks)):
            editor.placeBlock(
                middle_line.coordinates_with_blocks[i][0], Block(middle_line.coordinates_with_blocks[i][1]))

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
