import random as rd
from utils.Enums import COLLUMN_STYLE
from buildings.Foundations import Foundations
from buildings.Facade import Facade

class Building:
    def __init__(self, position : tuple[int,int], size : tuple[int, int], matrice : list[list[int]]):
        self.position = position
        self.length, self.width = size
        self.matrice = matrice
        
        # Generate every random components here
        is_collumn_full_tile = bool(rd.getrandbits(1))
        is_inner_or_outer = rd.choice(list(COLLUMN_STYLE))
        tile_size = self.gen_tile_size()
        floor_height = rd.randint(4, 7)
        
        is_inner_or_outer = COLLUMN_STYLE.BOTH
        
        self.foundations = Foundations(size, matrice, tile_size, is_collumn_full_tile, is_inner_or_outer)
        self.facade = Facade(self.foundations.vertices, floor_height, is_inner_or_outer)
        
    def gen_tile_size(self) -> int:
        # Tiles are constant square units different for each buildings
        smaller_side = min(self.length, self.width)
        
        # area is too small, will work but not very well
        if smaller_side <= 15 : return smaller_side // 5
        
        return rd.randint(3, smaller_side // len(self.matrice))
    