import networks.geometry.curve_tools as curve_tools
import networks.geometry.Strip as Strip

from gdpc import Editor, Block, geometry


class Road:
    def __init__(self, coordinates, road_configuration):
        self.coordinates = coordinates
        self.road_configuration = road_configuration 	# 'road', 'highway'
        self.width = 10  # TODO

    def place_roads(self):
        editor = Editor(buffering=True)

        self.resolution, self.distance = curve_tools.resolution_distance(
            self.coordinates, 6)

        self.curve_points = curve_tools.curve(
            self.coordinates, self.resolution)
        self.curve_surface = Strip.Strip(self.coordinates)
        self.curve_surface.compute_curvature()

        self.curvature = []
        for i in range(len(self.curve_surface.curvature)):
            self.curvature.append((0, 1, 0))

        # Perpendicular
        self.curve_surface.compute_surface_perpendicular(10, self.curvature)
        for i in range(len(self.curve_surface.surface)):
            for j in range(len(self.curve_surface.surface[i])):
                # block = random.choice(block_list)
                for k in range(len(self.curve_surface.surface[i][j])):
                    editor.placeBlock(
                        self.curve_surface.surface[i][j][k], Block("blackstone"))

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
