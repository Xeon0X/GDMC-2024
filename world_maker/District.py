from Position import Position

class District:
    """
    The CustomDistrict class represents a district that can be expanded.

    Attributes:
        center_expend (Position): The center position from which the district expands.
        area (list): The list of positions that are part of the district.
        area_expend_from_point (list): The list of positions from which the district can expand.
        area_expend (list): The list of positions to which the district will maybe expand.
    """
    def __init__(self, tile_id: int, center: Position, type: str = ""):
        """
        The constructor for the District class.

        :param tile_id: Unique id of the district (Must be greater than 0)
        :param center: The center position from which the district expands.
        :param type: The type of the district (Forest, City, Mountain, Villa)
        """
        if tile_id <= 0:
            raise ValueError("Tile id must be greater than 0")
        self.tile_id = tile_id
        self.type = type
        self.center_expend = center
        self.area = [center]
        self.area_expend_from_point = [center]
        self.area_expend = []

    def verify_point(self, point: Position, point_new: Position, map_data: list[list[int]], height_map: list[list[int]]):
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
                    (self.type == "Mountain" or
                    abs(height_map[point_new.y][point_new.x] - height_map[point.y][point.x]) < 2))

    def update_expend_points(self, point: Position, map_data: list[list[int]], height_map: list[list[int]]):
        """
        Update the points to which the district can expand.

        :param point: The current point.
        :param map_data: The 2D list representing the map.
        :param height_map: The 2D list representing the height map.
        """
        for pos in [Position(1, 0), Position(-1, 0), Position(0, 1), Position(0, -1)]:
            if self.verify_point(point, point + pos, map_data, height_map):
                if point + pos not in self.area_expend:
                    self.area_expend.append(point + pos)
        self.area_expend_from_point.remove(point)
