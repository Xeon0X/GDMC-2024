from networks.geometry.Point2D import Point2D
from math import cos, sin, pi
from typing import List


class Circle:
    def __init__(self, center: Point2D, inner: int, outer: int):
        self.center = center

        self.inner = inner
        self.outer = outer
        self.coordinates = []

        self.radius = None  # Used with circle_points()
        self.spaced_coordinates = []

        self.circle(self.center, self.inner, self.outer)

    def __repr__(self):
        return f"Circle(center: {self.center}, inner: {self.inner}, outer: {self.outer})"

    def circle(self, center: Point2D, inner: int, outer: int) -> List[Point2D]:
        """Compute discrete value of a 2d-circle with thickness. 

        https://stackoverflow.com/questions/27755514/circle-with-thickness-drawing-algorithm

        Args:
            center (Type[Point2D]): Center of the circle. Circles always have an odd diameter due to the central coordinate.
            inner (int): The minimum radius at which the disc is filled (included).
            outer (int): The maximum radius where disc filling stops (included).

        Returns:
            list(Point2D): List of 2d-coordinates composing the surface. Note that some coordinates are redondant and are not ordered.

        >>> Circle(Point2D(0, 0), 5, 10)
        """
        xo = outer
        xi = inner
        y = 0
        erro = 1 - xo
        erri = 1 - xi

        while xo >= y:
            self._x_line(center.x + xi, center.x + xo, center.y + y)
            self._y_line(center.x + y,  center.y + xi, center.y + xo)
            self._x_line(center.x - xo, center.x - xi, center.y + y)
            self._y_line(center.x - y,  center.y + xi, center.y + xo)
            self._x_line(center.x - xo, center.x - xi, center.y - y)
            self._y_line(center.x - y,  center.y - xo, center.y - xi)
            self._x_line(center.x + xi, center.x + xo, center.y - y)
            self._y_line(center.x + y,  center.y - xo, center.y - xi)

            y += 1

            if erro < 0:
                erro += 2 * y + 1
            else:
                xo -= 1
                erro += 2 * (y - xo + 1)

            if y > inner:
                xi = y
            else:
                if erri < 0:
                    erri += 2 * y + 1
                else:
                    xi -= 1
                    erri += 2 * (y - xi + 1)
        return self.coordinates

    def circle_points(self, number: int, radius: int) -> List[Point2D]:
        """Get evenly spaced coordinates of the circle.

        https://stackoverflow.com/questions/8487893/generate-all-the-points-on-the-circumference-of-a-circle

        Args:
            number (int): Number of coordinates to be returned. 
            radius (int, optional): Radius of the circle. Defaults to self.inner.

        Returns:
            list(Point2D): List of evenly spaced 2d-coordinates forming the circle.
        """
        print(self.center.x)
        self.spaced_coordinates = [
            Point2D(cos(2 * pi / number * i) * radius,
                    sin(2 * pi / number * i) * radius)
            for i in range(0, number + 1)
        ]

        for i in range(len(self.spaced_coordinates)):
            self.spaced_coordinates[i] = Point2D(
                self.spaced_coordinates[i].x + self.center.x,
                self.spaced_coordinates[i].y + self.center.y
            ).round()
        return self.spaced_coordinates

    def _x_line(self, x1, x2, y):
        while x1 <= x2:
            self.coordinates.append(Point2D(x1, y))
            x1 += 1

    def _y_line(self, x, y1, y2):
        while y1 <= y2:
            self.coordinates.append(Point2D(x, y1))
            y1 += 1
