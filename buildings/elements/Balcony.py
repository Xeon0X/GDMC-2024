import random as rd
from gdpc import Editor, Block, geometry
from utils.functions import *
from utils.Enums import BALCONY_BORDER_RADIUS,COLLUMN_STYLE
from buildings.geometry.Point import Point
from buildings.geometry.Vertice import Vertice
from buildings.elements.Window import Window

class Balcony:
    def __init__(self, rdata, max_width : int, windows : Window, collumn_style : COLLUMN_STYLE):
        self.rdata = rdata
        self.windows = windows
        self.max_width = max_width
        self.collumn_style = collumn_style
        self.length = self.get_len()
        self.has_multiple = self.has_multiple()
        self.has_details = self.has_details()
        self.border_radius = self.has_border_radius()
        self.follow_window = self.follow_window()
        self.structure = self.get_structures()
        self.editor, self.materials = None,None
        
    def build(self, editor : Editor, materials : list[str]):
        self.editor = editor
        self.materials = materials
        for s in self.structure:
            s.fill(editor, materials[0])
            self.build_rembard(s)
            self.build_details(s)
            self.build_border_radius(s)
            
    def build_rembard(self, s : Vertice):
        geometry.placeCuboid(self.editor,(s.point1.x,1,-1),(s.point1.x,1,-self.length),Block(self.materials[3]))
        geometry.placeCuboid(self.editor,(s.point2.x,1,-1),(s.point2.x,1,-self.length),Block(self.materials[3]))
        geometry.placeCuboid(self.editor,(s.point1.x,1,-self.length),(s.point2.x,1,-self.length),Block(self.materials[3]))
        
    def build_details(self, s : Vertice):
        if not self.has_details: return
        geometry.placeCuboid(self.editor,(s.point1.x,0,-1),(s.point1.x,0,-self.length),Block(self.materials[4], {"facing": "east", "half": "top"}))
        geometry.placeCuboid(self.editor,(s.point2.x,0,-1),(s.point2.x,0,-self.length),Block(self.materials[4], {"facing": "west", "half": "top"}))
        geometry.placeCuboid(self.editor,(s.point1.x,0,-self.length),(s.point2.x,0,-self.length),Block(self.materials[4], {"facing": "south", "half": "top"}))
      
    def build_border_radius(self, s : Vertice):
        if self.border_radius == BALCONY_BORDER_RADIUS.NONE: return
        
        geometry.placeCuboid(self.editor,(s.point1.x,0,-self.length),(s.point1.x,1,-self.length),Block("air"))
        geometry.placeCuboid(self.editor,(s.point2.x,0,-self.length),(s.point2.x,1,-self.length),Block("air"))
        self.editor.placeBlock((s.point1.x+1,1,-self.length+1), Block(self.materials[3]))
        self.editor.placeBlock((s.point2.x-1,1,-self.length+1), Block(self.materials[3]))
        
        if self.has_details:
            self.editor.placeBlock((s.point1.x,0,-self.length+1), Block(self.materials[4], {"facing": "south", "half": "top"}))
            self.editor.placeBlock((s.point1.x+1,0,-self.length), Block(self.materials[4], {"facing": "east", "half": "top"}))
            self.editor.placeBlock((s.point2.x,0,-self.length+1), Block(self.materials[4], {"facing": "south", "half": "top"}))
            self.editor.placeBlock((s.point2.x-1,0,-self.length), Block(self.materials[4], {"facing": "west", "half": "top"}))
            
            if self.border_radius == BALCONY_BORDER_RADIUS.FULL:
                self.editor.placeBlock((s.point1.x+1,0,-self.length+1), Block(self.materials[4], {"facing": "east", "half": "top"}))
                self.editor.placeBlock((s.point2.x-1,0,-self.length+1), Block(self.materials[4], {"facing": "west", "half": "top"}))
        
    def get_structures(self) -> list[Vertice]:
        # structures are the base shape of the balcony
        attach_points = self.get_attach_points()
        len_attach_points = len(attach_points)-1
        min_wid = self.rdata["size"]["min_width"]
        min_gap = self.rdata["multiple"]["min_gap"]
        growth_chance = self.rdata["growth"]
        midpoint = len_attach_points//2
        x1,x2 = midpoint, len_attach_points - midpoint
        
        structures = []
        centered = True
        while x1 > 0:
            x1 -= 1
            x2 += 1 if centered else 0
            leng = attach_points[x2] - attach_points[x1] - 1
            
            if x1 == 0: 
                if leng >= min_wid: self.append_structure(structures, x1, x2, attach_points, len_attach_points, centered)
                break
            if leng < min_wid: continue
            
            if growth_chance < rd.random(): 
                self.append_structure(structures, x1, x2, attach_points, len_attach_points, centered)
                    
                if not self.has_multiple: break
                else:
                    centered = False
                    if attach_points[x1]-min_wid < min_gap: break
                    gap  = rd.randint(min_gap, attach_points[x1]-min_wid)
                    x2 = x1-gap
                    x1 = x2-min_wid+1
                           
        return structures
                
    def get_attach_points(self) -> list[int]:
        # points where the structures can start/finish
        padding = 0 if self.collumn_style.value < 2 else 1 # collumn_style < 2 = no outer collumns
        points = [i + padding for i in range(self.max_width)]
        if self.follow_window:
            pad = self.windows.padding
            for w in self.windows.windows:
                for i in range(pad+w.x1, pad+w.x2+1):
                    points.remove(i)
                    
        return points
    
    def create_structure(self, x1 : int, x2 : int) -> Vertice:
        return Vertice(Point(x = x1), Point(x = x2,z = -self.length))
    
    def append_structure(self, structures : list[Vertice], x1 : int, x2 : int, attach_points : list[int], len_attach_points : int, centered : bool):
        structures.append(self.create_structure(attach_points[x1], attach_points[x2]))
        if not centered:
            structures.append(self.create_structure(attach_points[len_attach_points-x1], attach_points[len_attach_points-x2]))
    
    def follow_window(self) -> bool:
        return not self.windows.ypadding > 3
        
    def has_multiple(self) -> bool:
        if self.max_width < self.rdata["multiple"]["min_width"]: return False
        return self.rdata["multiple"]["proba"] >= rd.random()
    
    def has_details(self) -> bool:
        return self.rdata["details"] >= rd.random()
    
    def has_border_radius(self) -> bool:
        if self.length < 2: return BALCONY_BORDER_RADIUS.NONE
        return select_random(self.rdata["border_radius"], BALCONY_BORDER_RADIUS)
    
    def get_len(self) -> int:
        return rd.randint(self.rdata["size"]["min_len"], self.rdata["size"]["max_len"])