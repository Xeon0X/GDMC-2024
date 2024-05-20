from enum import Enum

class DIRECTION(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3
    
class COLLUMN_STYLE(Enum):
    NONE = 0
    INNER = 1
    OUTER = 2
    BOTH = 3