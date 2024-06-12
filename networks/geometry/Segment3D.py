from typing import List
from networks.geometry.Enums import LINE_OVERLAP
from networks.geometry.Point3D import Point3D


class Segment3D:
    def __init__(self, start: Point3D, end: Point3D, overlap: bool = True):
        self.start = start
        self.end = end
        self.coordinates = []
        self.overlap = overlap

        self._compute_segment(self.start, self.end, self.overlap)

    def __repr__(self):
        return str(self.coordinates)

    def _compute_segment(self, start: Point3D, end: Point3D, overlap: bool = False):
        """Calculate a segment between two points in 3D space. 3d Bresenham algorithm.

        From: https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/

        Args:
            start (Point3D): First coordinates.
            end (Point3D): Second coordinates.
            overlap (bool, optional): If False, remove unnecessary coordinates connecting to other coordinates side by side, leaving only a diagonal connection. Defaults to False.

        >>> Segment3D(Point3D(0, 0, 0), Point3D(10, 10, 15))
        """
        self.coordinates.append(start.copy())
        dx = abs(end.x - start.x)
        dy = abs(end.y - start.y)
        dz = abs(end.z - start.z)
        if end.x > start.x:
            xs = 1
        else:
            xs = -1
        if end.y > start.y:
            ys = 1
        else:
            ys = -1
        if end.z > start.z:
            zs = 1
        else:
            zs = -1

        # Driving axis is X-axis
        if dx >= dy and dx >= dz:
            p1 = 2 * dy - dx
            p2 = 2 * dz - dx
            while start.x != end.x:
                start.x += xs
                self.coordinates.append(start.copy())
                if p1 >= 0:
                    start.y += ys
                    if not overlap:
                        if self.coordinates[-1].y != start.y:
                            self.coordinates.append(start.copy())
                    p1 -= 2 * dx
                if p2 >= 0:
                    start.z += zs
                    if not overlap:
                        if self.coordinates[-1].z != start.z:
                            self.coordinates.append(start.copy())
                    p2 -= 2 * dx
                p1 += 2 * dy
                p2 += 2 * dz

        # Driving axis is Y-axis
        elif dy >= dx and dy >= dz:
            p1 = 2 * dx - dy
            p2 = 2 * dz - dy
            while start.y != end.y:
                start.y += ys
                self.coordinates.append(start.copy())
                if p1 >= 0:
                    start.x += xs
                    if not overlap:
                        if self.coordinates[-1].x != start.x:
                            self.coordinates.append(start.copy())
                    p1 -= 2 * dy
                if p2 >= 0:
                    start.z += zs
                    if not overlap:
                        if self.coordinates[-1].z != start.z:
                            self.coordinates.append(start.copy())
                    p2 -= 2 * dy
                p1 += 2 * dx
                p2 += 2 * dz

        # Driving axis is Z-axis
        else:
            p1 = 2 * dy - dz
            p2 = 2 * dx - dz
            while start.z != end.z:
                start.z += zs
                self.coordinates.append(start.copy())
                if p1 >= 0:
                    start.y += ys
                    if not overlap:
                        if self.coordinates[-1].y != start.y:
                            self.coordinates.append(start.copy())
                    p1 -= 2 * dz
                if p2 >= 0:
                    start.x += xs
                    if not overlap:
                        if self.coordinates[-1].x != start.x:
                            self.coordinates.append(start.copy())
                    p2 -= 2 * dz
                p1 += 2 * dy
                p2 += 2 * dx
