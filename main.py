import random

import gdpc.exceptions

from world_maker.world_maker import *
from world_maker.data_analysis import transpose_form_heightmap
from world_maker.Skeleton import Skeleton, simplify_coordinates
from world_maker.terraforming import remove_trees, smooth_terrain
from networks.geometry.Point3D import Point3D
from networks.geometry.Point2D import Point2D
from networks.geometry.Segment2D import Segment2D
from networks.roads_2.Road import Road
from networks.legacy_roads import roads
from world_maker.District import Road as Road_grid
from networks.geometry.Circle import Circle
from House import *
from gdpc import Editor, Block
from utils.Enums import LINE_THICKNESS_MODE


def main():
    editor = Editor(buffering=False)
    # c = Circle(Point2D(400, -75)).circle_thick_by_line(5, 32)
    # for i in range(len(c[0])):
    #     for j in range(len(c[0][i])):
    #         if i % 2 == 0:
    #             editor.placeBlock(
    #                 (c[0][i][j].x, 110, c[0][i][j].y), Block("white_concrete"))
    #         else:
    #             editor.placeBlock(
    #                 (c[0][i][j].x, 110, c[0][i][j].y), Block("black_concrete"))
    # print(c[1])
    # for i in range(len(c[1])):
    #     for j in range(len(c[1][i])):
    #         editor.placeBlock(
    #             (c[1][i][j].x, 110, c[1][i][j].y), Block("red_concrete"))

    def place_segment(segment):
        segment.segment_thick(30, LINE_THICKNESS_MODE.MIDDLE)
        for i in range(len(segment.points_thick_by_line)):
            kk = i % 7
            match kk:
                case 0:
                    blob = 'pink_concrete'
                case 1:
                    blob = 'red_concrete'
                case 2:
                    blob = 'orange_concrete'
                case 3:
                    blob = 'yellow_concrete'
                case 4:
                    blob = 'green_concrete'
                case 5:
                    blob = 'blue_concrete'
                case 6:
                    blob = 'purple_concrete'
            for j in range(len(segment.points_thick_by_line[i])):
                editor.placeBlock(Point3D.insert_3d(
                    [segment.points_thick_by_line[i][j]], 'y', [134])[0].coordinates, Block(blob))
        for i in range(len(segment.gaps)):
            kk = i % 7
            match kk:
                case 0:
                    blob = 'pink_concrete'
                case 1:
                    blob = 'red_concrete'
                case 2:
                    blob = 'orange_concrete'
                case 3:
                    blob = 'yellow_concrete'
                case 4:
                    blob = 'green_concrete'
                case 5:
                    blob = 'blue_concrete'
                case 6:
                    blob = 'purple_concrete'
            for j in range(len(segment.gaps[i])):
                editor.placeBlock(Point3D.insert_3d(
                    [segment.gaps[i][j]], 'y', [135])[0].coordinates, Block(blob))

    # place_segment(Segment2D(Point2D(147, -616), Point2D(132, -554)))
    # # place_segment(Segment2D(Point2D(147, -616), Point2D(117, -563)))
    # # place_segment(Segment2D(Point2D(147, -616), Point2D(97, -576)))
    # # place_segment(Segment2D(Point2D(147, -616), Point2D(71, -625)))
    # # place_segment(Segment2D(Point2D(147, -616), Point2D(115, -655)))
    # # place_segment(Segment2D(Point2D(147, -616), Point2D(162, -682)))
    # # place_segment(Segment2D(Point2D(147, -616), Point2D(195, -665)))
    # # place_segment(Segment2D(Point2D(147, -616), Point2D(204, -622)))
    # # place_segment(Segment2D(Point2D(147, -616), Point2D(178, -575)))

    x = 200

    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(50+x, 0)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(50+x, 25)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(50+x, 50)))
    place_segment(Segment2D(Point2D(0+x, 0), Point2D(25+x, 50)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(0+x, 50)))
    place_segment(Segment2D(Point2D(0+x, 0), Point2D(-25+x, 50)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(-50+x, 50)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(-50+x, 25)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(-50+x, 0)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(-50+x, -25)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(-50+x, -50)))
    place_segment(Segment2D(Point2D(0+x, 0), Point2D(-25+x, -50)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(0+x, -50)))
    place_segment(Segment2D(Point2D(0+x, 0), Point2D(25+x, -50)))
    # place_segment(Segment2D(Point2D(0+x, 0), Point2D(50+x, -50)))

    # place_segment(Segment2D(Point2D(147, -616), Point2D(201, -595)))
    # place_segment(Segment2D(Point2D(147, -616), Point2D(233, -605)))

    y = 105

    # Road([Point3D(121, 108+y, -68), Point3D(163, 108+y, -95), Point3D(173, 108+y, -169), Point3D(188, 108+y, -174), Point3D(229,
    #      108+y, -217), Point3D(190, 95+y, -270), Point3D(198, 95+y, -297), Point3D(237, 95+y, -287), Point3D(283, 95+y, -328)], 15)

    # Road([Point3D(464, 85+10, -225), Point3D(408, 105+10, -224),
    #      Point3D(368, 104+10, -249), Point3D(368, 85+10, -296), Point3D(457, 79+10, -292)], 15)
    # Road([Point3D(526, 70, -415), Point3D(497, 76, -420), Point3D(483, 70, -381), Point3D(460, 71, -360), Point3D(430, 78, -383), Point3D(410, 71, -364), Point3D(381,
    #      71, -383), Point3D(350, 76, -375), Point3D(332, 79, -409), Point3D(432, 71, -460), Point3D(450, 70, -508), Point3D(502, 81, -493), Point3D(575, 85, -427)], 15)
    # rectangle_house_mountain, rectangle_building, ske,leton_highway, skeleton_mountain, road_grid = world_maker()

    # editor = Editor(buffering=True)
    # buildArea = editor.getBuildArea()
    # origin = ((buildArea.begin).x, (buildArea.begin).z)

    # remove_trees('./world_maker/data/heightmap.png', './world_maker/data/treemap.png',
    #              './world_maker/data/smooth_sobel_watermap.png')
    # smooth_terrain('./world_maker/data/heightmap.png',
    #                './world_maker/data/heightmap_smooth.png', './world_maker/data/smooth_sobel_watermap.png')

    # # set_roads(skeleton_mountain, origin)
    # # set_roads(skeleton_highway, origin)
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
