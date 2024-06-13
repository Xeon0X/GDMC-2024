from typing import List
from math import atan2, sqrt
import numpy as np


class Point3D:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.coordinate = (x, y, z)

    def copy(self):
        return Point3D(self.x, self.y, self.z)

    def __repr__(self):
        return f"Point3D(x: {self.x}, y: {self.y}, z: {self.z})"

    def __eq__(self, other):
        if isinstance(other, Point3D):
            return self.x == other.x and self.y == other.y and self.z == other.z

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

    def optimized_path(self, points: List["Point3D"]) -> List["Point3D"]:
        """Get an optimized ordered path starting from the current point.

        From: https://stackoverflow.com/questions/45829155/sort-points-in-order-to-have-a-continuous-curve-using-python

        Args:
            points (List[Point3D]): List of 3d-points. Could contain the current point.

        Returns:
            List[Point3D]: Ordered list of 3d-points starting from the current point.

        >>> Point3D(-2, -5, 6).optimized_path([Point3D(0, 0, 7), Point3D(10, 5, 1), Point3D(1, 3, 3)])
        [Point3D(x: -2, y: -5, z: 6), Point3D(x: 0, y: 0, z: 7), Point3D(x: 1, y: 3, z: 3), Point3D(x: 10, y: 5, z: 1)]
        """
        start = self
        if start not in points:
            points.append(start)
        pass_by = points
        path = [start]
        pass_by.remove(start)
        while pass_by:
            nearest = min(pass_by, key=lambda point: point.distance(path[-1]))
            path.append(nearest)
            pass_by.remove(nearest)
        return path

    def round(self, ndigits: int = None) -> "Point3D":
        self.x = round(self.x, ndigits)
        self.y = round(self.y, ndigits)
        self.z = round(self.z, ndigits)
        self.coordinate = (self.x, self.y, self.z)
        return self

    def distance(self, point: "Point3D"):
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2)

    @staticmethod
    def to_vectors(points: List["Point3D"]):
        vectors = []
        for point in points:
            vectors.append(np.array(point.coordinate))

        if (len(vectors) == 1):
            return vectors[0]
        else:
            return vectors
