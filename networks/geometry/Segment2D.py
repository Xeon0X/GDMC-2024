from typing import List, Union

import numpy as np

from utils.Enums import LINE_OVERLAP, LINE_THICKNESS_MODE
from networks.geometry.Point2D import Point2D


class Segment2D:
    def __init__(self, start: Point2D, end: Point2D):
        self.start = start
        self.end = end
        self.points: List[Point2D] = []
        self.points_thick: List[Point2D] = []

        self.points_thick_by_line: List[List[Point2D]] = []
        self.gaps: List[List[Point2D]] = []

        self.thickness = None

    def __repr__(self):
        return str(f"Segment2D(start: {self.start}, end: {self.end}, points: {self.points})")

    def segment(self, start: Point2D = None, end: Point2D = None, overlap: LINE_OVERLAP = LINE_OVERLAP.NONE, _is_computing_thickness: int = 0) -> Union[List[Point2D], None]:
        """Modified Bresenham draw (line) with optional overlap.

        From: https://github.com/ArminJo/Arduino-BlueDisplay/blob/master/src/LocalGUI/ThickLine.hpp

        Args:
            start (Point2D): Start point of the segment.
            end (Point2D): End point of the segment.
            overlap (LINE_OVERLAP): Overlap draws additional pixel when changing minor direction. For standard bresenham overlap, choose LINE_OVERLAP_NONE. Can also be LINE_OVERLAP_MAJOR or LINE_OVERLAP_MINOR.
            _is_computing_thickness (bool, optionnal): Used by segment_thick. Don't touch.

        >>> Segment2D(Point2D(0, 0), Point2D(10, 15))
        """

        if start is None or end is None:
            start = self.start.copy()
            end = self.end.copy()
        else:
            start = start.copy()
            end = end.copy()

        # Direction
        delta_x = end.x - start.x
        delta_y = end.y - start.y

        if (delta_x < 0):
            delta_x = -delta_x
            step_x = -1
        else:
            step_x = +1

        if (delta_y < 0):
            delta_y = -delta_y
            step_y = -1
        else:
            step_y = +1

        delta_2x = 2*delta_x
        delta_2y = 2*delta_y

        self._add_points(start, _is_computing_thickness, LINE_OVERLAP.NONE)

        if (delta_x > delta_y):
            error = delta_2y - delta_x
            while (start.x != end.x):
                start.x += step_x
                if (error >= 0):
                    if (overlap == LINE_OVERLAP.MAJOR):
                        self._add_points(
                            start, _is_computing_thickness, overlap)

                    start.y += step_y
                    if (overlap == LINE_OVERLAP.MINOR):
                        self._add_points(
                            Point2D(start.copy().x - step_x, start.copy().y), _is_computing_thickness, overlap)
                    error -= delta_2x
                error += delta_2y
                self._add_points(
                    start, _is_computing_thickness, LINE_OVERLAP.NONE)
        else:
            error = delta_2x - delta_y
            while (start.y != end.y):
                start.y += step_y
                if (error >= 0):
                    if (overlap == LINE_OVERLAP.MAJOR):
                        self._add_points(
                            start, _is_computing_thickness, overlap)

                    start.x += step_x
                    if (overlap == LINE_OVERLAP.MINOR):
                        self._add_points(
                            Point2D(start.copy().x, start.copy().y - step_y), _is_computing_thickness, overlap)
                    error -= delta_2y
                error += delta_2x
                self._add_points(
                    start, _is_computing_thickness, LINE_OVERLAP.NONE)

        if not _is_computing_thickness:
            return self.points
        return None

    def segment_thick(self, thickness: int, thickness_mode: LINE_THICKNESS_MODE) -> List[Point2D]:
        """Bresenham with thickness.

        From: https://github.com/ArminJo/Arduino-BlueDisplay/blob/master/src/LocalGUI/ThickLine.hpp
        Murphy's Modified Bresenham algorithm : http://zoo.co.uk/murphy/thickline/index.html

        Args:
            start (Point2D): Start point of the segment.
            end (Point2D): End point of the segment.
            thickness (int): Total width of the surface. Placement relative to the original segment depends on thickness_mode.
            thickness_mode (LINE_THICKNESS_MODE): Can be one of LINE_THICKNESS_MIDDLE, LINE_THICKNESS_DRAW_CLOCKWISE, LINE_THICKNESS_DRAW_COUNTERCLOCKWISE.

        >>> self.compute_thick_segment(self.start, self.end, self.thickness, self.thickness_mode)
        """
        self.points_thick_by_line = [[] for _ in range(thickness)]
        self.gaps = [[] for _ in range(thickness)]

        start = self.start.copy()
        end = self.end.copy()

        delta_y = end.x - start.x
        delta_x = end.y - start.y

        swap = True
        if (delta_x < 0):
            delta_x = -delta_x
            step_x = -1
            swap = not swap
        else:
            step_x = +1

        if (delta_y < 0):
            delta_y = -delta_y
            step_y = -1
            swap = not swap
        else:
            step_y = +1

        delta_2x = 2 * delta_x
        delta_2y = 2 * delta_y

        draw_start_adjust_count = int(thickness / 2)
        if (thickness_mode == LINE_THICKNESS_MODE.DRAW_COUNTERCLOCKWISE):
            draw_start_adjust_count = thickness - 1
        elif (thickness_mode == LINE_THICKNESS_MODE.DRAW_CLOCKWISE):
            draw_start_adjust_count = 0

        if (delta_x >= delta_y):
            if swap:
                draw_start_adjust_count = (
                    thickness - 1) - draw_start_adjust_count
                step_y = -step_y
            else:
                step_x = -step_x

            error = delta_2y - delta_x
            for i in range(draw_start_adjust_count, 0, -1):

                start.x -= step_x
                end.x -= step_x
                if error >= 0:
                    start.y -= step_y
                    end.y -= step_y
                    error -= delta_2x
                error += delta_2x

            if not swap:
                self.segment(
                    start, end, overlap=LINE_OVERLAP.NONE, _is_computing_thickness=0)
            else:
                self.segment(
                    start, end, overlap=LINE_OVERLAP.NONE, _is_computing_thickness=thickness-1)

            error = delta_2x - delta_x
            for i in range(thickness, 1, -1):
                start.x += step_x
                end.x += step_x
                overlap = LINE_OVERLAP.NONE
                if (error >= 0):
                    start.y += step_y
                    end.y += step_y
                    error -= delta_2x
                    overlap = LINE_OVERLAP.MAJOR
                error += delta_2y

                if not swap:
                    self.segment(
                        start, end, overlap=overlap, _is_computing_thickness=(thickness-i+1))
                else:
                    self.segment(
                        start, end, overlap=overlap, _is_computing_thickness=(i-2))

        else:
            if swap:
                step_x = -step_x
            else:
                draw_start_adjust_count = (
                    thickness - 1) - draw_start_adjust_count
                step_y = -step_y

            error = delta_2x - delta_y
            for i in range(draw_start_adjust_count, 0, -1):
                start.y -= step_y
                end.y -= step_y
                if (error >= 0):
                    start.x -= step_x
                    end.x -= step_x
                    error -= delta_2y
                error += delta_2x

            if swap:
                self.segment(
                    start, end, overlap=LINE_OVERLAP.NONE, _is_computing_thickness=0)
            else:
                self.segment(
                    start, end, overlap=LINE_OVERLAP.NONE, _is_computing_thickness=thickness-1)

            error = delta_2x - delta_y
            for i in range(thickness, 1, -1):
                start.y += step_y
                end.y += step_y
                overlap = LINE_OVERLAP.NONE
                if (error >= 0):
                    start.x += step_x
                    end.x += step_x
                    error -= delta_2y
                    overlap = LINE_OVERLAP.MAJOR
                error += delta_2x

                if swap:
                    self.segment(
                        start, end, overlap=overlap, _is_computing_thickness=(thickness-i+1))
                else:
                    self.segment(
                        start, end, overlap=overlap, _is_computing_thickness=(i-2))

        reel_distance = self.points_thick_by_line[0][0].distance(
            self.points_thick_by_line[-1][0])

        return self.points_thick

    def perpendicular(self, distance: int) -> List[Point2D]:
        """Compute perpendicular points from both side of the segment placed at start level.

        Args:
            distance (int): Distance bewteen the start point and the perpendicular.

        Returns:
            List[Point2D]: Two points. First one positioned on the counterclockwise side of the segment, oriented from start to end (meaning left).

        >>> Segment2D(Point2D(0, 0), Point2D(10, 10)).perpendicular(10)
        (Point2D(x: -4, y: 4), Point2D(x: 4, y: -4))
        """
        delta = self.start.distance(self.end)
        dx = (self.start.x - self.end.x) / delta
        dy = (self.start.y - self.end.y) / delta

        x3 = self.start.x + (distance / 2) * dy
        y3 = self.start.y - (distance / 2) * dx
        x4 = self.start.x - (distance / 2) * dy
        y4 = self.start.y + (distance / 2) * dx
        return Point2D(x3, y3).round(), Point2D(x4, y4).round()

    def middle_point(self):
        return (np.round((self.start.x + self.end.x) / 2.0).astype(int),
                np.round((self.start.y + self.end.y) / 2.0).astype(int),
                )

    def _add_points(self, points, is_computing_thickness, overlap):
        if is_computing_thickness >= 0:
            self.points_thick.append(points.copy())
            if overlap == LINE_OVERLAP.NONE:
                self.points_thick_by_line[is_computing_thickness].append(
                    (points.copy()))
            else:
                self.gaps[is_computing_thickness].append(
                    (points.copy()))
        else:
            self.points.append(points.copy())
