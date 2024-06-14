import random as rd
from gdpc import Editor, Block, geometry
from utils.Enums import DIRECTION,COLLUMN_STYLE
from buildings.geometry.Vertice import Vertice
from buildings.Facade import Facade

class Entrance:
    def __init__(self, 
                 rdata, 
                 vertices : list[Vertice], 
                 direction : DIRECTION, 
                 collumn_style : COLLUMN_STYLE):
        self.vertices = self.correct_vertices(vertices)
        self.direction = direction
        self.rdata = rdata
        self.collumn_style = collumn_style
        self.is_centered = self.is_centered()
        self.door_vertice, self.facade = self.get_door_and_facade()
        self.door_width, self.door_height, self.padding, self.ypadding = self.get_door_dimention()
        self.editor, self.materials = None,None
        
    def build(self, editor : Editor, materials : list[str]):
        self.editor = editor
        self.materials = materials
        self.correct_facade()
        with self.editor.pushTransform((0,1,0)):
            self.facade.build(self.editor, self.materials)
            self.build_door()
        
    def build_door(self):
        # self.padding is the padding from the door to the facade, padding is the padding from the door+self.padding to the end of the vertice
        padding = (len(self.door_vertice) - (self.padding*2 + self.door_width // 2)) // 2
        self.door_vertice.fill(self.editor, self.materials[0], 
                               y = self.door_height+self.ypadding, 
                               xpadding = padding, 
                               zpadding = padding)
        # padding is now the padding from the door to the end of the vertice
        padding += self.padding
        self.door_vertice.fill(self.editor, "air",
                               y = self.door_height,
                               xpadding = padding,
                               zpadding = padding)
        
    def correct_facade(self):
        self.facade.has_balcony = False
        
    def correct_vertices(self, vertices : list[Vertice]) -> list[Vertice]:
        for v in vertices:
            v.point2.set_position(y=v.point2.y-1)
        return vertices
        
    def is_centered(self) -> bool:
        return rd.random() <= self.rdata["entrance"]["centered"]
    
    def get_door_and_facade(self) -> tuple[Vertice, Facade]:
        oriented_vertices = self.get_oriented_vertices()
        door_vertice = None
        
        if self.is_centered:
            oriented_vertices.sort(key = lambda v: v.point1.x if self.direction.value % 2 == 0 else v.point1.z) # if direction is north or south, sort by x, else sort by z
            mid = len(oriented_vertices) // 2
            ver1, ver2 = oriented_vertices[mid], oriented_vertices[-mid-1]
            
            if ver1.point1.x != ver2.point1.x and ver1.point1.z != ver2.point1.z:
                door_vertice = rd.choice([ver1, ver2])
            elif ver1.point1.position == ver2.point1.position:
                door_vertice = ver1
            else : 
                door_vertice =  Vertice(ver2.point1.copy(), ver1.point2.copy())
            
        else: 
            door_vertice = rd.choice(oriented_vertices)
        
        facade = Facade(self.rdata["facade"], self.vertices, self.collumn_style)
        return(door_vertice, facade)
        
    def get_oriented_vertices(self) -> list[Vertice]:
        # Get all the vertice that can contain the door
        
        # if direction is north or south, compare by x, else compare by z
        compare  = lambda v: (v.point1.z,v.point1.x) if self.direction.value % 2 == 0 else (v.point1.x,v.point1.z) 
        # if direction is north or west, the most off_centered is the maximum, else it is the minimum
        off_centered = lambda p1,p2: max(p1,p2) if self.direction == DIRECTION.NORTH or self.direction == DIRECTION.WEST else min(p1,p2) 
        
        oriented_vertices = []
        for v in self.vertices:
            if v.facing != self.direction: continue
            sortby,position = compare(v)
            alreadyset = False
            for ov in oriented_vertices:
                ov_sorted, ov_position = compare(ov)
                if position == ov_position:
                    if off_centered(sortby,ov_sorted) == sortby: oriented_vertices.remove(ov)
                    else: alreadyset = True
            if not alreadyset: oriented_vertices.append(v)
                    
        return oriented_vertices
    
    def get_door_dimention(self) -> tuple[int,int,int,int]: # return width, height, padding, ypadding
        max_width = len(self.door_vertice) - 2
        max_height = self.door_vertice.get_height() - 1
        
        door_width = rd.randint(self.rdata["entrance"]["door"]["size"]["min_width"], self.rdata["entrance"]["door"]["size"]["max_width"])
        door_height = rd.randint(self.rdata["entrance"]["door"]["size"]["min_height"], self.rdata["entrance"]["door"]["size"]["max_height"])
        xpadding = rd.randint(1, self.rdata["entrance"]["door"]["padding"]["max"])
        ypadding = rd.randint(1, self.rdata["entrance"]["door"]["padding"]["max_top"])
        
        if door_width > max_width: door_width = max_width
        if door_height > max_height: door_height = max_height
        if xpadding*2 + door_width > max_width: xpadding += (max_width - (xpadding*2 + door_width)-1)//2
        if ypadding + door_height > max_height: ypadding += max_height - (ypadding + door_height)
        
        return door_width,door_height,xpadding,ypadding
        