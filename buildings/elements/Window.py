import random as rd
import math
from gdpc import Editor, Block, geometry
from utils.Enums import DIRECTION
from buildings.geometry.Vertice import Vertice

class Window:
    def __init__(self, rdata, size : tuple[int,int]):
        self.rdata = rdata
        self.width, self.height = size
        self.is_grounded = self.is_grounded()
        self.has_multiple_windows = self.has_multiple_windows()
        self.padding = 0
        
    def build(self, editor : Editor, vertice : Vertice, height : int, y : int, materials : list[str]):
        self.padding = (vertice.get_size() - self.width)//2
        if not self.is_grounded: y += (height - self.height)//2
        
        if self.has_multiple_windows: self.build_multiple_windows(editor, vertice, self.padding, self.height, y, materials)
        else : vertice.fill(editor, materials[1], y, y + self.height, xpadding = self.padding, zpadding = self.padding)
        
    def build_multiple_windows(self, editor : Editor, vertice : Vertice, padding : int, height : int, y : int, materials : list[str]):
        slices = rd.randint(2, self.width//self.rdata["size"]["min_width"])
        windows_count = math.ceil(slices/2)
        inter_count = slices - windows_count
        window_size = rd.randint(self.rdata["size"]["min_width"], self.width-inter_count // windows_count) 
        inter_size = (self.width - window_size*windows_count) // inter_count
        
        revert, switching = slices % 2 == 0, math.ceil(slices/2)
        is_revert, gap = False, 0
        for i in range(1,slices+1):
            modulo = i % 2
            if revert and i == switching: is_revert = True
            
            # kepp a spacing between windows, "is revert" is used to keep symetry
            if modulo == 0 or (modulo == 1 and is_revert):
                #set the values to orient windows in x or z axis
                xpadding,xlen,zpadding,zlen = 0,0,0,0
                if vertice.facing == DIRECTION.NORTH or vertice.facing == DIRECTION.SOUTH:
                    xpadding,xlen = self.padding + gap, window_size
                else: zpadding,zlen = self.padding + gap, window_size
                
                geometry.placeCuboid(editor, 
                                    (vertice.point1.x+xpadding, y, vertice.point1.z+zpadding), 
                                    (vertice.point1.x+xpadding+xlen, y+self.height, vertice.point1.z+zpadding+zlen),
                                    Block(materials[1]))
                gap += window_size
            else : 
                gap += inter_size
                  
    def is_grounded(self):
        # if the window is grounded or if there is a padding between the window and the ground
        if self.rdata["grounded"] >= rd.random(): return True
        return False
    
    def has_multiple_windows(self):
        if self.width >  self.rdata["size"]["max_width"]: return True
        if self.width >=  self.rdata["multiple"]["min_width"]:
            if self.rdata["multiple"]["proba"] >= rd.random(): return True
        return False
    
    def open(self):
        pass
    
    def close(self):
        pass