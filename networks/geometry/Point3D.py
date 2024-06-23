from math import sqrt
from typing import List, Union
from networks.geometry.Point2D import Point2D

import numpy as np


class Point3D:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.coordinates = (x, y, z)

    def copy(self):
        return Point3D(self.x, self.y, self.z)

    def __repr__(self):
        return f"Point3D(x: {self.x}, y: {self.y}, z: {self.z})"

    def __eq__(self, other):
        if isinstance(other, Point3D):
            return self.x == other.x and self.y == other.y and self.z == other.z

    def nearest(self, points: List["Point3D"], return_index=False) -> "Point3D":
        """Return the nearest point. If multiple nearest point, returns the first in the list.

        Args:
            points (List[Point2D]): List of the points to test.

        Returns:
            Point3D: The nearest point, and if multiple, the first in the list.

        >>> Point3D(0, 0, 0).nearest((Point3D(-10, 10, 5), Point3D(10, 10, 1)))
        Point3D(x: 10, y: 10, z: 1)
        """
        if return_index:
            return min(
                enumerate(points), key=lambda pair: self.distance(pair[1]))
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
        self.coordinates = (self.x, self.y, self.z)
        return self

    def distance(self, point: "Point3D"):
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2)

    @staticmethod
    def to_arrays(points: Union[List["Point3D"], "Point3D"]) -> Union[List[np.array], "Point3D"]:
        if isinstance(points, list):
            vectors = []
            for point in points:
                vectors.append(np.array(point.coordinates))
            return vectors
        else:
            return np.array(points.coordinates)

    @staticmethod
    def from_arrays(vectors: Union[List[np.array], "Point3D"]) -> Union[List["Point3D"], "Point3D"]:
        if isinstance(vectors, list):
            points = []
            for vector in vectors:
                points.append(Point3D(vector[0], vector[1], vector[2]))
            return points
        else:
            return Point3D(vectors[0], vectors[1], vectors[2])

    @staticmethod
    def to_2d(points: List["Point3D"], removed_axis: str) -> List[Point2D]:
        points_2d = []
        if removed_axis == 'x':
            for i in range(len(points)):
                points_2d.append(Point2D(points[i].y, points[i].z))
        if removed_axis == 'y':
            for i in range(len(points)):
                points_2d.append(Point2D(points[i].x, points[i].z))
        if removed_axis == 'z':
            for i in range(len(points)):
                points_2d.append(Point2D(points[i].x, points[i].y))
        return points_2d

    @staticmethod
    def insert_3d(points: List[Point2D], position: str, to_insert: List[int]) -> List["Point3D"]:
        points_3d = []
        if position == 'x':
            for i in range(len(points)):
                points_3d.append(
                    Point3D(to_insert[i], points[i].x, points[i].y))
        if position == 'y':
            for i in range(len(points)):
                points_3d.append(
                    Point3D(points[i].x, to_insert[i], points[i].y))
        if position == 'z':
            for i in range(len(points)):
                points_3d.append(
                    Point3D(points[i].x, points[i].y, to_insert[i]))
        return points_3d
