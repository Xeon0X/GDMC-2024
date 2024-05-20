import random as rd
from utils.Enums import COLLUMN_STYLE
from gdpc import Editor, Transform
from buildings.geometry.Vertice import Vertice
from buildings.elements.Window import Window

class Facade:
    def __init__(self, rdata, vertices : list[Vertice], height : int, length : int, is_inner_or_outer : COLLUMN_STYLE):
        self.rdata = rdata
        self.vertices = vertices
        self.is_inner_or_outer = is_inner_or_outer
        self.height = height
        self.length = length
        self.padding = 0
        self.window =  self.get_window()
        self.has_balcony = self.has_balcony()
        self.has_inter_floor = self.has_inter_floor()
        
    def build(self, editor : Editor, materials : list[str]):            
        for vertice in self.vertices:
            vertice.fill(editor, materials[0], self.height, xpadding = self.padding, zpadding = self.padding)
            with editor.pushTransform(Transform(vertice.point1.position,rotation = vertice.facing.value)):
                self.window.build(editor, vertice.get_len(), self.height, materials)
        
    def get_window(self) -> Window:
        if self.is_inner_or_outer == COLLUMN_STYLE.OUTER or self.is_inner_or_outer == COLLUMN_STYLE.BOTH:
            self.padding = 1
        
        max_width = self.length-2*self.padding
        max_height = min(self.height, self.rdata["windows"]["size"]["max_height"])
            
        return Window(self.rdata["windows"] ,max_width, max_height)
    
    def has_balcony(self) -> bool:
        pass
    
    def has_inter_floor(self) -> bool:
        pass
    