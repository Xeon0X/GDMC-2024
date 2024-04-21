from gdpc import Editor, Block, geometry
import networks.curve as curve
import numpy as np

editor = Editor(buffering=True)

# # Get a block
# block = editor.getBlock((0,48,0))

# # Place a block
editor.placeBlock((-5, -58, 0), Block("stone"))

# # Build a cube
# geometry.placeCuboid(editor, (458, 92, 488), (468, 99, 471), Block("oak_planks"))

curve = curve.Curve([(396, 132, 740), (435, 138, 730),
                    (443, 161, 758), (417, 73, 729)])
curve.compute_curve()

#for point in curve.computed_points:
#    print(point)
#    editor.placeBlock(point, Block("stone"))
