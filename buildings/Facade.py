import random as rd
from utils.Enums import COLLUMN_STYLE
from gdpc import Editor, Block, geometry, Transform
from buildings.geometry.Vertice import Vertice
from buildings.elements.Window import Window
from buildings.elements.Balcony import Balcony

class Facade:
    def __init__(self, rdata, vertices : list[Vertice], is_inner_or_outer : COLLUMN_STYLE):
        self.rdata = rdata
        self.vertices = vertices
        self.is_inner_or_outer = is_inner_or_outer
        self.height, self.length = self.get_dimentions()
        self.padding = 0
        self.window =  self.get_window()
        self.has_balcony = self.has_balcony()
        self.has_inter_floor = self.has_inter_floor()
        self.editor, self.materials = None,None
        
    def build(self, editor : Editor, materials : list[str]):  
        self.editor = editor
        self.materials = materials
                  
        for vertice in self.vertices:
            vertice.fill(editor, materials[0], self.height, xpadding = self.padding, zpadding = self.padding)
            with editor.pushTransform(Transform(vertice.point1.position,rotation = vertice.facing.value)):
                self.window.build(editor, materials)
                self.build_inter_floor()
        
    def get_window(self) -> Window:
        if self.is_inner_or_outer == COLLUMN_STYLE.OUTER or self.is_inner_or_outer == COLLUMN_STYLE.BOTH:
            self.padding = 1
        
        max_width = self.length-2*self.padding
        max_height = min(self.height, self.rdata["windows"]["size"]["max_height"])
            
        return Window(self.rdata["windows"] ,max_width, max_height, self.length, self.height)
    
    def get_balcony(self) -> Balcony:
        max_width = self.length-2*self.padding
        return Balcony(self.rdata["balcony"], max_width, self.window)
    
    def build_inter_floor(self):
        if self.has_inter_floor:
            geometry.placeCuboid(self.editor,(0,self.height,0),(self.length-1,self.height,0),Block(self.materials[0])) 
            geometry.placeCuboid(self.editor,(0,self.height,-1),(self.length-1,self.height,-1),Block(self.materials[4], {"facing": "south", "half": "top"})) 
    
    def has_balcony(self) -> bool:
        return self.rdata["balcony"]["proba"] >= rd.random()
    
    def has_inter_floor(self) -> bool:
        return self.rdata["inter_floor"] >= rd.random()
    
    def get_dimentions(self) -> tuple[int]:
        return ( self.vertices[0].get_height(), len(self.vertices[0]))
    