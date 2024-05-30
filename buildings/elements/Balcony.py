import random as rd
from gdpc import Editor, Block, geometry, Transform
from buildings.geometry.Point import Point
from buildings.geometry.Vertice import Vertice
from buildings.elements.Window import Window

class Balcony:
    def __init__(self, rdata, max_width : int, windows : Window):
        self.rdata = rdata
        self.windows = windows
        self.max_width = max_width
        self.length = self.get_len()
        self.has_multiple = self.has_multiple_balcony()
        self.follow_window = self.follow_window()
        self.structure = self.get_structures()
        
    def build(self, editor : Editor, materials : list[str]):
        for s in self.structure:
            s.fill(editor, materials[0])
        
    def get_structures(self) -> list[Vertice]:
        attach_points = self.get_attach_points()
        len_attach_points = len(attach_points)
        min_wid = self.rdata["size"]["min_width"] -1
        min_gap = self.rdata["multiple"]["min_gap"]
        growth_chance = self.rdata["growth"]
        midpoint = len_attach_points//2
        x1,x2 = midpoint, len_attach_points - midpoint
        
        structures = []
        centered = True
        while True:
            x1 -= 1
            x2 += 1 if centered else 0
            leng = attach_points[x2] - attach_points[x1] - 1
            
            if x1 == 0: 
                if leng >= min_wid: structures.append(self.create_structure(attach_points[x1], attach_points[x2]))
                break
            if leng < min_wid: continue
            
            if growth_chance < rd.random(): 
                structures.append(self.create_structure(attach_points[x1], attach_points[x2]))
                if not centered:
                    structures.append(self.create_structure(attach_points[len_attach_points-x1], attach_points[len_attach_points-x2]))
                    
                if not self.has_multiple: break
                else:
                    if x1-min_wid < min_gap: break
                    gap  = rd.randint(min_gap, x1-min_wid)
                    x2 = x1-gap
                    x1 = x2-min_wid
                    
                
        return structures
                
    def get_attach_points(self) -> list[int]:
        points = [i for i in range(self.max_width)]
        if self.follow_window:
            for w in self.windows.windows:
                for i in range(w.x1, w.x2+1):
                    points.remove(i)
                    
        return points
    
    def create_structure(self, x1 : int, x2 : int) -> Vertice:
        return Vertice(Point(x1,0,0), Point(x2,0,self.length-1))
    
    def follow_window(self) -> bool:
        return self.windows.ypadding > 3
        
    def has_multiple_balcony(self) -> bool:
        if self.max_width < self.rdata["multiple"]["min_width"]: return False
        return self.rdata["multiple"]["proba"] >= rd.random()
    
    def get_len(self) -> int:
        return rd.randint(self.rdata["size"]["min_len"], self.rdata["size"]["max_len"])