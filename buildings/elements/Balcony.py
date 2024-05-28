import random as rd
from buildings.geometry.Point import Point
from buildings.geometry.Vertice import Vertice
from buildings.elements.Window import Window

class Balcony:
    def __init__(self, rdata, windows : Window):
        self.rdata = rdata
        self.windows = windows
        self.length = self.get_len()
        self.has_multiple = self.has_multiple_balcony()
        self.follow_window = self.follow_window()
        
    def get_structures(self) -> list[Vertice]:
        attach_points = self.get_attach_points()
        len_attach_points = len(attach_points)
        min_wid = self.rdata["balcony"]["size"]["min_width"]
        growth_chance = self.rdata["balcony"]["growth"]
        midpoint = len_attach_points//2
        x1,x2 = midpoint, len_attach_points - midpoint
        
        structures = []
        while True:
            x1 -= 1
            x2 += 1
            if x1 < 0 : break
            if attach_points[x2] - attach_points[x1] + 1 < min_wid: continue
            if growth_chance < rd.random(): 
                structures.append(self.create_structure(attach_points[x1], attach_points[x2]))
                if not self.has_multiple: break
                
                
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
        if self.max_width < self.rdata["balcony"]["multiple"]["min_width"]: return False
        return self.rdata["balcony"]["multiple"]["proba"] >= rd.random()
    
    def get_len(self) -> int:
        return rd.randint(self.rdata["balcony"]["size"]["min_len"], self.rdata["balcony"]["size"]["max_len"])