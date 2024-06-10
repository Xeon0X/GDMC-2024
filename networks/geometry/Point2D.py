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
