from enum import Enum


class DIRECTION(Enum):
    WEST = 0
    EAST = 1
    NORTH = 2
    SOUTH = 3


class COLLUMN_STYLE(Enum):
    INNER = 1
    OUTER = 2
    BOTH = 3


class LINE_OVERLAP(Enum):
    NONE = 0
    MAJOR = 1
    MINOR = 2


class LINE_THICKNESS_MODE(Enum):
    MIDDLE = 0
    DRAW_COUNTERCLOCKWISE = 1
    DRAW_CLOCKWISE = 2


class ROTATION(Enum):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1
