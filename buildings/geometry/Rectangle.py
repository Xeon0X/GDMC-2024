from gdpc import Editor, Block, geometry
from buildings.geometry.Point import Point

class Rectangle:
    def __init__(self, point1 : Point, point2 : Point):
        self.point1 = point1
        self.point2 = point2
        
    def get_position(self):
        return (self.point1.position, self.point2.position)
    
    def get_height(self):
        return self.point2.y - self.point1.y + 1
    
    def fill(self,editor : Editor, material : str, y : int = None, xpadding : int = 0, zpadding : int = 0):
        if self.point2.x - self.point1.x < 2*xpadding: xpadding = 0
        if self.point2.z - self.point1.z < 2*zpadding: zpadding = 0
        if y is None: y = self.point2.y
        
        geometry.placeCuboid(editor, (self.point1.x+xpadding, 0, self.point1.z+zpadding), (self.point2.x-xpadding, y, self.point2.z-zpadding), Block(material))
