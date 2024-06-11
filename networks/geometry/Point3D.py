from typing import Type


class Point3D:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def copy(self):
        return Point3D(self.x, self.y, self.z)

    def coordinates(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return f"Point2D(x: {self.x}, y: {self.y}, z: {self.z})"
