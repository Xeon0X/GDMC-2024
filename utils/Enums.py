from enum import Enum

class DIRECTION(Enum):
    WEST = 0
    EAST = 1
    NORTH = 2
    SOUTH = 3
    
class COLLUMN_STYLE(Enum):
    NONE = 0
    INNER = 1
    OUTER = 2
    BOTH = 3