from math import sqrt, atan2


class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> "Position":
        return Position(int(self.x * other), int(self.y * other))

    def __truediv__(self, other: float) -> "Position":
        return Position(int(self.x / other), int(self.y / other))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Position"):
        return self.x == other.x and self.y == other.y

    def get_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    def distance_to(self, other: "Position") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def norm(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def angle_to(self, other: "Position") -> float:
        return atan2(self.y - other.y, other.x - self.x)
