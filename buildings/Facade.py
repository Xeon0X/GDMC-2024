import random as rd
from utils.functions import *
from utils.Enums import COLLUMN_STYLE,DIRECTION,INTER_FLOOR_BORDER
from gdpc import Editor, Block, geometry, Transform
from buildings.geometry.Vertice import Vertice
from buildings.geometry.Point import Point
from buildings.elements.Window import Window
from buildings.elements.Balcony import Balcony

class Facade:
    def __init__(self, 
                 rdata, 
                 vertices : list[Vertice], 
                 collumn_style : COLLUMN_STYLE):
        self.rdata = rdata
        self.vertices = vertices
        self.collumn_style = collumn_style
        self.height, self.length = self.get_dimentions()
        self.padding = 0
        self.window =  self.get_window()
        self.has_balcony = self.has_balcony()
        self.balcony = self.get_balcony()
        self.has_inter_floor, self.inter_floor_border_style = self.has_inter_floor()
        self.editor, self.materials = None,None
        
    def build(self, editor : Editor, materials : list[str]):  
        self.editor = editor
        self.materials = materials
        points = sum([[vertice.point1, vertice.point2] for vertice in self.vertices], [])
                  
        for vertice in self.vertices:
            flip=(vertice.facing == DIRECTION.WEST or vertice.facing == DIRECTION.SOUTH, False, False)
            vertice.fill(editor, materials[0], self.height, xpadding = self.padding, zpadding = self.padding)
            with editor.pushTransform(Transform(vertice.point1.position,rotation = vertice.facing.value, flip = flip)):
                self.window.build(editor, materials)
                if self.has_inter_floor: self.build_inter_floor()
                if self.has_balcony: self.balcony.build(editor, materials)
                self.correct_corners(points,vertice)
                
    def correct_corners(self,points : list[Point], v : Vertice):
        if self.padding == 0:
            if self.window.border_radius != 0 and self.window.width == self.length:
                if points.count(v.point1) >= 2:
                    self.editor.placeBlock((0,self.window.ypadding,0), Block(self.materials[8]))
                    self.editor.placeBlock((0,self.window.ypadding+self.window.height,0), Block(self.materials[8], {"type": "top"}))
                if points.count(v.point2) >= 2:
                    self.editor.placeBlock((self.length-1,self.window.ypadding,0), Block(self.materials[8]))
                    self.editor.placeBlock((self.length-1,self.window.ypadding+self.window.height,0), Block(self.materials[8], {"type": "top"}))
            
            if self.has_inter_floor:
                material = Block("air")
                if self.inter_floor_border_style == INTER_FLOOR_BORDER.SLAB:
                    material = Block(self.materials[8], {"type": "top"})
                elif self.inter_floor_border_style == INTER_FLOOR_BORDER.STAIRS:
                    material = Block(self.materials[4], {"facing": "south", "half": "top"})
                    
                if points.count(v.point1) >= 2:
                    self.editor.placeBlock((-1,self.height,-1), material)
                if points.count(v.point2) >= 2:
                    self.editor.placeBlock((self.length,self.height,-1), material)
                     
        
    def get_window(self) -> Window:
        if self.collumn_style.value >= 2: # collumn_style >= 2 = outer collumns
            self.padding = 1
            
        max_width = self.length-2*self.padding
        max_height = min(self.height, self.rdata["windows"]["size"]["max_height"])
            
        return Window(self.rdata["windows"] ,max_width, max_height, self.length, self.height)
    
    def get_balcony(self) -> Balcony|None:
        if not self.has_balcony: return None
        max_width = self.length-2*self.padding
        return Balcony(self.rdata["balcony"], max_width, self.window, self.collumn_style)
    
    def build_inter_floor(self):
        geometry.placeCuboid(self.editor,(self.padding,self.height,0),(self.length-1-self.padding,self.height,0),Block(self.materials[0])) 
        geometry.placeCuboid(self.editor,(self.padding,self.height,-1),(self.length-1-self.padding,self.height,-1),Block(self.materials[4], {"facing": "south", "half": "top"})) 

    def has_balcony(self) -> bool:
        return self.rdata["balcony"]["proba"] >= rd.random()
    
    def has_inter_floor(self) -> bool:
        return (self.rdata["inter_floor"]["proba"] >= rd.random(), select_random(self.rdata["inter_floor"]["border_style"], INTER_FLOOR_BORDER))
    
    def get_dimentions(self) -> tuple[int,int]:
        return ( self.vertices[0].get_height(), len(self.vertices[0]))
    