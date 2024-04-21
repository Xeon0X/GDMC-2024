from gdpc import Editor, Block, geometry
import networks.Curve as curve
import networks.Segment as segment
import numpy as np

editor = Editor(buffering=True)

# # Get a block
# block = editor.getBlock((0,48,0))

# # Place a block
# editor.placeBlock((394, 132, 741), Block("stone"))

# # Build a cube
# geometry.placeCuboid(editor, (458, 92, 488), (468, 99, 471), Block("oak_planks"))

# curve = curve.Curve([(396, 132, 740), (435, 138, 730),
#                     (443, 161, 758), (417, 73, 729)])
# curve.compute_curve()

# for point in curve.computed_points:
#     print(point)
#     editor.placeBlock(point, Block("stone"))


# print(segment.parallel(((0, 0, 0), (0, 0, 10)), 10))
# print(segment.orthogonal((0, 0, 0), (1, 0, 0), 10))
# print(curve.curvature(np.array(([0, 0, 0], [0, 1, 1], [1, 0, 1]))))

for i in range(10):
    curve_points = curve.curve(
        [(317, 90, 686), (291, 95, 686), (271, 100, 705), (250, 95, 715), (234, 90, 692), (220, 146, 607), (185, 158, 598), (146, 90, 596), (142, 70, 674)], resolution=160)
    offset = curve.offset(curve_points, i)

    for coordinate in offset:
        editor.placeBlock(coordinate, Block("blue_concrete"))

    offset = curve.offset(curve_points, -i)

    for coordinate in offset:
        editor.placeBlock(coordinate, Block("red_concrete"))

    for coordinate in curve_points:
        editor.placeBlock(coordinate, Block("white_concrete"))
