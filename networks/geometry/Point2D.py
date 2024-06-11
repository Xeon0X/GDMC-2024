from typing import Type


class Point2D:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def copy(self):
        return Point2D(self.x, self.y)

    def coordinates(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Point2D(x: {self.x}, y: {self.y})"

    def is_in_triangle(self, xy0: Type[Point2D], xy1: Type[Point2D], xy2: Type[Point2D]):
        """Returns True is the point is in a triangle defined by 3 others points.

        From: https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle#:~:text=A%20simple%20way%20is%20to,point%20is%20inside%20the%20triangle.

        Args:
            xy0 (Type[Point2D]): Point of the triangle.
            xy1 (Type[Point2D]): Point of the triangle.
            xy2 (Type[Point2D]): Point of the triangle.

        Returns:
            bool: False if the point is not inside the triangle.
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

    def distance(self, point: Type[Point2D]):
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)
