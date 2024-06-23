import random

from gdpc import Editor

from House import *
from networks.geometry.Point3D import Point3D
from networks.roads_2.Road import Road
from world_maker.data_analysis import transpose_form_heightmap
from world_maker.District import Road as Road_grid
from world_maker.Skeleton import Skeleton, simplify_coordinates
from world_maker.terraforming import remove_trees, smooth_terrain
from world_maker.world_maker import world_maker
from networks.geometry.Point3D import Point3D
from networks.geometry.Point3D import Point3D


def main():
    y = 50
    Road([Point3D(3903, 137+y, -142), Point3D(3948, 111+y, -148),
         Point3D(3967, 112+y, -116), Point3D(4011, 112+y, -99)], 25)
    # rectangle_house_mountain, rectangle_building, skeleton_highway, skeleton_mountain, road_grid = world_maker()

    # editor = Editor(buffering=True)
    # buildArea = editor.getBuildArea()
    # origin = ((buildArea.begin).x, (buildArea.begin).z)

    # remove_trees('./world_maker/data/heightmap.png', './world_maker/data/treemap.png',
    #              './world_maker/data/smooth_sobel_watermap.png')
    # smooth_terrain('./world_maker/data/heightmap.png',
    #                './world_maker/data/heightmap_smooth.png', './world_maker/data/smooth_sobel_watermap.png')

    # set_roads(skeleton_mountain, origin)
    # set_roads(skeleton_highway, origin)
    # # set_roads_grids(road_grid, origin)
    # # roads.setRoads(skeleton_mountain)
    # # roads.setRoads(skeleton_highway)

    # blocks = {
    #     "wall": "blackstone",
    #     "roof": "blackstone",
    #     "roof_slab": "blackstone_slab",
    #     "door": "oak_door",
    #     "window": "glass_pane",
    #     "entrance": "oak_door",
    #     "stairs": "quartz_stairs",
    #     "stairs_slab": "quartz_slab",
    #     "celling": "quartz_block",
    #     "floor": "quartz_block",
    #     "celling_slab": "quartz_slab",
    #     "garden_outline": "oak_leaves",
    #     "garden_floor": "grass_block"
    # }

    # entranceDirection = ["N", "S", "E", "W"]

    # for houses in rectangle_building:
    #     start = (houses[0][0]+buildArea.begin[0], houses[0]
    #              [1], houses[0][2]+buildArea.begin[2])
    #     end = (houses[1][0]+buildArea.begin[0], houses[1]
    #            [1], houses[1][2]+buildArea.begin[2])
    #     house = House(editor, start, end,
    #                   entranceDirection[random.randint(0, 3)], blocks)
    #     house.build()

    # for houses in rectangle_house_mountain:
    #     start = (houses[0][0]+buildArea.begin[0], houses[0]
    #              [1], houses[0][2]+buildArea.begin[2])
    #     end = (houses[1][0]+buildArea.begin[0], houses[1]
    #            [1], houses[1][2]+buildArea.begin[2])
    #     house = House(editor, start, end,
    #                   entranceDirection[random.randint(0, 3)], blocks)
    #     house.build()


def set_roads_grids(road_grid: Road_grid, origin):
    for i in range(len(road_grid)):
        if road_grid[i].border:
            for j in range(len(road_grid)):
                # Same line
                if (road_grid[i].position.x == road_grid[j].position.x and road_grid[i].position.y != road_grid[j].position.y) or (road_grid[i].position.x != road_grid[j].position.x and road_grid[i].position.y == road_grid[j].position.y):
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
        print(f"[Roads] Parsing skeleton {i+1}/{len(skeleton.lines)}.")
        for j in range(len(skeleton.lines[i])):
            xyz = transpose_form_heightmap('./world_maker/data/heightmap.png',
                                           skeleton.coordinates[skeleton.lines[i][j]], origin)
            skeleton.lines[i][j] = xyz

    print("[Roads] Start simplification...")
    # Simplification
    for i in range(len(skeleton.lines)):
        print(f"[Roads] Simplify skelton {i+1}/{len(skeleton.lines)}")
        skeleton.lines[i] = simplify_coordinates(skeleton.lines[i], 40)

    print("[Roads] Start generation...")
    for i in range(len(skeleton.lines)):
        print(f"[Roads] Generating roads {i+1}/{len(skeleton.lines)}.")
        if len(skeleton.lines[i]) >= 4:
            Road(Point3D.from_arrays(skeleton.lines[i]), 9)
        else:
            print(
                f"[Roads] Ignore roads {i+1} with {len(skeleton.lines[i])} coordinates between {skeleton.lines[i][1]} and {skeleton.lines[i][-1]}.")


if __name__ == '__main__':
    main()
