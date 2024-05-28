import random as rd
import math
from gdpc import Editor, Block, geometry, Transform
from utils.Enums import COLLUMN_STYLE, BORDER_RADIUS
from utils.functions import *
from buildings.geometry.Point import Point
from buildings.geometry.Vertice import Vertice
from buildings.elements.Glass import Glass

class Window:
    def __init__(self, rdata, max_width : int, max_height : int, facade_len : int, facade_height : int):
        self.rdata = rdata
        self.width, self.height = self.get_size(max_width, max_height)
        self.is_grounded = self.is_grounded()
        self.is_alternate = self.is_alternate()
        self.border_radius = self.border_radius()
        self.has_multiple = self.has_multiple_windows()
        self.has_vertical_crossbar, self.has_horizontal_crossbar = self.has_crossbars()
        self.padding, self.ypadding = self.get_padding(facade_len, facade_height)
        self.windows = self.get_windows()
        self.editor, self.materials = None,None
        
    def build(self, editor : Editor, materials : list[str]):
        self.editor = editor
        self.materials = materials
        with editor.pushTransform(Transform((self.padding,self.ypadding,0))):
            for g in self.windows:
                leng = len(g)
                g.build(editor, materials[1], materials[2])
                self.build_crossbars(g.x1, g.x2, leng)
                if leng > 1: self.build_border_radius(g.x1, g.x2)
                         
    def build_crossbars(self, x1 : int, x2 : int, len : int):
        if self.has_vertical_crossbar and self.height >= self.rdata["crossbars"]["min_height_for_vertical_crossbar"]:
            y = self.height//2
            geometry.placeCuboid(self.editor,(x1,y,0),(x2,y,0),Block(self.materials[3]))
        if self.has_horizontal_crossbar and len >= self.rdata["crossbars"]["min_width_for_horizontal_crossbar"]:
            x = len//2
            geometry.placeCuboid(self.editor,(x1+x,0,0),(x2-x,self.height,0),Block(self.materials[3], {"up" : "true"})) 
            
    def build_border_radius(self, x1 : int, x2 : int):
        if self.border_radius != BORDER_RADIUS.NONE:
            self.editor.placeBlock((x1,self.height,0),Block(self.materials[4], {"facing": "west", "half": "top"}))
            self.editor.placeBlock((x2,self.height,0),Block(self.materials[4], {"facing": "east", "half": "top"}))
        if self.border_radius == BORDER_RADIUS.TOP_AND_BOTTOM:
            self.editor.placeBlock((x1,0,0),Block(self.materials[4], {"facing": "west"}))
            self.editor.placeBlock((x2,0,0),Block(self.materials[4], {"facing": "east"}))
    
    
    def get_windows(self) -> list[Glass]:
        windows = []
        if not self.has_multiple: windows = [Glass(0,self.width-1,[self.create_window(0, self.width)])]
        else: windows = self.get_multiple_windows()
        if self.is_alternate: self.alternate(windows)
        
        return windows
        
    def get_multiple_windows(self) -> list[Glass]:
        windows = []
        slices = rd.randint(3, self.width//self.rdata["size"]["min_width"])
        mid = math.ceil(slices/2)
        windows_count = mid
        inter_count = slices - windows_count
        window_size = rd.randint(self.rdata["size"]["min_width"], (self.width-inter_count) // windows_count) 
        inter_size = (self.width - window_size*windows_count) // inter_count
        
        is_even= slices % 2 == 0
        is_window, gap = True, 0
        remainder = self.width - (window_size*windows_count + inter_size*inter_count)
        
        if windows_count % 2 == 1 and inter_count % 2 == 1: 
            inter_count -= 1
            remainder += inter_size
            is_even = not is_even
            
        for i in range(1,slices+1):
            wsize,isize = window_size, inter_size
            if is_even and i == mid: wsize, isize = wsize*2, isize*2
            if i ==  mid: wsize, isize = wsize + remainder, isize + remainder
            
            if is_window:               
                windows.append(Glass(gap, gap+wsize-1,[self.create_window(gap, wsize)]))
                gap += wsize
            else : 
                gap += isize
                
            is_window = not is_window
        
        return windows
    
    def alternate(self, windows : list[Glass]):
        for g in windows:
            g.reset_groups()
            leng = len(g)
            mid = g.x1 + leng//2
            
            is_block, is_even = False, leng % 2 == 0
            for x in range(g.x1,g.x2+1):
                if is_even and x == mid: is_block = not is_block # to keep symetry
                if is_block: g.group2.append(self.create_window(x))
                else : g.group1.append(self.create_window(x))
                is_block = not is_block
        
    def create_window(self, x1 : int, length : int = None) -> Vertice:
        x2 = x1 if length is None else x1 + length -1
        return Vertice(Point(x1,0,0), Point(x2,self.height,0))
    
    def has_multiple_windows(self):
        if self.width >  self.rdata["size"]["max_width"]: return True
        elif self.width >=  self.rdata["multiple"]["min_width"]:
            return self.rdata["multiple"]["proba"] >= rd.random()
        else : return False
    
    def is_alternate(self):
        # if the window alternate between glass_blocks and glass_panes
        return self.rdata["alternate"] >= rd.random()
    
        
    def get_size(self, max_width : int ,max_height : int) -> tuple[int,int]:
        return (
                rd.randint(self.rdata["size"]["min_width"],max_width),
                rd.randint(self.rdata["size"]["min_height"],max_height)
            )
        
    def get_padding(self, facade_len : int, facade_height : int) -> tuple[int]:
        padding,ypadding = 0,0
        if not self.is_grounded: ypadding = (facade_height - self.height)//2
        
        # correction to avoid asymetry
        padding = (facade_len - self.width)//2
        self.width = facade_len - padding*2
        
        return (padding, ypadding)
                          
    def is_grounded(self):
        # if the window is grounded or if there is a padding between the window and the ground
        return self.rdata["grounded"] >= rd.random()
    
    def has_crossbars(self):
        # if the window has crossbars
        data = self.rdata["crossbars"]
        
        return (data["vertical_crossbar"] >= rd.random(), data["horizontal_crossbar"] >= rd.random())
    
    def border_radius(self):
        return select_random(self.rdata["border_radius"], BORDER_RADIUS)