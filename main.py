import random

import gdpc.exceptions

from world_maker.world_maker import *
from House import *


def main():

    rectangle_house_mountain, rectangle_building, skeleton_highway, skeleton_mountain = world_maker()

    editor = Editor(buffering=True)
    buildArea = editor.getBuildArea()

    blocks = {
        "wall": "blackstone",
        "roof": "blackstone",
        "roof_slab": "blackstone_slab",
        "door": "oak_door",
        "window": "glass_pane",
        "entrance": "oak_door",
        "stairs": "quartz_stairs",
        "stairs_slab": "quartz_slab",
        "celling": "quartz_block",
        "floor": "quartz_block",
        "celling_slab": "quartz_slab",
        "garden_outline": "oak_leaves",
        "garden_floor": "grass_block"
    }

    entranceDirection = ["N", "S", "E", "W"]

    for houses in rectangle_house_mountain:
        start = (houses[0][0]+buildArea.begin[0], houses[0]
                 [1], houses[0][2]+buildArea.begin[2])
        end = (houses[1][0]+buildArea.begin[0], houses[1]
               [1], houses[1][2]+buildArea.begin[2])
        house = House(editor, start, end,
                      entranceDirection[random.randint(0, 3)], blocks)
        house.build()


if __name__ == '__main__':
    main()

"""
from gdpc import Editor, Block, geometry, Transform
import networks.curve as curve
import numpy as np
from utils.JsonReader import JsonReader
from utils.YamlReader import YamlReader
from buildings.Building import Building

from utils.functions import *
from utils.Enums import DIRECTION

editor = Editor(buffering=True)

# get every differents buildings shapes
f = JsonReader('buildings\shapes.json')
shapes = f.data
baseShape = shapes[0]['matrice']

# get the random data for the buildings
y = YamlReader('params.yml')
random_data = y.data

#move your editor to the position you wanna build on
transform = Transform((75,-60,110),rotation = 0)
editor.transform.push(transform)

# clear the area you build on
geometry.placeCuboid(editor, (-5,0,-8), (25,100,25), Block("air"))

# create a building at the relative position 0,0 with 20 blocks length and 20 blocks width, with a normal shape and 10 floors
building = Building(random_data["buildings"], [(0,0,0), (20,30,20)], baseShape, DIRECTION.EAST)
# build it with your custom materials
building.build(editor, ["stone_bricks","glass_pane","glass","cobblestone_wall","stone_brick_stairs","oak_planks","white_concrete","cobblestone","stone_brick_slab","iron_bars"])
"""
