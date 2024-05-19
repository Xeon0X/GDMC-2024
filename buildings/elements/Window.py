import random as rd
import math
from gdpc import Editor, Block, geometry
from utils.Enums import DIRECTION
from buildings.geometry.Point import Point
from buildings.geometry.Vertice import Vertice

class Window:
    def __init__(self, rdata, size : tuple[int,int]):
        self.rdata = rdata
        self.width, self.height = size
        self.is_grounded = self.is_grounded()
        self.has_multiple_windows = self.has_multiple_windows()
        self.is_alternate = self.is_alternate()
        self.has_vertical_crossbar, self.has_horizontal_crossbar = self.has_crossbars()
        self.padding = 0
        self.editor, self.materials = None,None
        
    def build(self, editor : Editor, vertice : Vertice, height : int, y : int, materials : list[str]):
        self.editor = editor
        self.materials = materials
        
        len = vertice.get_size()
        self.padding = (len - self.width)//2
        self.width = len - self.padding*2
        self.is_alternate = True
        if not self.is_grounded: y += (height - self.height)//2
        
        if self.has_multiple_windows: self.build_multiple_windows(vertice,  y)
        else : 
            xpadding, zpadding = self.padding, self.padding
            if vertice.facing == DIRECTION.NORTH or vertice.facing == DIRECTION.SOUTH: zpadding = 0
            else: xpadding = 0
            
            self.place_glasses(Point(vertice.point1.x+xpadding, y, vertice.point1.z+zpadding), 
                               Point(vertice.point2.x-xpadding, y+self.height, vertice.point2.z-zpadding))
        
    def build_multiple_windows(self, vertice : Vertice, y : int):
        slices = rd.randint(3, self.width//self.rdata["size"]["min_width"])
        mid = math.ceil(slices/2)
        windows_count = mid
        inter_count = slices - windows_count
        window_size = rd.randint(self.rdata["size"]["min_width"], (self.width-inter_count) // windows_count) 
        inter_size = (self.width - window_size*windows_count) // inter_count
        
        is_even= slices % 2 == 0
        is_window, gap = True, 0
        remainder = self.width - (window_size*windows_count + inter_size*inter_count)
        for i in range(1,slices+1):
            wsize,isize = window_size, inter_size
            if is_even and i == mid: wsize, isize = wsize*2, isize*2
            if i ==  mid: wsize, isize = wsize + remainder, isize + remainder
            
            # kepp a spacing between windows, "is revert" is used to keep symetry
            if is_window:
                #set the values to orient windows in x or z axis
                xpadding,xlen,zpadding,zlen = 0,0,0,0
                if vertice.facing == DIRECTION.NORTH or vertice.facing == DIRECTION.SOUTH:
                    xpadding,xlen = self.padding + gap, wsize-1
                else: zpadding,zlen = self.padding + gap, wsize-1
                
                self.place_glasses(Point(vertice.point1.x+xpadding, y, vertice.point1.z+zpadding), 
                                   Point(vertice.point1.x+xpadding+xlen, y+self.height, vertice.point1.z+zpadding+zlen))
                gap += wsize
            else : 
                gap += isize
                
            is_window = not is_window
    
    def place_glasses(self, pos1 : Point, pos2 : Point):
        
        xlen, zlen = pos2.x - pos1.x, pos2.z - pos1.z
        len = xlen + zlen
        if self.is_alternate:
            mid = len//2 + 1
            
            is_block, is_even = False, len % 2 == 1 # yeah the result isn't actually even but it's because either xlen or zlen is 1, we want to know of the other result is even
            for x in range(xlen+1):
                for z in range(zlen+1):
                    if is_even and (x+z) == mid: is_block = not is_block # to keep symetry
                    id = 1 if not is_block else 2
                    geometry.placeCuboid(self.editor,(pos1.x+x,pos1.y,pos1.z+z),(pos1.x+x,pos2.y,pos1.z+z),Block(self.materials[id]))
                    is_block = not is_block
            
        else:
            geometry.placeCuboid(self.editor,pos1.position,pos2.position,Block(self.materials[1]))
            
        self.build_crossbars(pos1, pos2, len)
            
            
    def build_crossbars(self, pos1 : Point, pos2 : Point, len : int):
        if self.has_vertical_crossbar and self.height >= self.rdata["crossbars"]["min_height_for_vertical_crossbar"]:
            print(pos1.x,pos2.x)
            y = self.height//2
            geometry.placeCuboid(self.editor,(pos1.x,pos1.y+y,pos1.z),(pos2.x,pos2.y-y,pos2.z),Block(self.materials[3]))
        if self.has_horizontal_crossbar and len >= self.rdata["crossbars"]["min_width_for_horizontal_crossbar"]:
            pass 
                          
    def is_grounded(self):
        # if the window is grounded or if there is a padding between the window and the ground
        if self.rdata["grounded"] >= rd.random(): return True
        return False
    
    def has_multiple_windows(self):
        if self.width >  self.rdata["size"]["max_width"]: return True
        if self.width >=  self.rdata["multiple"]["min_width"]:
            return True
            if self.rdata["multiple"]["proba"] >= rd.random(): return True
        return False
    
    def is_alternate(self):
        # if the window alternate between glass_blocks and glass_panes
        if self.rdata["alternate"] >= rd.random(): return True
        return False
    
    def has_crossbars(self):
        # if the window has crossbars
        data = self.rdata["crossbars"]
        
        return (data["vertical_crossbar"] >= rd.random(), data["horizontal_crossbar"] >= rd.random())