import random as rd
from buildings.Foundations import Foundations
from buildings.Facade import Facade

class Building:
    def __init__(self,rdata, position : tuple[int,int], size : tuple[int, int], matrice : list[list[int]], floors : int):
        self.position = position
        self.length, self.width = size
        self.matrice = matrice
        self.floors = floors
        
        # Generate every random components here
        tile_size = self.gen_tile_size()
        
        self.foundations = Foundations(rdata["foundations"], size, matrice, tile_size,)
        self.facade = Facade(rdata["facade"], self.foundations.vertices, self.foundations.is_inner_or_outer)
        
    def build(self, editor, materials : list[str]):
        for y in range(self.floors):      
            with editor.pushTransform((self.position[0], y*(self.foundations.floor_height+1), self.position[1])):
                self.foundations.build(editor, materials)
                self.facade.build(editor, materials)
        
    def gen_tile_size(self) -> int:
        # Tiles are constant square units different for each buildings
        return self.length
        smaller_side = min(self.length, self.width)
        
        # area is too small, will work but not very well
        if smaller_side <= 5 : return smaller_side
        if smaller_side <= 15 : return smaller_side // 5
        
        return rd.randint(3, smaller_side // len(self.matrice))
    