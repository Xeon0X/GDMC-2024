from math import cos, pi, sin
from typing import List, Dict

import numpy as np

from networks.geometry.Point2D import Point2D


class Circle:
    def __init__(self, center: Point2D):
        self.center = center

        self.radius = None
        self.points: List[Point2D] = []

        self.inner = None
        self.outer = None
        self.points_thick: List[Point2D] = []

        self.points_thick_by_line: List[List[Point2D]] = []
        self.gaps: List[Point2D] = []

        self.spaced_radius = None
        self.spaced_points: List[Point2D] = []

    def __repr__(self):
        return f"Circle(center: {self.center}, radius: {self.radius}, spaced_radius: {self.spaced_radius}, inner: {self.inner}, outer: {self.outer})"

    def circle(self, radius: int) -> List[Point2D]:
        self.points = []
        self.radius = radius
        center = self.center.copy()

        x = -radius
        y = 0
        error = 2-2*radius
        while (True):
            self.points.append(Point2D(center.x-x, center.y+y))
            self.points.append(Point2D(center.x-y, center.y-x))
            self.points.append(Point2D(center.x+x, center.y-y))
            self.points.append(Point2D(center.x+y, center.y+x))
            r = error
            if (r <= y):
                y += 1
                error += y*2+1
            if (r > x or error > y):
                x += 1
                error += x*2+1
            if (x < 0):
                continue
            else:
                break
        return self.points

    def circle_thick_by_line(self, inner: int, outter: int) -> List[List[Point2D]]:
        width = outter - inner
        print(f"[Circle gaps] {inner}/{outter}, {self.center}")
        self.circle_thick_by_line = [[] for _ in range(width)]
        for i in range(width):
            self.circle_thick_by_line[i] = self.circle(inner + i)
            if i > 0:
                self.gaps.append(Circle._remove_gaps(
                    self.circle_thick_by_line[i], self.circle_thick_by_line[i-1]))
        return self.circle_thick_by_line, self.gaps

    @staticmethod
    def _remove_gaps(outter_line: List[Point2D], inner_line: List[Point2D]) -> List[Point2D]:
        gaps = []
        for i in range(len(outter_line)):
            nearest_index = outter_line[i].nearest(
                inner_line, True)[0]
            potential_neighbors = [inner_line[(nearest_index+j) % len(inner_line)]
                                   for j in range(-10, 10, 1)]
            # print(f"[Circle gaps] {i}/{len(outter_line)}")
            if Circle._count_neighbors(outter_line[i], potential_neighbors) == 0:
                if Circle._count_neighbors(Point2D(outter_line[i].x-1, outter_line[i].y), potential_neighbors) > 1:
                    if Point2D(outter_line[i].x-1, outter_line[i].y) not in outter_line:
                        gaps.append(
                            Point2D(outter_line[i].x-1, outter_line[i].y))
                if Circle._count_neighbors(Point2D(outter_line[i].x+1, outter_line[i].y), potential_neighbors) > 1:
                    if Point2D(outter_line[i].x+1, outter_line[i].y) not in outter_line:
                        gaps.append(
                            Point2D(outter_line[i].x+1, outter_line[i].y))
                if Circle._count_neighbors(Point2D(outter_line[i].x, outter_line[i].y-1), potential_neighbors) > 1:
                    if Point2D(outter_line[i].x, outter_line[i].y-1) not in outter_line:
                        gaps.append(
                            Point2D(outter_line[i].x, outter_line[i].y-1))
                if Circle._count_neighbors(Point2D(outter_line[i].x, outter_line[i].y+1), potential_neighbors) > 1:
                    if Point2D(outter_line[i].x, outter_line[i].y+1) not in outter_line:
                        gaps.append(
                            Point2D(outter_line[i].x, outter_line[i].y+1))
        return gaps

    @ staticmethod
    def _count_neighbors(point: Point2D, line: List[Point2D]) -> int:
        neighbors = 0
        for i in range(len(line)):
            if point.x == line[i].x:
                if point.y == line[i].y:
                    return 0
                if point.y-1 == line[i].y:
                    neighbors += 1
                if point.y+1 == line[i].y:
                    neighbors += 1
            if point.y == line[i].y:
                if point.x-1 == line[i].x:
                    neighbors += 1
                if point.x+1 == line[i].x:
                    neighbors += 1
        return neighbors

    def circle_thick(self, inner: int, outer: int) -> List[Point2D]:
        """Compute discrete value of a 2d-circle with thickness.

        From: https://stackoverflow.com/questions/27755514/circle-with-thickness-drawing-algorithm

        Args:
            inner (int): The minimum radius at which the disc is filled (included).
            outer (int): The maximum radius where disc filling stops (included).

        Returns:
            list(Point2D): List of 2d-coordinates composing the surface. Note that some coordinates are redondant and are not ordered.

        >>> Circle(Point2D(0, 0), 5, 10)
        """

        self.inner = inner
        self.outer = outer
        center = self.center.copy()

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
        return self.points_thick

    def circle_spaced(self, number: int, radius: int) -> List[Point2D]:
        """Get evenly spaced coordinates of the circle.

        From: https://stackoverflow.com/questions/8487893/generate-all-the-points-on-the-circumference-of-a-circle

        Args:
            number (int): Number of coordinates to be returned.
            radius (int): Radius of the circle.

        Returns:
            list(Point2D): List of evenly spaced 2d-coordinates forming the circle.
        """
        self.spaced_radius = radius
        center = self.center

        self.spaced_points = [
            Point2D(round(cos(2 * pi / number * i) * radius),
                    round(sin(2 * pi / number * i) * radius))
            for i in range(0, number + 1)
        ]

        for i in range(len(self.spaced_points)):
            current_point = Point2D(
                self.spaced_points[i].x + center.x,
                self.spaced_points[i].y + center.y
            ).round()
            self.spaced_points[i] = current_point
        return self.spaced_points

    def _x_line(self, x1, x2, y):
        while x1 <= x2:
            self.points_thick.append(Point2D(x1, y))
            x1 += 1

    def _y_line(self, x, y1, y2):
        while y1 <= y2:
            self.points_thick.append(Point2D(x, y1))
            y1 += 1
