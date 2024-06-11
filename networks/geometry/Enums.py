from enum import Enum


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
