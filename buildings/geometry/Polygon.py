from Enums import DIRECTION
from gdpc import Editor, Block, geometry
from buildings.geometry.Tile import Tile
from buildings.geometry.Point import Point
from buildings.geometry.Rectangle import Rectangle
from buildings.geometry.Vertice import Vertice

class Polygon:
    def __init__(self, position : Point, size: tuple[int,int], vertices : list[Vertice] = []):
        self.position = position
        self.size = size
        self.compressed = {"shape":[], "vertices":[]}
        self.vertices = vertices
        
    def fill_polygon(self, editor : Editor, material : str, y : int, y2 : int = None):
        if y2 == None: y2 = y
        for rect in self.compressed["shape"]:
            rect.fill(editor, material, y, y2)
        
    def fill_vertice(self, editor : Editor, material : str, y : int, y2 : int = None):
        if y2 == None: y2 = y
        for vertice in self.compressed["vertices"]:
            vertice.fill(editor, Block(material), y, y2)

    def compress(self, tiles : list[Tile]):
        remaining_tiles = tiles.copy()
        while len(remaining_tiles) > 0:
            start = remaining_tiles[0]
            neightbor = start.get_neighbor(DIRECTION.WEST)
            row = []
            
            # Find western border
            while neightbor:
                start = neightbor
                neightbor = start.get_neighbor(DIRECTION.WEST)
            
            # Find eastern border
            while True:
                row.append(start)
                remaining_tiles.remove(start)
                neightbor = start.get_neighbor(DIRECTION.EAST)
                if not neightbor: break
                start = neightbor            
            
            # Find northern border
            north_row = self.find_row_border(row.copy(), DIRECTION.NORTH, remaining_tiles) 
            # Find southern border   
            south_row = self.find_row_border(row.copy(), DIRECTION.SOUTH, remaining_tiles)
            
            area = Rectangle(north_row[0].north_west, south_row[-1].south_east)    
            self.compressed["shape"].append(area)    
        
        remaining_vertices = self.vertices.copy()
        current = remaining_vertices.pop()
        while len(remaining_vertices) > 0:
            neighbors = current.get_neighbors()
            has_next1 = self.has_next(neighbors[0], current.facing, remaining_vertices)
            has_next2 = self.has_next(neighbors[1], current.facing, remaining_vertices)
            
            if has_next1:
                current = Vertice(has_next1.point1, current.point2, current.facing)
            elif has_next2:
                current = Vertice(current.point1, has_next2.point2, current.facing)
            else:
                self.compressed["vertices"].append(current)
                current = remaining_vertices.pop()
            
            if len(remaining_vertices) == 0: self.compressed["vertices"].append(current)     
                    
    def find_row_border(self, line : list[Tile], direction : str, remaining_tiles : list[Tile]) -> list[Tile]:
        while True:
            new_line = []
            for tile in line:
                neightbor = tile.get_neighbor(direction)
                if neightbor not in remaining_tiles: return line
                new_line.append(neightbor)
            for tile in new_line: remaining_tiles.remove(tile)
            line = new_line

    def set_vertices_and_neighbors(self, tiles : list[Tile]):
        for tile in tiles:
            targets = tile.get_neighbors_coords()
            for vertice_num,target in enumerate(targets):
                has_neighbor = self.has_neighbor(target, tiles)
                if not has_neighbor:
                    self.vertices.append(tile.get_vertice(vertice_num))
                else :
                    tile.set_neighbor(vertice_num, has_neighbor)
    
    def has_neighbor(self, target : tuple[int], tiles : list[Tile]) -> bool|Tile:
        for tile in tiles:
            if tile.pos.position == target.position:
                return tile
        return False
    
    def has_next(self, target : Point, facing : str, remaining_vertices : list[Vertice]) -> bool|Vertice:
        for vertice in remaining_vertices:
            if vertice.facing == facing:
                if vertice.point1.position == target.position or vertice.point2.position == target.position:
                    remaining_vertices.remove(vertice)
                    return vertice
        return False
                        
    