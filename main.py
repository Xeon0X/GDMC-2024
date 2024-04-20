from gdpc import Editor, Block, geometry
import networks.curve as curve
import numpy as np

# editor = Editor(buffering=True)

# # Get a block
# block = editor.getBlock((0,48,0))

# # Place a block
# editor.placeBlock((394, 132, 741), Block("stone"))

# # Build a cube
# geometry.placeCuboid(editor, (458, 92, 488), (468, 99, 471), Block("oak_planks"))

curve = curve.Curve([(0, 0, 0), (1, 1, 1), (5, 5, 5), (1, 1, 1), (1, 1, 1)])
curve.compute_curve()
