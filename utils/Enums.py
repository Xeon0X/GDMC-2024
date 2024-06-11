from enum import Enum

class DIRECTION(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    
class COLLUMN_STYLE(Enum):
    NONE = 0
    INNER = 1
    OUTER = 2
    BOTH = 3
    
class WINDOW_BORDER_RADIUS(Enum):
    NONE = 0
    TOP = 1
    TOP_AND_BOTTOM = 2  
    
class BALCONY_BORDER_RADIUS(Enum):
    NONE = 0
    MEDIUM = 1
    FULL = 2
    
class INTER_FLOOR_BORDER(Enum):
    NONE = 0
    SLAB = 1
    STAIRS = 2