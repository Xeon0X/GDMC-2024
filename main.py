import random

import gdpc.exceptions

from world_maker.world_maker import *
from world_maker.Skeleton import Skeleton, transpose_form_heightmap, simplify_coordinates
from networks.geometry.Point3D import Point3D
from networks.roads_2.Road import Road
from networks.legacy_roads import roads
from world_maker.District import Road as Road_grid
from House import *


def main():

    rectangle_house_mountain, rectangle_building, skeleton_highway, skeleton_mountain, road_grid = world_maker()

    editor = Editor(buffering=True)
    buildArea = editor.getBuildArea()

    # set_roads(skeleton_mountain)
    # set_roads(skeleton_highway)
    # set_roads_grids(road_grid)
    roads.setRoads(skeleton_mountain)
    roads.setRoads(skeleton_highway)

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

    for houses in rectangle_building:
        start = (houses[0][0]+buildArea.begin[0], houses[0]
                 [1], houses[0][2]+buildArea.begin[2])
        end = (houses[1][0]+buildArea.begin[0], houses[1]
               [1], houses[1][2]+buildArea.begin[2])
        house = House(editor, start, end,
                      entranceDirection[random.randint(0, 3)], blocks)
        house.build()

    for houses in rectangle_house_mountain:
        start = (houses[0][0]+buildArea.begin[0], houses[0]
                 [1], houses[0][2]+buildArea.begin[2])
        end = (houses[1][0]+buildArea.begin[0], houses[1]
               [1], houses[1][2]+buildArea.begin[2])
        house = House(editor, start, end,
                      entranceDirection[random.randint(0, 3)], blocks)
        house.build()


def set_roads_grids(road_grid: Road_grid):
    for i in range(len(road_grid)):
        if road_grid[i].border:
            for j in range(len(road_grid)):
                # Same line
                if (road_grid[i].position.x == road_grid[j].position.x and road_grid[i].position.y != road_grid[j].position.y) or (road_grid[i].position.x != road_grid[j].position.x and road_grid[i].position.y == road_grid[j].position.y):
                    point_1 = transpose_form_heightmap(
                        './world_maker/data/heightmap.png', (road_grid[i].position.x, road_grid[i].position.y))
                    point_2 = transpose_form_heightmap(
                        './world_maker/data/heightmap.png', (road_grid[j].position.x, road_grid[j].position.y))
                    Road(
                        [Point3D(point_1[0], point_1[1], point_1[2]), Point3D(point_2[0], point_2[1], point_2[2])], 9)


def set_roads(skeleton: Skeleton):
    # Parsing
    print("[Roads] Start parsing...")
    for i in range(len(skeleton.lines)):
        print(f"[Roads] Parsing skeleton {i+1}/{len(skeleton.lines)}.")
        for j in range(len(skeleton.lines[i])):
            xyz = transpose_form_heightmap('./world_maker/data/heightmap.png',
                                           skeleton.coordinates[skeleton.lines[i][j]])
            skeleton.lines[i][j] = xyz

    print("[Roads] Start simplification...")
    # Simplification
    for i in range(len(skeleton.lines)):
        print(f"[Roads] Simplify skelton {i+1}/{len(skeleton.lines)}")
        skeleton.lines[i] = simplify_coordinates(skeleton.lines[i], 10)

    print("[Roads] Start generation...")
    for i in range(len(skeleton.lines)):
        print(f"[Roads] Generating roads {i+1}/{len(skeleton.lines)}.")
        if len(skeleton.lines[i]) >= 4:
            Road(Point3D.from_arrays(skeleton.lines[i]), 25)
        else:
            print(
                f"[Roads] Ignore roads {i+1} with {len(skeleton.lines[i])} coordinates between {skeleton.lines[i][1]} and {skeleton.lines[i][-1]}.")


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
