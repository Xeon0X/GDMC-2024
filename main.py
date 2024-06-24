import random
from math import exp, sqrt

from gdpc import Editor, Block, geometry, Transform

from House import *
from networks.geometry.Point3D import Point3D
from networks.roads_2.Road import Road
from world_maker.data_analysis import transpose_form_heightmap
from world_maker.District import Road as Road_grid
from world_maker.Skeleton import Skeleton, simplify_coordinates
from world_maker.terraforming import remove_trees, smooth_terrain
from world_maker.world_maker import world_maker
from networks.geometry.Point3D import Point3D
from networks.geometry.Point2D import Point2D
from networks.geometry.Circle import Circle

from PIL import Image
from utils.JsonReader import JsonReader
from utils.YamlReader import YamlReader
from buildings.Building import Building

from utils.functions import *
from utils.Enums import DIRECTION


def main():
    rectangle_house_mountain, rectangle_building, skeleton_highway, skeleton_mountain, road_grid = world_maker()

    editor = Editor(buffering=True)
    buildArea = editor.getBuildArea()
    origin = ((buildArea.begin).x, (buildArea.begin).z)
    center = (abs(buildArea.begin.x - buildArea.end.x) / 2,
              abs(buildArea.begin.z - buildArea.end.z) / 2)
    length_world = sqrt((center[0]*2) ** 2 + (center[1]*2) ** 2)

    # remove_trees('./world_maker/data/heightmap.png', './world_maker/data/treemap.png',
    #              './world_maker/data/smooth_sobel_watermap.png')
    # smooth_terrain('./world_maker/data/heightmap.png',
    #                './world_maker/data/heightmap_smooth.png', './world_maker/data/smooth_sobel_watermap.png')

    # set_roads(skeleton_highway, origin)
    # set_roads(skeleton_mountain, origin)
    # set_roads_grids(road_grid, origin)
    # roads.setRoads(skeleton_mountain)
    # roads.setRoads(skeleton_highway)

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

    # get every differents buildings shapes
    f = JsonReader('./buildings/shapes.json')
    shapes = f.data
    baseShape = shapes[0]['matrice']

    # get the random data for the buildings
    y = YamlReader('params.yml')
    random_data = y.data

    # move your editor wto the position you wanna build on
    transform = Transform((75, -60, 110), rotation=0)
    editor.transform.push(transform)

    # clear the area you build on
    geometry.placeCuboid(editor, (-5, 0, -8), (25, 100, 25), Block("air"))

    # create a building at the relative position 0,0 with 20 blocks length and 20 blocks width, with a normal shape and 10 floors

    # build it with your custom materials

    for buildings in rectangle_building:
        height = get_height_building_from_center(
            center, (buildings[0][0], buildings[0][2]), length_world)
        start = (min(buildings[0][0], buildings[1][0]) + origin[0], buildings[0]
                 [1], min(buildings[0][2], buildings[1][2]) + origin[1])
        end = (max(buildings[0][0], buildings[1][0]) + origin[0], buildings[1]
               [1], max(buildings[0][2], buildings[1][2]) + origin[1])

        transform = Transform(start, rotation=0)
        editor.transform.push(transform)

        building = Building(random_data["buildings"], [
            (0, 0, 0), (end[0] - start[0], height, end[2] - start[2])], baseShape, DIRECTION.EAST)
        building.build(editor, ["stone_bricks", "glass_pane", "glass", "cobblestone_wall", "stone_brick_stairs",
                                "oak_planks", "white_concrete", "cobblestone", "stone_brick_slab", "iron_bars"])

    for buildings in rectangle_house_mountain:
        start = (buildings[0][0] + origin[0], buildings[0]
                 [1], buildings[0][2] + origin[1])
        end = (buildings[1][0] + origin[0], buildings[1]
               [1], buildings[1][2] + origin[1])
        house = House(editor, start, end,
                      entranceDirection[random.randint(0, 3)], blocks)
        house.build()


def get_height_building_from_center(center, position, length_world):
    length = abs(
        sqrt(((center[0] - position[0]) ** 2 + (center[1] - position[1]) ** 2)))
    print(length, length_world)
    return int(exp(-(length / (length_world / 4)) ** 2) * 75 + 30)


def set_roads_grids(road_grid: Road_grid, origin):
    for i in range(len(road_grid)):
        if road_grid[i].border:
            for j in range(len(road_grid)):
                # Same line
                if (road_grid[i].position.x == road_grid[j].position.x and road_grid[i].position.y != road_grid[
                    j].position.y) or (
                        road_grid[i].position.x != road_grid[j].position.x and road_grid[i].position.y == road_grid[
                            j].position.y):
                    point_1 = transpose_form_heightmap(
                        './world_maker/data/heightmap.png', (road_grid[i].position.x, road_grid[i].position.y), origin)
                    point_2 = transpose_form_heightmap(
                        './world_maker/data/heightmap.png', (road_grid[j].position.x, road_grid[j].position.y), origin)
                    Road(
                        [Point3D(point_1[0], point_1[1], point_1[2]), Point3D(point_2[0], point_2[1], point_2[2])], 9)


def set_roads(skeleton: Skeleton, origin):
    # Parsing
    print("[Roads] Start parsing...")
    for i in range(len(skeleton.lines)):
        print(f"[Roads] Parsing skeleton {i + 1}/{len(skeleton.lines)}.")
        for j in range(len(skeleton.lines[i])):
            xyz = transpose_form_heightmap('./world_maker/data/heightmap.png',
                                           skeleton.coordinates[skeleton.lines[i][j]], origin)
            heightmap_smooth = Image.open(
                './world_maker/data/full_road_heightmap_smooth.png')
            skeleton.lines[i][j] = [xyz[0], heightmap_smooth.getpixel(
                (skeleton.coordinates[skeleton.lines[i][j]][0], skeleton.coordinates[skeleton.lines[i][j]][-1])), xyz[2]]

    print("[Roads] Start simplification...")
    # Simplification
    for i in range(len(skeleton.lines)):
        print(f"[Roads] Simplify skelton {i + 1}/{len(skeleton.lines)}")
        print(f"[Roads] Number of points: {len(skeleton.lines[i])}")
        skeleton.lines[i] = simplify_coordinates(skeleton.lines[i], 20)
        j = 0
        while j < len(skeleton.lines[i])-1:
            print(f"[Distance] {Point3D(skeleton.lines[i][j][0], skeleton.lines[i][j][1], skeleton.lines[i][j][2]).distance(Point3D(skeleton.lines[i][j+1][0], skeleton.lines[i][j+1][1], skeleton.lines[i][j+1][2]))}")
            if Point3D(skeleton.lines[i][j][0], skeleton.lines[i][j][1], skeleton.lines[i][j][2]).distance(Point3D(skeleton.lines[i][j+1][0], skeleton.lines[i][j+1][1], skeleton.lines[i][j+1][2])) <= 20:
                print(skeleton.lines[i][j+1], skeleton.lines[i][j])
                del skeleton.lines[i][j+1]
                print("[Roads] Delete point to close")
            j += 1
        j = 0
        while j < len(skeleton.lines[i])-1:
            print(f"[Distance] {Point3D(skeleton.lines[i][j][0], skeleton.lines[i][j][1], skeleton.lines[i][j][2]).distance(Point3D(skeleton.lines[i][j+1][0], skeleton.lines[i][j+1][1], skeleton.lines[i][j+1][2]))}")
            if Point3D(skeleton.lines[i][j][0], skeleton.lines[i][j][1], skeleton.lines[i][j][2]).distance(Point3D(skeleton.lines[i][j+1][0], skeleton.lines[i][j+1][1], skeleton.lines[i][j+1][2])) <= 10:
                print(skeleton.lines[i][j+1], skeleton.lines[i][j])
                del skeleton.lines[i][j+1]
                print("[Roads] Delete point to close")
            j += 1
        j = 0
        while j < len(skeleton.lines[i])-1:
            print(f"[Distance] {Point3D(skeleton.lines[i][j][0], skeleton.lines[i][j][1], skeleton.lines[i][j][2]).distance(Point3D(skeleton.lines[i][j+1][0], skeleton.lines[i][j+1][1], skeleton.lines[i][j+1][2]))}")
            if Point3D(skeleton.lines[i][j][0], skeleton.lines[i][j][1], skeleton.lines[i][j][2]).distance(Point3D(skeleton.lines[i][j+1][0], skeleton.lines[i][j+1][1], skeleton.lines[i][j+1][2])) <= 10:
                print(skeleton.lines[i][j+1], skeleton.lines[i][j])
                del skeleton.lines[i][j+1]
                print("[Roads] Delete point to close")
            j += 1
        print(
            f"[Roads] Number of points after simplification: {len(skeleton.lines[i])}")

    print("[Roads] Start generation...")
    for i in range(len(skeleton.lines)):
        print(f"[Roads] Generating roads {i + 1}/{len(skeleton.lines)}.")
        if len(skeleton.lines[i]) >= 4:
            Road(Point3D.from_arrays(skeleton.lines[i]), 9)
            print(f"[ROAD] Points: {skeleton.lines[i]}")


if __name__ == '__main__':
    main()
