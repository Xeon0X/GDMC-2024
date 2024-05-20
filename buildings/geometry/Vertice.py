from utils.Enums import DIRECTION
from buildings.geometry.Point import Point
from buildings.geometry.Rectangle import Rectangle

class Vertice(Rectangle):
    def __init__(self, point1 : Point, point2 : Point, facing : DIRECTION):
        Rectangle.__init__(self, point1, point2)
        self.facing = facing
        
    def get_neighbors(self):
        match self.facing:
            case DIRECTION.NORTH | DIRECTION.SOUTH:
                return [Point(x = self.point1.x - 1, z = self.point1.z), 
                        Point(x = self.point2.x + 1, z = self.point2.z)]
            case DIRECTION.EAST | DIRECTION.WEST:
                return [Point(x = self.point1.x, z = self.point1.z - 1), 
                        Point(x = self.point2.x, z = self.point2.z + 1)]
                
    def get_len(self):
        return self.point2.x - self.point1.x + self.point2.z - self.point1.z + 1
        