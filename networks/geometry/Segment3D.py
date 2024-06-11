from typing import Type
from networks.geometry.Enums import LINE_OVERLAP
from networks.geometry.Point3D import Point3D


class Segment3D:
    def __init__(start: Type[Point3D], end: Type[Point3D]):
        self.start = start
        self.end = end
        self.coordinates = []

    def compute_segment(start: Type[Point3D], end: Type[Point3D], overlap=True):
        """Calculate a segment between two points in 3D space. 3d Bresenham algorithm.

        From: https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/

        Args:
            start (Type[Point3D]): First coordinates.
            end (Type[Point3D]): Second coordinates.
            overlap (bool, optional): If true, remove unnecessary coordinates connecting to other coordinates side by side, leaving only a diagonal connection. Defaults to True.
        """
        self.coordinates.append(start)
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
                self.coordinates.append(start)
                if p1 >= 0:
                    start.y += ys
                    if not overlap:
                        if self.coordinates[-1].y != start.y:
                            self.coordinates.append(start)
                    p1 -= 2 * dx
                if p2 >= 0:
                    start.z += zs
                    if not overlap:
                        if self.coordinates[-1].z != start.z:
                            self.coordinates.append(start)
                    p2 -= 2 * dx
                p1 += 2 * dy
                p2 += 2 * dz

        # Driving axis is Y-axis
        elif dy >= dx and dy >= dz:
            p1 = 2 * dx - dy
            p2 = 2 * dz - dy
            while start.y != end.y:
                start.y += ys
                self.coordinates.append(start)
                if p1 >= 0:
                    start.x += xs
                    if not overlap:
                        if self.coordinates[-1].x != start.x:
                            self.coordinates.append(start)
                    p1 -= 2 * dy
                if p2 >= 0:
                    start.z += zs
                    if not overlap:
                        if self.coordinates[-1].z != start.z:
                            self.coordinates.append(start)
                    p2 -= 2 * dy
                p1 += 2 * dx
                p2 += 2 * dz

        # Driving axis is Z-axis
        else:
            p1 = 2 * dy - dz
            p2 = 2 * dx - dz
            while start.z != end.z:
                start.z += zs
                self.coordinates.append(start)
                if p1 >= 0:
                    start.y += ys
                    if not overlap:
                        if self.coordinates[-1].y != start.y:
                            self.coordinates.append(start)
                    p1 -= 2 * dz
                if p2 >= 0:
                    start.x += xs
                    if not overlap:
                        if self.coordinates[-1].x != start.x:
                            self.coordinates.append(start)
                    p2 -= 2 * dz
                p1 += 2 * dy
                p2 += 2 * dx
