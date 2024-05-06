import random as rd
import numpy as np
import math
from buildings.geometry.Tile import Tile
from buildings.geometry.Polygon import Polygon
from buildings.geometry.Point import Point
from buildings.geometry.Rectangle import Rectangle

class Foundations:
    def __init__(self, position : tuple[int,int], size : tuple[int, int], matrice : list[list[int]]):
        # Foundations are the base of the building, they are made of tiles and based on a matrice
        x,z = position
        self.position = Point(x = x, z = z)
        self.size = size
        self.length = size[0]
        self.width = size[1]
        self.matrice = matrice
        self.tiles = []
        self.tile_size = self.define_tile_size()
        self.length_in_tiles = self.length // self.tile_size
        self.width_in_tiles = self.width // self.tile_size
        self.x_distribution = []
        self.z_distribution = []
        self.polygon = self.get_polygon()
        self.collumns = self.get_columns()
        
    def define_tile_size(self) -> int:
        # Tiles are constant square units different for each buildings
        smaller_side = min(self.length, self.width)
        
        # area is too small, will work but not very well
        if smaller_side <= 15 : return smaller_side // 5
        
        return rd.randint(3, smaller_side // len(self.matrice))
    
    def add_tile(self, tile : Tile):
        self.tiles.append(tile)
    
    def get_polygon(self) -> Polygon:
        ## The polygon is a shape of tiles representing the foundation shape
        polygon = Polygon(self.position, self.size)
        avaliable_space = (self.length_in_tiles, self.width_in_tiles)
        
        # we save the distribution, usefull for the next steps 
        self.x_distribution = self.get_distribution(len(self.matrice), avaliable_space[0])
        self.z_distribution = self.get_distribution(len(self.matrice[0]), avaliable_space[1])
        
        # this bullshit is to create tiles from the matrice and the distribution
        x_padding = self.position.x
        for x,xsize in enumerate(self.x_distribution):
            z_padding = self.position.z
            for z,zsize in enumerate(self.z_distribution):
                if self.matrice[x][z] == 1:
                    for xi in range(xsize):
                        for zi in range(zsize):
                            tile = Tile(self.tile_size, (x_padding + xi*self.tile_size, z_padding + zi*self.tile_size))
                            self.add_tile(tile)
                z_padding += zsize * self.tile_size
            x_padding += xsize * self.tile_size               
        
        polygon.set_vertices_and_neighbors(self.tiles)   
        polygon.compress(self.tiles)                 
        return polygon
        
        
        
    def get_distribution(self,length,avaliable_tiles):
        # foundations are based on a matrice, 
        # this function gives the number of tiles for each row/collumn of the matrice, giving a more random shape
        # The real shit start here
        if length == 1:
            return [avaliable_tiles]
        
        if length == 2:
            l = rd.randint(1,avaliable_tiles-1)
            return [l,avaliable_tiles-l]
        
        if length >= 3:
            is_len_even = length % 2 == 0
            is_availiable_even = avaliable_tiles % 2 == 0
            sizes = []
            
            # This is to keep symetry in case of an even matrice
            if not is_len_even:
                center = rd.randint(1,avaliable_tiles-length+1)
                avaliable_tiles -= center
                is_availiable_even = avaliable_tiles % 2 == 0

                if not is_availiable_even: center += 1

                sizes.append(center)
                is_availiable_even = True
            
            intersection_number = length // 2 - 1
            tiles_per_side = avaliable_tiles // 2
            # we keep symetry we randomize only one side
            intersect_values = np.random.choice(np.arange(1,tiles_per_side), size=intersection_number, replace=False)
            
            # we duplicate the side for the symetry
            last_pos = 0
            intersect_values = np.append(intersect_values,tiles_per_side)
            for intersect in intersect_values:
                size = [intersect - last_pos]
                sizes = size + sizes + size
                last_pos = intersect
            
            # if there is a tile left, add it randomly
            if not is_availiable_even: sizes[rd.randint(0,len(sizes)-1)] += 1
            return sizes
    
    def get_columns(self) -> list[Rectangle]:
        collumns = []
        is_full_tile = bool(rd.getrandbits(1))
        x_padding = self.position.x
        
        for x,row in enumerate(self.matrice):
            z_padding = self.position.z
            lenx = self.x_distribution[x]
            
            for z,value in enumerate(row):
                lenz = self.z_distribution[z]
                
                # conditions to not make a collumn on the facade of the building (no outter collumns)
                
                skip_first_x,skip_first_z = False,False
                # if it's the first or last row/collumn 
                if x == 0 : skip_first_x = True
                if z == 0 : skip_first_z = True
                    
                last_value_x,last_value_z = self.matrice[x-1][z],self.matrice[x][z-1]
                # if the previous row/collumn is empty
                if last_value_x == 0 : skip_first_x = True
                if last_value_z == 0 : skip_first_z = True
                
                next_value_x,next_value_z = 0,0
                try : next_value_x = self.matrice[x+1][z]
                except : pass
                try : next_value_z = self.matrice[x][z+1]
                except : pass
                # if this part of the building is too tiny
                if last_value_x == 0 and next_value_x == 0 and self.x_distribution[x] == 1: continue
                if last_value_z == 0 and next_value_z == 0 and self.z_distribution[z] == 1: continue
                
                if value == 1:
                    self.create_collumns(x_padding, z_padding, lenx, lenz, skip_first_x, skip_first_z, collumns)
                    
                z_padding += lenz * self.tile_size
            x_padding += lenx * self.tile_size
    
        return collumns
        
    def create_collumns(self, basex : int, basez : int, lenx : int, lenz : int, skip_first_x : bool, skip_first_z : bool, collumns : list[Rectangle]):
        for x in range(lenx):
            if x==0 and skip_first_x: continue
            for z in range(lenz):
                if z==0 and skip_first_z: continue
                collumns.append(Rectangle(Point(x = basex+x*self.tile_size, z = basez+z*self.tile_size), Point(x = basex+x*self.tile_size-1, z = basez+z*self.tile_size-1)))
        