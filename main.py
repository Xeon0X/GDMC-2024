from gdpc import Editor, Block, geometry, Transform
import networks.curve as curve
import numpy as np
from utils.JsonReader import JsonReader
from utils.YamlReader import YamlReader
from buildings.Building import Building

from utils.functions import *

editor = Editor(buffering=True)

# get every differents buildings shapes
f = JsonReader('buildings\shapes.json')
shapes = f.data

# get the random data for the buildings
y = YamlReader('params.yml')
random_data = y.data

#move your editor to the position you wanna build on
transform = Transform((0,-60,110),rotation = 0)
editor.transform.push(transform)

# clear the area you build on
geometry.placeCuboid(editor, (-5,0,-8), (25,100,25), Block("air"))

# create a building at the relative position 0,0 with 20 blocks length and 20 blocks width, with a normal shape and 10 floors
building = Building(random_data["buildings"], (0, 0), (20,20), shapes[0]['matrice'], 10)
# build it with your custom materials
building.build(editor, ["stone_bricks","glass_pane","glass","cobblestone_wall","stone_brick_stairs","oak_planks","white_concrete","cobblestone","stone_brick_slab","iron_bars"])






# # Get a block
block = editor.getBlock((0,48,0))

# # Build a cube
# geometry.placeCuboid(editor, (458, 92, 488), (468, 99, 471), Block("oak_planks"))

# curve = curve.Curve([(396, 132, 740), (435, 138, 730),
#                     (443, 161, 758), (417, 73, 729)])
# curve.compute_curve()