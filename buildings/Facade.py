import random as rd
from utils.Enums import COLLUMN_STYLE, DIRECTION
from gdpc import Editor
from buildings.geometry.Vertice import Vertice
from buildings.geometry.Rectangle import Rectangle
from buildings.elements.Window import Window

class Facade:
    def __init__(self, rdata, vertices : list[Vertice], height : int, lenght : int, is_inner_or_outer : COLLUMN_STYLE):
        self.rdata = rdata
        self.vertices = vertices
        self.is_inner_or_outer = is_inner_or_outer
        self.height = height
        self.lenght = lenght
        self.window_size = self.get_window_size()
        self.window =  self.get_window()
        self.has_balcony = self.has_balcony()
        self.has_inter_floor = self.has_inter_floor()
        
    def build(self, editor : Editor, materials : list[str], y : int):
        padding = 0
        if self.is_inner_or_outer == COLLUMN_STYLE.OUTER or self.is_inner_or_outer == COLLUMN_STYLE.BOTH:
            padding = 1
            
        for vertice in self.vertices:
            xpadding, zpadding = 0, 0
            if vertice.facing == DIRECTION.NORTH or vertice.facing == DIRECTION.SOUTH:
                xpadding = padding
            else: zpadding = padding
            
            vertice.fill(editor, materials[0], y, y + self.height, xpadding = xpadding, zpadding = zpadding)
            self.window.build(editor, vertice, self.height, y, materials)
        
    def get_window_size(self) -> tuple[int,int]:
        max_width = self.lenght
        max_height = min(self.height, self.rdata["windows"]["size"]["max_height"])
        if self.is_inner_or_outer == COLLUMN_STYLE.OUTER or self.is_inner_or_outer == COLLUMN_STYLE.BOTH:
            max_width -= 2
         
        return (
                rd.randint(self.rdata["windows"]["size"]["min_width"],max_width),
                rd.randint(self.rdata["windows"]["size"]["min_height"],max_height)
        )
        
    def has_balcony(self) -> bool:
        pass
    
    def has_inter_floor(self) -> bool:
        pass
    
    def get_window(self) -> Window:
        return Window(self.rdata["windows"] ,self.window_size)