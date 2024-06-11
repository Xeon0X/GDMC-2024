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

transform = Transform((0,-60,80),rotation = 0)
editor.transform.push(transform)

geometry.placeCuboid(editor, (-5,0,-8), (170,25,25), Block("air"))


padd = 0
for i in range(4,13):
    building = Building(random_data["buildings"], (padd, 0), (i,i), shapes[0]['matrice'], 3)
    building.build(editor, ["stone_bricks","glass_pane","glass","cobblestone_wall","stone_brick_stairs","oak_planks","white_concrete","cobblestone","stone_brick_slab"])
    padd += i + 10



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
