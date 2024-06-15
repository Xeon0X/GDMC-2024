from world_maker.Position import Position
from typing import Union
from random import randint
from PIL import Image


class Road:
    def __init__(self, position: Position, id_height: int, id_width: int, border: bool = False):
        self.position: Position = position
        self.north: Union[Road, None] = None
        self.south: Union[Road, None] = None
        self.east: Union[Road, None] = None
        self.west: Union[Road, None] = None
        self.id_height = id_height
        self.id_width = id_width
        self.border = border


class District:
    """
    The District class represents a district that can be expanded.

    Attributes:
        center_expend (Position): The center position from which the district expands.
        area (list): The list of positions that are part of the district.
        area_expend_from_point (list): The list of positions from which the district can expand.
        area_expend (list): The list of positions to which the district will maybe expand.
    """

    def __init__(self, tile_id: int, center: Position, district_type: str = ""):
        """
        The constructor for the District class.

        :param tile_id: Unique id of the district (Must be greater than 0)
        :param center: The center position from which the district expands.
        :param district_type: The type of the district (Forest, City, Mountain, Villa)
        """
        if tile_id <= 0:
            raise ValueError("Tile id must be greater than 0")
        self.tile_id = tile_id
        self.type = district_type
        self.center_expend = center
        self.area_expend_from_point = [center]
        self.area_expend = []
        self.roads: list[Road] = []
        self.roads_expend = []

    def verify_point(self, point: Position, point_new: Position, map_data: list[list[int]],
                     height_map: list[list[int]]):
        """
            Verify if a new point can be added to a district extend area list.

            :param point: The current point.
            :param point_new: The new point to be verified.
            :param map_data: The 2D list representing the map.
            :param height_map: The 2D list representing the height map.
            :return: True if the new point can be added, False otherwise.
            """
        return (0 <= point_new.x < len(map_data[0]) and
                0 <= point_new.y < len(map_data) and
                map_data[point_new.y][point_new.x] == 0 and
                (self.type == "mountain" or
                 abs(height_map[point_new.y][point_new.x] - height_map[point.y][point.x]) < 2))

    def is_point_inside(self, point: Position, map_data) -> bool:
        """
        Check if a point is inside the district.

        :param point: The point to be checked.
        :return: True if the point is inside the district, False otherwise.
        """
        if not (0 <= point.x < len(map_data[0]) and 0 <= point.y < len(map_data)):
            return False
        return map_data[point.y][point.x] == self.tile_id

    def is_position_in_area_expend(self, position: Position) -> bool:
        """
        Check if a position is inside the district.

        :param position: The position to be checked.
        :return: True if the position is inside the district, False otherwise.
        """
        for point in self.area_expend:
            if point == position:
                return True
        return False

    def update_expend_points(self, point: Position, map_data: list[list[int]], height_map: list[list[int]]):
        """
        Update the points to which the district can expand.

        :param point: The current point.
        :param map_data: The 2D list representing the map.
        :param height_map: The 2D list representing the height map.
        """
        for pos in [Position(1, 0), Position(-1, 0), Position(0, 1), Position(0, -1)]:
            if self.verify_point(point, point + pos, map_data, height_map):
                if not self.is_position_in_area_expend(point + pos):
                    self.area_expend.append(point + pos)
        self.area_expend_from_point.remove(point)

    def move_point_to_area(self, point: Position, vector: Position, map_data) -> Position:
        while not self.is_point_inside(point + vector, map_data):
            point += vector
        return point + vector

    def get_road_from_point(self, point: Position) -> Union[Road, None]:
        """
        Get the road that contains a specific point.

        :param point: The point to be checked.
        :return: The road that contains the point.
        """
        for road in self.roads:
            if point == road.position:
                return road
        return None

    def get_road_expend_from_point(self, point: Position) -> Union[Road, None]:
        """
        Get the road that contains a specific point.

        :param point: The point to be checked.
        :return: The road that contains the point.
        """
        for road in self.roads_expend:
            if point == road.position:
                return road
        return None

    def generate_roads(self, map_data, random_range=(20, 40)):
        width = {0: self.center_expend.x}
        height = {0: self.center_expend.y}
        self.roads_expend = [Road(self.center_expend, 0, 0)]
        self.roads = [self.roads_expend[0]]
        while len(self.roads_expend) > 0:
            road = self.roads_expend.pop(0)
            print(road.position)
            for id_width in [-1, 1]:
                if road.id_width + id_width not in width:
                    width[road.id_width + id_width] = width[road.id_width] + randint(random_range[0],
                                                                                     random_range[1]) * id_width
                road_new = Road(Position(width[road.id_width + id_width], road.position.y),
                                road.id_height, road.id_width + id_width)
                if self.is_point_inside(road_new.position, map_data):
                    road_search = self.get_road_from_point(road_new.position)
                    road_expend_search = self.get_road_expend_from_point(road_new.position)
                    if road_search is not None:
                        road_new = road_search

                    if id_width == -1:
                        road.west = road_new
                        road_new.east = road
                    else:
                        road.east = road_new
                        road_new.west = road

                    if road_search is None:
                        self.roads.append(road_new)
                        self.roads_expend.append(road_new)
                    else:
                        self.roads[self.roads.index(road_search)] = road_new
                        if road_expend_search is not None:
                            self.roads_expend[self.roads_expend.index(road_expend_search)] = road_new
                else:
                    point_new = self.move_point_to_area(road_new.position, Position(-id_width, 0), map_data)
                    road_new = Road(point_new, road.id_height, road.id_width + id_width, True)
                    if id_width == -1:
                        road.west = road_new
                        road_new.east = road
                    else:
                        road.east = road_new
                        road_new.west = road
                    self.roads.append(road_new)

            for id_height in [-1, 1]:
                if road.id_height + id_height not in height:
                    height[road.id_height + id_height] = height[road.id_height] + randint(random_range[0],
                                                                                          random_range[1]) * id_height
                road_new = Road(Position(road.position.x, height[road.id_height + id_height]),
                                road.id_height + id_height, road.id_width)
                if self.is_point_inside(road_new.position, map_data):
                    road_search = self.get_road_from_point(road_new.position)
                    road_expend_search = self.get_road_expend_from_point(road_new.position)
                    if road_search is not None:
                        road_new = road_search

                    if id_height == -1:
                        road.north = road_new
                        road_new.south = road
                    else:
                        road.south = road_new
                        road_new.north = road

                    if road_search is None:
                        self.roads.append(road_new)
                        self.roads_expend.append(road_new)
                    else:
                        self.roads[self.roads.index(road_search)] = road_new
                        if road_expend_search is not None:
                            self.roads_expend[self.roads_expend.index(road_expend_search)] = road_new
                else:
                    pass
                    point_new = self.move_point_to_area(road_new.position, Position(0, -id_height), map_data)
                    road_new = Road(point_new, road.id_height + id_height, road.id_width, True)
                    if id_height == -1:
                        road.north = road_new
                        road_new.south = road
                    else:
                        road.south = road_new
                        road_new.north = road
                    self.roads.append(road_new)

    def draw_roads(self, image: Image, size: int = 1):
        for road in self.roads:
            image.putpixel((road.position.x, road.position.y), (255, 255, 255))
            if road.north is not None:
                for y in range(road.position.y, road.north.position.y):
                    image = draw_square(image, Position(road.position.x, y), size)
            if road.south is not None:
                for y in range(road.position.y, road.south.position.y):
                    image = draw_square(image, Position(road.position.x, y), size)
            if road.east is not None:
                for x in range(road.position.x, road.east.position.x):
                    image = draw_square(image, Position(x, road.position.y), size)
            if road.west is not None:
                for x in range(road.position.x, road.west.position.x):
                    image = draw_square(image, Position(x, road.position.y), size)


def draw_square(image, center: Position, size: int) -> Image:
    for x in range(center.x - size, center.x + size):
        for y in range(center.y - size, center.y + size):
            if 0 <= x < image.width and 0 <= y < image.height:
                image.putpixel((x, y), (255, 255, 255))
    return image
