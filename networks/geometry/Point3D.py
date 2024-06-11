from typing import List
from math import atan2, sqrt


class Point3D:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def copy(self):
        return Point3D(self.x, self.y, self.z)

    def coordinates(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return f"Point3D(x: {self.x}, y: {self.y}, z: {self.z})"

    def distance(self, point: "Point3D"):
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2)

    def nearest(self, points: List["Point3D"]) -> "Point3D":
        """Return the nearest point. If multiple nearest point, returns the first in the list.

        Args:
            points (List[Point2D]): List of the points to test.

        Returns:
            Point3D: The nearest point, and if multiple, the first in the list.

        >>> print(Point3D(0, 0, 0).nearest((Point3D(-10, 10, 5), Point3D(10, 10, 1))))
        Point3D(x: 10, y: 10, z: 1)
        """
        return min(points, key=lambda point: self.distance(point))

    def round(self, ndigits: int = None) -> "Point3D":
        self.x = round(self.x, ndigits)
        self.y = round(self.y, ndigits)
        self.z = round(self.z, ndigits)
        self.coordinate = (self.x, self.y, self.z)
        return self
