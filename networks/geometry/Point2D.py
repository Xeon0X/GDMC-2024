import numpy as np
from typing import List
from math import atan2, sqrt
from Enums import ROTATION


class Point2D:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.coordinate = (self.x, self.y)

    def copy(self):
        return Point2D(self.x, self.y)

    def __repr__(self):
        return f"Point2D(x: {self.x}, y: {self.y})"

    def __eq__(self, other):
        if isinstance(other, Point2D):
            return self.x == other.x and self.y == other.y
        return False

    def is_in_triangle(self, xy0: "Point2D", xy1: "Point2D", xy2: "Point2D"):
        """Returns True is the point is in a triangle defined by 3 others points.

        From: https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle#:~:text=A%20simple%20way%20is%20to,point%20is%20inside%20the%20triangle.

        Args:
            xy0 (Type[Point2D]): Point of the triangle.
            xy1 (Type[Point2D]): Point of the triangle.
            xy2 (Type[Point2D]): Point of the triangle.

        Returns:
            bool: False if the point is not inside the triangle.

        >>> Point2D(0, 0).is_in_triangle(Point2D(10, 10), Point2D(-10, 20), Point2D(0, -20)))
        True
        """
        dx = self.x - xy0.x
        dy = self.y - xy0.y

        dx2 = xy2.x - xy0.x
        dy2 = xy2.y - xy0.y
        dx1 = xy1.x - xy0.x
        dy1 = xy1.y - xy0.y

        s_p = (dy2 * dx) - (dx2 * dy)
        t_p = (dx1 * dy) - (dy1 * dx)
        d = (dx1 * dy2) - (dy1 * dx2)

        if d > 0:
            return (s_p >= 0) and (t_p >= 0) and (s_p + t_p) <= d
        else:
            return (s_p <= 0) and (t_p <= 0) and (s_p + t_p) >= d

    def distance(self, point: "Point2D") -> int:
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)

    def nearest(self, points: List["Point2D"]) -> "Point2D":
        """Return the nearest point. If multiple nearest point, returns the first in the list.

        Args:
            points (List[Point2D]): List of the points to test.

        Returns:
            Point2D: The nearest point, and if multiple, the first in the list.
        """
        return min(points, key=lambda point: self.distance(point))

    def optimized_path(self, points: List["Point2D"]) -> List["Point2D"]:
        """Get an optimized ordered path starting from the current point.

        From: https://stackoverflow.com/questions/45829155/sort-points-in-order-to-have-a-continuous-curve-using-python

        Args:
            points (List[Point2D]): List of 2d-points. Could contain the current point.

        Returns:
            List[Point2D]: Ordered list of 2d-points starting from the current point.

        >>> Point2D(-2, -5).optimized_path([Point2D(0, 0), Point2D(10, 5), Point2D(1, 3)])
        [Point2D(x: -2, y: -5), Point2D(x: 0, y: 0), Point2D(x: 1, y: 3), Point2D(x: 10, y: 5)]
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

    def sort_by_rotation(self, points: List["Point2D"], rotation: ROTATION = ROTATION.CLOCKWISE) -> List["Point2D"]:
        """Sort points in clockwise order, starting from current point.

        From: https://stackoverflow.com/questions/58377015/counterclockwise-sorting-of-x-y-data

        Args:
            points (List[Point2D]): List of 2d-points. Current point can be included here.
            rotation (ROTATION): Can be ROTATION.CLOCKWISE or ROTATION.COUNTERCLOCKWISE. Optional. Defaults to ROTATION.CLOCKWISE.

        Returns:
            List[Point2D]: List of 2d-points.

        >>> Point2D(-10, -10).sort_by_rotation([Point2D(10, 10), Point2D(-10, 10), Point2D(10, -10)])
        [Point2D(x: -10, y: -10), Point2D(x: 10, y: -10), Point2D(x: 10, y: 10), Point2D(x: -10, y: 10)]
        """
        if self not in points:
            points.append(self)
        x, y = [], []
        for i in range(len(points)):
            x.append(points[i].x)
            y.append(points[i].y)
        x, y = np.array(x), np.array(y)

        x0 = np.mean(x)
        y0 = np.mean(y)

        r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)

        angles = np.where(
            (y - y0) > 0,
            np.arccos((x - x0) / r),
            2 * np.pi - np.arccos((x - x0) / r),
        )

        mask = np.argsort(angles)

        x_sorted = list(x[mask])
        y_sorted = list(y[mask])

        # Rearrange tuples to get the correct coordinates.
        sorted_points = []
        for i in range(len(points)):
            j = 0
            while (x_sorted[i] != points[j].x) and (y_sorted[i] != points[j].y):
                j += 1
            else:
                sorted_points.append(Point2D(x_sorted[i], y_sorted[i]))

        if rotation == ROTATION.CLOCKWISE:
            sorted_points.reverse()
            start_index = sorted_points.index(self)
            return sorted_points[start_index:] + sorted_points[:start_index]
        else:
            start_index = sorted_points.index(self)
            return sorted_points[start_index:] + sorted_points[:start_index]

    def angle(self, xy1, xy2):
        """
        Compute angle (in degrees). Corner in current point.

        From: https://stackoverflow.com/questions/13226038/calculating-angle-between-two-vectors-in-python

        Args:
            xy0 (numpy.ndarray): Points in the form of [x,y].
            xy1 (numpy.ndarray): Points in the form of [x,y].
            xy2 (numpy.ndarray): Points in the form of [x,y].

        Returns:
            float: Angle negative for counterclockwise angle, angle positive
            for counterclockwise angle.

        >>> Point2D(0, 0).angle(Point2D(10, 10), Point2D(0, -20))
        -135.0
        """
        if xy2 is None:
            xy2 = xy1.coordinate + np.array([1, 0])
        v0 = np.array(xy1.coordinate) - np.array(self.coordinate)
        v1 = np.array(xy2.coordinate) - np.array(self.coordinate)

        angle = atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
        return np.degrees(angle)

    def round(self, ndigits: int = None) -> "Point2D":
        self.x = round(self.x, ndigits)
        self.y = round(self.y, ndigits)
        self.coordinate = (self.x, self.y)
        return self

    @staticmethod
    def to_vectors(points: List["Point3D"]) -> List[np.array]:
        vectors = []
        for point in points:
            vectors.append(np.array(point.coordinate))

        if (len(vectors) == 1):
            return vectors[0]
        else:
            return vectors
