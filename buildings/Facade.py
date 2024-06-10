from Enums import COLLUMN_STYLE
from buildings.geometry.Vertice import Vertice
from buildings.geometry.Rectangle import Rectangle
from buildings.elements.Window import Window

class Facade:
    def __init__(self, vertices : list[Vertice], height : int, is_inner_or_outer : COLLUMN_STYLE):
        self.vertices = vertices
        self.is_inner_or_outer = is_inner_or_outer
        self.height = height
        self.window_size = self.get_window_size()
        self.window =  self.get_window()
        self.has_balcony = self.has_balcony()
        self.has_inter_floor = self.has_inter_floor()
        
    def build_facade(self):
        pass
        
    def get_window_size(self) -> tuple[int,int]:
        pass
        
    def has_balcony(self) -> bool:
        pass
    
    def has_inter_floor(self) -> bool:
        pass
    
    def get_window(self) -> Window:
        pass