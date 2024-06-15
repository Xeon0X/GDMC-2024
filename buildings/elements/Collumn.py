from buildings.geometry.Rectangle import Rectangle
from buildings.geometry.Point import Point

class Collumn(Rectangle):
    def __init__(self, point1 : Point, point2 : Point, is_outer : bool = False) :
        Rectangle.__init__(self, point1, point2)
        self.is_outer = is_outer
        
    def set_is_outer(self, is_outer : bool):
        self.is_outer = is_outer
        
    def __repr__(self):
        return super().__repr__() + f"\nIs outer : {self.is_outer}\n\n"
        