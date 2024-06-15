import random as rd
from utils.Enums import DIRECTION
from gdpc import Editor, Block, geometry
from buildings.Foundations import Foundations
from buildings.Facade import Facade
from buildings.Entrance import Entrance
from buildings.Roof import Roof

class Building:
    def __init__(self,rdata, positions : list[tuple[int,int,int]], matrice : list[list[int]], doors_direction : DIRECTION):
        self.position = (0,0,0)
        self.length, self.width, self.height = 0,0,0
        self.matrice = matrice
        
        self.get_pos_and_size(positions)
        tile_size = self.gen_tile_size()
        
        self.foundations = Foundations(rdata["foundations"], (self.length,self.width), matrice, tile_size,)
        self.facade = Facade(rdata["facade"], self.foundations.vertices, self.foundations.is_inner_or_outer)
        self.entrance = Entrance(rdata, self.foundations.vertices, doors_direction, self.foundations.is_inner_or_outer)
        self.roof = Roof(rdata["roof"], self.foundations.polygon)
        
    def build(self, editor : Editor, materials : list[str]):
        y=0
        while y < self.height:      
            with editor.pushTransform((self.position[0], y -1, self.position[1])):
                self.foundations.build(editor, materials)
                if y == 0: self.entrance.build(editor, materials)
                else : self.facade.build(editor, materials)
            y+=self.foundations.floor_height+1
        with editor.pushTransform((self.position[0], y -1, self.position[1])): self.roof.build(editor, materials)
        
    def gen_tile_size(self) -> int:
        # Tiles are constant square units different for each buildings
        smaller_side = min(self.length, self.width)
        
        # area is too small, will work but not very well
        if smaller_side <= 5 : return smaller_side
        if smaller_side <= 15 : return smaller_side // 5
        
        return rd.randint(3, smaller_side // len(self.matrice))
    
    def get_pos_and_size(self, pos : list[tuple[int,int,int]]) -> tuple[tuple[int,int],int,int]:
        pos1, pos2 = pos[0], pos[1]
        self.position = (min(pos1[0], pos2[0]), min(pos1[1], pos2[1]), min(pos1[2], pos2[2]))
        self.length = abs(pos1[0] - pos2[0])
        self.height = abs(pos1[1] - pos2[1])
        self.width = abs(pos1[2] - pos2[2])
        