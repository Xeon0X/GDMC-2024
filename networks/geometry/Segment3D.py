from typing import Type
from networks.geometry.Enums import LINE_OVERLAP
from networks.geometry.Point3D import Point3D


class Segment3D:
    def __init__(start: Type[Point3D], end: Type[Point3D]):
        self.start = start
        self.end = end
        self.coordinates = []
