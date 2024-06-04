from gdpc import Editor, Block, geometry, Transform
import networks.curve as curve
import numpy as np
from utils.JsonReader import JsonReader
from utils.YamlReader import YamlReader
from buildings.Building import Building

from buildings.geometry.Vertice import Vertice
from buildings.geometry.Point import Point
from utils.Enums import DIRECTION,COLLUMN_STYLE,BORDER_RADIUS
from buildings.Facade import Facade

from utils.functions import *

editor = Editor(buffering=True)

f = JsonReader('buildings\shapes.json')
shapes = f.data

y = YamlReader('params.yml')
random_data = y.data


transform = Transform((0,-60,-5),rotation = 0)
editor.transform.push(transform)

geometry.placeCuboid(editor, (0,0,-3), (100,15,1), Block("air"))


x = 0
facade = []
for i in range(3,13):
    facade.append(Facade(random_data["buildings"]["facade"],[Vertice(Point(x,0,0), Point(x+i,i,0), DIRECTION.NORTH)],COLLUMN_STYLE.NONE))
    x += i+2

for f in facade:
    f.build(editor, ["stone_bricks","glass_pane","glass","cobblestone_wall","stone_brick_stairs"])

 
# F = Foundations((0,0), (20,20), shapes[0]['matrice'])
# F.polygon.fill_polygon(editor, "stone", -60)

# geometry.placeCuboid(editor, (-10,-60,-10), (85,-55,85), Block("air"))
# B = Building((0,0), (75,75), shapes[7]['matrice'])
# B.foundations.polygon.fill_vertice(editor, "pink_wool", -60)
# for collumn in B.foundations.collumns:
#     collumn.fill(editor, "white_concrete", -60, -55)
# B.foundations.polygon.fill_polygon(editor, "white_concrete", -60)



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
