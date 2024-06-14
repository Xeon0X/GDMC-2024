import random as rd
import numpy as np
import math

from utils.Enums import COLLUMN_STYLE
from utils.functions import *
from buildings.geometry.Tile import Tile
from buildings.geometry.Polygon import Polygon
from buildings.geometry.Point import Point
from buildings.elements.Collumn import Collumn

class Foundations:
    # TODO : gérer les collones sur les tiles trop petites et les colones 1tile/2
    
    def __init__(self,
                 rdata,
                 size : tuple[int, int], 
                 matrice : list[list[int]], 
                 tile_size : int):
        # Foundations are the base of the building, they are made of tiles and based on a matrice
        
        # Random components
        self.tile_size = tile_size
        self.is_inner_or_outer = select_random(rdata["collumn_style"], COLLUMN_STYLE)
        self.floor_height = rd.randint(rdata["floor"]["min_height"], rdata["floor"]["max_height"])-1
        
        self.size = size
        self.length, self.width = size
        self.matrice = matrice
        self.tiles = []
        self.vertices = []
        self.length_in_tiles = self.length // self.tile_size
        self.width_in_tiles = self.width // self.tile_size
        self.x_distribution = []
        self.z_distribution = []
        self.polygon = self.get_polygon()
        self.collumns = self.get_columns()
        
    def build(self, editor, materials : list[str]):
        self.polygon.fill(editor, materials[5],0)
        self.polygon.fill(editor, materials[6], self.floor_height)
        self.build_collumns(editor, materials)
        
    def build_collumns(self, editor, materials : list[str]):
        for collumn in self.collumns:
            if collumn.is_outer and self.is_inner_or_outer == COLLUMN_STYLE.INNER: continue
            if not collumn.is_outer and self.is_inner_or_outer == COLLUMN_STYLE.OUTER: continue
            collumn.fill(editor, materials[7], self.floor_height+1)
    
    def add_tile(self, tile : Tile):
        self.tiles.append(tile)
    
    def get_polygon(self) -> Polygon:
        ## The polygon is a shape of tiles representing the foundation shape
        polygon = Polygon(self.size)
        
        # we save the distribution, usefull for the next steps 
        self.x_distribution = self.get_distribution(len(self.matrice), self.length_in_tiles)
        self.z_distribution = self.get_distribution(len(self.matrice[0]), self.width_in_tiles)
        
        # this bullshit is to create tiles from the matrice and the distribution
        x_padding = 0
        for x,xsize in enumerate(self.x_distribution):
            z_padding = 0
            for z,zsize in enumerate(self.z_distribution):
                if self.matrice[x][z] == 1:
                    for xi in range(xsize):
                        for zi in range(zsize):
                            tile = Tile(self.tile_size, (x_padding + xi*self.tile_size, z_padding + zi*self.tile_size))
                            self.add_tile(tile)
                z_padding += zsize * self.tile_size
            x_padding += xsize * self.tile_size               
        
        polygon.set_vertices_and_neighbors(self.tiles, self.vertices, self.floor_height)   
        polygon.compress(self.tiles, self.vertices)                 
        return polygon
        
        
        
    def get_distribution(self,length,avaliable_tiles):
        # foundations are based on a matrice, 
        # this function gives the number of tiles for each row/collumn of the matrice, giving a more random shape
        # The real shit start here
        if length == avaliable_tiles:
            return [1 for i in range(avaliable_tiles)]
        
        if length == 1:
            return [avaliable_tiles]
        
        if length == 2:
            l = rd.randint(1,avaliable_tiles-1)
            return [l,avaliable_tiles-l]
        
        if length >= 3:
            sizes = []
            intersections_count = math.ceil(length/2)-1
            tiles_per_side = avaliable_tiles//2
            correction = 0
            
            intersect_values = np.random.choice(np.arange(1,tiles_per_side), size=intersections_count, replace=False)
            
            #we generate only half of the distribution      
            last_pos = 0
            intersect_values = np.append(intersect_values,tiles_per_side)
            for intersect in intersect_values:
                sizes.append(intersect - last_pos)
                last_pos = intersect
             
            # we duplicate the side for the symetry
            symetry = sizes.copy()
            symetry.reverse()  
            if avaliable_tiles%2 == 1: correction = 1  # if there is a tile left, add it randomly
            if length%2 == 1 : sizes[-1], symetry = sizes[-1]*2 + correction,  symetry[1:]
            sizes += symetry
                
            return sizes
    
    def get_columns(self) -> list[Collumn]:
        if self.is_inner_or_outer ==  COLLUMN_STYLE.NONE: return []
        collumns = []
        
        for tile in self.tiles:
            north_west_collumn = Collumn(Point(x = tile.north_west.x-1, z = tile.north_west.z-1), tile.north_west)
            north_east_collumn = Collumn(Point(x = tile.north_east.x, z = tile.north_east.z-1), Point(x = tile.north_east.x+1, z = tile.north_east.z))
            south_west_collumn = Collumn(Point(x = tile.south_west.x-1, z = tile.south_west.z), Point(x = tile.south_west.x, z = tile.south_west.z+1))
            south_east_collumn = Collumn(tile.south_east, Point(x = tile.south_east.x+1, z = tile.south_east.z+1))
            
            if tile.north_vertice != None or tile.west_vertice != None: north_west_collumn.set_is_outer(True)
            
            if tile.north_vertice != None or tile.east_vertice != None: north_east_collumn.set_is_outer(True)
            
            if tile.south_vertice != None or tile.west_vertice != None: south_west_collumn.set_is_outer(True)
            
            if tile.south_vertice != None or tile.east_vertice != None: south_east_collumn.set_is_outer(True)

            collumns.extend([north_west_collumn, north_east_collumn, south_west_collumn, south_east_collumn])
        
        return self._suppr_doubblons_collumns(collumns)
                   
    def _suppr_doubblons_collumns(self, collumns : list[Collumn]): 
        for index,collumn in enumerate(collumns):
            if index == len(collumns)-1: break
            for compare in  collumns[index+1:]:
                if collumn.point1.position == compare.point1.position :
                    if compare.is_outer : collumn.set_is_outer(True)
                    collumns.remove(compare)
                   
        return collumns
    
        