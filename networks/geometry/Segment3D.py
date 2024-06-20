from typing import List
from utils.Enums import LINE_OVERLAP
from networks.geometry.Point3D import Point3D


class Segment3D:
    def __init__(self, start: Point3D, end: Point3D):
        self.start = start
        self.end = end
        self.output_points = []

    def __repr__(self):
        return str(self.output_points)

    def segment(self, overlap: bool = False):
        """Calculate a segment between two points in 3D space. 3d Bresenham algorithm.

        From: https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/

        Args:
            overlap (bool, optional): If False, remove unnecessary points connecting to other points side by side, leaving only a diagonal connection. Defaults to False.

        >>> Segment3D(Point3D(0, 0, 0), Point3D(10, 10, 15))
        """
        start = self.start.copy()
        end = self.end.copy()
        self.output_points.append(start.copy())
        dx = abs(self.end.x - self.start.x)
        dy = abs(self.end.y - self.start.y)
        dz = abs(self.end.z - self.start.z)
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
                self.output_points.append(start.copy())
                if p1 >= 0:
                    start.y += ys
                    if not overlap:
                        if self.output_points[-1].y != start.y:
                            self.output_points.append(start.copy())
                    p1 -= 2 * dx
                if p2 >= 0:
                    start.z += zs
                    if not overlap:
                        if self.output_points[-1].z != start.z:
                            self.output_points.append(start.copy())
                    p2 -= 2 * dx
                p1 += 2 * dy
                p2 += 2 * dz

        # Driving axis is Y-axis
        elif dy >= dx and dy >= dz:
            p1 = 2 * dx - dy
            p2 = 2 * dz - dy
            while start.y != end.y:
                start.y += ys
                self.output_points.append(start.copy())
                if p1 >= 0:
                    start.x += xs
                    if not overlap:
                        if self.output_points[-1].x != start.x:
                            self.output_points.append(start.copy())
                    p1 -= 2 * dy
                if p2 >= 0:
                    start.z += zs
                    if not overlap:
                        if self.output_points[-1].z != start.z:
                            self.output_points.append(start.copy())
                    p2 -= 2 * dy
                p1 += 2 * dx
                p2 += 2 * dz

        # Driving axis is Z-axis
        else:
            p1 = 2 * dy - dz
            p2 = 2 * dx - dz
            while start.z != end.z:
                start.z += zs
                self.output_points.append(start.copy())
                if p1 >= 0:
                    start.y += ys
                    if not overlap:
                        if self.output_points[-1].y != start.y:
                            self.output_points.append(start.copy())
                    p1 -= 2 * dz
                if p2 >= 0:
                    start.x += xs
                    if not overlap:
                        if self.output_points[-1].x != start.x:
                            self.output_points.append(start.copy())
                    p2 -= 2 * dz
                p1 += 2 * dy
                p2 += 2 * dx
        return self.output_points

    def middle_point(self):
        return (np.round((self.start.x + self.end.x) / 2.0).astype(int),
                np.round((self.start.y + self.end.y) / 2.0).astype(int),
                np.round((self.start.z + self.end.z) / 2.0).astype(int),
                )
