from math import sqrt, atan2


class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> "Position":
        return Position(int(self.x * other), int(self.y * other))

    def __truediv__(self, other: float) -> "Position":
        return Position(int(self.x / other), int(self.y / other))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Position"):
        return self.x == other.x and self.y == other.y

    def distance_to(self, other: "Position") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def norm(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def angle_to(self, other: "Position") -> float:
        return atan2(self.y - other.y, other.x - self.x)


class Station:
    """
    This class represents the position and link of a metro station.
    """

    def __init__(self, pos: Position, orientation: float, name: str = "Station"):
        """
        Constructor of Station.

        :param pos: Position x and y of the station
        :param orientation: The orientation of the station in radian (The angle is where the station is facing next)
        :param name: The name of the station
        """
        self.name = name
        self.orientation = orientation
        self.pos = pos
        self.last_station = None
        self.next_station = None

    def distance_to(self, station: "Station") -> float:
        """
        Calculate the distance between two stations.

        :param station: The station to calculate the distance to
        :return: The distance between two stations
        """
        return self.pos.distance_to(station.pos)


class Metro_Line:
    """
    This class represents the metro line.
    """

    def __init__(self, name: str = "Metro line A"):
        """
        Constructor of Metro_Line.

        :param name: The name of the metro line
        """
        self.name = name
        self.stations = []

    def add_station(self, station: Station):
        """
        Add a station to the metro map.

        :param station: The station to be added
        """
        self.stations.append(station)
        if len(self.stations) > 1:
            self.stations[-2].next_station = station
            station.last_station = self.stations[-2]


__all__ = ["Metro_Line", "Station", "Position"]
