import random as rd
from gdpc import Editor, Block, geometry
from utils.Enums import DIRECTION,COLLUMN_STYLE
from buildings.geometry.Vertice import Vertice
from buildings.Facade import Facade

class Entrance:
    def __init__(self, rdata, vertices : list[Vertice], direction : DIRECTION, collumn_style : COLLUMN_STYLE):
        self.vertices = vertices
        self.direction = direction
        self.rdata = rdata
        self.collumn_style = collumn_style
        self.is_centered = self.is_centered()
        self.door_vertice, self.facade = self.get_door_and_facade()
        
    def build(self, editor : Editor, materials : list[str]):
        self.facade.build(editor, materials)
        self.door_vertice.fill(editor, materials[0])
        
    def is_centered(self) -> bool:
        return rd.random() <= self.rdata["entrance"]["centered"]
    
    def get_door_and_facade(self) -> tuple[Vertice, Facade]:
        oriented_vertices = self.get_oriented_vertices()
        facade_vertices = self.vertices.copy()
        door_vertice = None
        
        if self.is_centered:
            oriented_vertices.sort(key = lambda v: v.point1.x if self.direction.value % 2 == 0 else v.point1.z) # if direction is north or south, sort by x, else sort by z
            mid = len(oriented_vertices) // 2
            ver1, ver2 = oriented_vertices[mid], oriented_vertices[-mid-1]
            if ver1.point1.position == ver2.point1.position:
                door_vertice = ver1
            else : 
                door_vertice =  Vertice(ver2.point1, ver1.point2)
                facade_vertices.remove(ver2)
            facade_vertices.remove(ver1)
            
        else: 
            door_vertice = rd.choice(oriented_vertices)
            facade_vertices.remove(door_vertice)
        
        facade = Facade(self.rdata["facade"], facade_vertices, self.collumn_style)
        return(door_vertice, facade)
        
    def get_oriented_vertices(self) -> list[Vertice]:
        # get the most off-centered vertices that are in the same direction as self.direction
        same_direction_vertices = sorted([v for v in self.vertices if v.facing == self.direction],
                                         key = lambda v: v.point1.z if self.direction.value % 2 == 0 else v.point1.x, # if direction is north or south, sort by x, else sort by z
                                         reverse = self.direction == DIRECTION.NORTH or self.direction == DIRECTION.WEST) # if direction is north or west, sort in reverse
        extremum = same_direction_vertices[0]
        return [v for v in same_direction_vertices if 
                (v.point1.x == extremum.point1.x and self.direction.value % 2 == 0) or 
                (v.point1.z == extremum.point1.z and self.direction.value % 2 == 1)]
        