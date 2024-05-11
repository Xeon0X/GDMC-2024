from gdpc import Editor, Block, geometry
from buildings.geometry.Point import Point

class Rectangle:
    def __init__(self, point1 : Point, point2 : Point):
        self.point1 = point1
        self.point2 = point2
        
    def get_position(self):
        return (self.point1.position, self.point2.position)
    
    def fill(self,editor : Editor, material : str, y : int, y2 : int = None):
        if y2 == None: y2 = y
        geometry.placeCuboid(editor, (self.point1.x, y, self.point1.z), (self.point2.x, y2, self.point2.z), Block(material))
