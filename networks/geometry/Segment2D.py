from typing import Type
from networks.geometry.Enums import LINE_OVERLAP, LINE_THICKNESS_MODE
from networks.geometry.Point2D import Point2D


class Segment2D:
    def __init__(start: Type[Point2D], end: Type[Point2D]):
        self.start = start
        self.end = end
        self.coordinates = []

    def draw_line_overlap(start: Type[Point2D], end: Type[Point2D], overlap: Type[LINE_OVERLAP]):
        """Modified Bresenham draw (line) with optional overlap.

        From https://github.com/ArminJo/Arduino-BlueDisplay/blob/master/src/LocalGUI/ThickLine.hpp

        Args:
            start (Type[Point2D]): Start point of the segment.
            end (Type[Point2D]): End point of the segment.
            overlap (Type[LINE_OVERLAP]): Overlap draws additional pixel when changing minor direction. For standard bresenham overlap, choose LINE_OVERLAP_NONE. Can also be LINE_OVERLAP_MAJOR or LINE_OVERLAP_MINOR.
        """
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

        self.coordinates.append(start)

        if (delta_x > delta_y):
            error = delta_2y - delta_x
            while (start.x != end.x):
                start.x += step_x
                if (error >= 0):
                    if (overlap == LINE_OVERLAP.MAJOR):
                        self.coordinates.append(start)

                    start.y += step_y
                    if (overlap == LINE_OVERLAP.MINOR):
                        self.coordinates.append(
                            Point2D(start.x - step_x, start.y))
                    error -= delta_2x
                error += delta_2y
                self.coordinates.append(start)
        else:
            error = delta_2x - delta_y
            while (start.y != end.y):
                start.y += step_y
                if (error >= 0):
                    if (overlap == LINE_OVERLAP.MAJOR):
                        self.coordinates.append(start)

                    start.x += step_x
                    if (overlap == LINE_OVERLAP.MINOR):
                        self.coordinates.append(
                            Point2D(start.x, start.y - step_y))
                    error -= delta_2y
                error += delta_2x
                self.coordinates.append(start)

    def draw_thick_line(start: Type[Point2D], end: Type[Point2D], thickness: int, thickness_mode: Type[LINE_THICKNESS_MODE]):
        """Bresenham with thickness.

        From https://github.com/ArminJo/Arduino-BlueDisplay/blob/master/src/LocalGUI/ThickLine.hpp
        Probably inspired from Murphy's Modified Bresenham algorithm : http://zoo.co.uk/murphy/thickline/index.html

        Args:
            start (Type[Point2D]): Start point of the segment.
            end (Type[Point2D]): End point of the segment.
            thickness (int): Total width of the surface. Placement relative to the original segment depends on thickness_mode.
            thickness_mode (Type[LINE_THICKNESS_MODE]): Can be one of LINE_THICKNESS_MIDDLE, LINE_THICKNESS_DRAW_CLOCKWISE, LINE_THICKNESS_DRAW_COUNTERCLOCKWISE.
        """
        delta_y = end.x - start.x
        delta_x = end.y - start.y

        swap = True
        if delta_x < 0:
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
        if (thickness_mode == LineThicknessMode.DRAW_COUNTERCLOCKWISE):
            draw_start_adjust_count = thickness - 1
        elif (thickness_mode == LineThicknessMode.DRAW_CLOCKWISE):
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

            draw_line_overlap(start, end, LINE_OVERLAP.NONE)

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

                draw_line_overlap(start, end, overlap)

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

            draw_line_overlap(start, end, LINE_OVERLAP.NONE)

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

                draw_line_overlap(start, end, overlap)
