from gdpc import Editor, Block, geometry, Transform
import networks.curve as curve
import numpy as np
from utils.JsonReader import JsonReader
from utils.YamlReader import YamlReader
from buildings.Building import Building

from utils.functions import *

editor = Editor(buffering=True)

f = JsonReader('buildings\shapes.json')
shapes = f.data

y = YamlReader('params.yml')
random_data = y.data

# transform = Transform((0,-60,-20),rotation = 0)
# editor.transform.push(transform)
# for i in range(4):
#     with editor.pushTransform(Transform(rotation = i)):
#         geometry.placeCuboid(editor, (0,0,0), (0,3,5), Block("stone"))

transform = Transform((0,-60,110),rotation = 0)
editor.transform.push(transform)

geometry.placeCuboid(editor, (-5,0,-8), (60,10,70), Block("air"))

buildings = []
buildings.append(Building(random_data["buildings"], (0, 0), (20,20), shapes[0]['matrice'], 1))
buildings.append(Building(random_data["buildings"], (25, 0), (30,30), shapes[5]['matrice'], 1))
buildings.append(Building(random_data["buildings"], (0, 35), (30,30), shapes[6]['matrice'], 1))
buildings.append(Building(random_data["buildings"], (35, 35), (20,20), shapes[7]['matrice'], 1))

for building in buildings :
    building.build(editor, ["stone_bricks","glass_pane","glass","cobblestone_wall","stone_brick_stairs","oak_planks","white_concrete","cobblestone","stone_brick_slab"])


# # Get a block
# block = editor.getBlock((0,48,0))

# # Place a block
# editor.placeBlock((0 , 5, 0), Block("stone"))

# # Build a cube
# geometry.placeCuboid(editor, (458, 92, 488), (468, 99, 471), Block("oak_planks"))

# curve = curve.Curve([(396, 132, 740), (435, 138, 730),
#                     (443, 161, 758), (417, 73, 729)])
# curve.compute_curve()

# for point in curve.computed_points:
#     print(point)
#     editor.placeBlock(point, Block("stone"))
