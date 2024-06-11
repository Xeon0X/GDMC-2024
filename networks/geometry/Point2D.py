import numpy as np
import math


class Point2D:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.coordinate = (self.x, self.y)

    def copy(self):
        return Point2D(self.x, self.y)

    def __repr__(self):
        return f"Point2D(x: {self.x}, y: {self.y})"

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

    def distance(self, point: "Point2D"):
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)

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

        angle = math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
        return np.degrees(angle)
