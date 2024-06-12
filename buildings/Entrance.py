import random as rd
from utils.Enums import DIRECTION
from buildings.geometry.Vertice import Vertice

class Entrance:
    def __init__(self, rdata, vertices : list[Vertice], direction : DIRECTION):
        self.vertices = vertices
        self.direction = direction
        self.rdata = rdata
        self.is_centered = self.is_centered()
        self.door_vertices = self.get_door_vertices()
        
    def is_centered(self) -> bool:
        return rd.random() <= self.rdata["centered"]
    
    def get_door_vertices(self) -> Vertice:
        oriented_vertices = self.get_oriented_vertices()
        
    def get_oriented_vertices(self) -> list[Vertice]:
        # get the most off-centered vertices that are in the same direction as self.direction
        same_direction_vertices = sorted([v for v in self.vertices if v.direction == self.direction],
                                         lambda v: v.point1.z if self.direction.value % 2 == 0 else v.point1.x, # if direction is north or south, sort by x, else sort by z
                                         reverse = self.direction == DIRECTION.NORTH or self.direction == DIRECTION.WEST) # if direction is north or west, sort in reverse
        extremum = same_direction_vertices[0]
        return [v for v in same_direction_vertices if 
                (v.poin1.x == extremum.point1.x and self.direction.value % 2 == 0) or 
                (v.point1.z == extremum.point1.z and self.direction.value % 2 == 1)]
        