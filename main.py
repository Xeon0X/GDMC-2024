from gdpc import Editor, Block, geometry
import networks.curve as curve
import numpy as np
import json
from buildings.Foundations import Foundations

editor = Editor(buffering=True)

f = open('buildings\shapes.json')
shapes = json.load(f)
 
# F = Foundations((0,0), (20,20), shapes[0]['matrice'])
# F.polygon.fill_polygon(editor, "stone", -60)
geometry.placeCuboid(editor, (-10,-60,-10), (85,-55,85), Block("air"))
F = Foundations((0,0), (75,75), shapes[8]['matrice'])
F.polygon.fill_polygon(editor, "stone", -60)
F.polygon.fill_vertice(editor, "pink_wool", -60)
for collumn in F.collumns:
    collumn.fill(editor, "stone", -60, -55)
# # Get a block
# block = editor.getBlock((0,48,0))

# # Place a block
#editor.placeBlock((0 , 5, 0), Block("stone"))

# # Build a cube
# geometry.placeCuboid(editor, (458, 92, 488), (468, 99, 471), Block("oak_planks"))

# curve = curve.Curve([(396, 132, 740), (435, 138, 730),
#                     (443, 161, 758), (417, 73, 729)])
# curve.compute_curve()

# for point in curve.computed_points:
#     print(point)
#     editor.placeBlock(point, Block("stone"))
