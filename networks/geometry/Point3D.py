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

    def distance(self, point: "Point3D"):
        return sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2)

    def round(self, ndigits: int = None) -> "Point3D":
        self.x = round(self.x, ndigits)
        self.y = round(self.y, ndigits)
        self.z = round(self.z, ndigits)
        self.coordinate = (self.x, self.y, self.z)
        return self
