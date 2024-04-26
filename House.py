
from gdpc import Editor, Block, geometry
from list_block import *
import numpy as np

class House:
    def __init__(self, editor, coordinates_min, coordinates_max):
        self.editor = editor
        self.coordinates_min = coordinates_min
        self.coordinates_max = coordinates_max
        self.grid = np.zeros((coordinates_max[0], coordinates_max[2]), dtype=[('bool', bool), ('int', int)])
        self.skeleton = []
        
    def createHouseSkeleton(self):
        self.delete()
        x_min, y_min, z_min = self.coordinates_min
        x_max, y_max, z_max = self.coordinates_max
        
        for i in range (x_min, x_max):
            for y in range(z_min, z_max):
                if i == x_min or i == x_max - 1 or y == z_min or y == z_max - 1:
                    self.editor.placeBlock((i, y_min, y), Block("oak_planks"))
                    
        
    
        
        perimeter_width = x_max - x_min
        perimeter_depth = z_max - z_min
        

        x = np.random.randint(x_min+1 , x_max-1)  
        z = np.random.randint(z_min+1 , z_max-1 ) 
        
        width = perimeter_width // 2
        depth = perimeter_depth // 2
        
        if x + width-1 > x_max-1:
            x = x_max - width-1
        if z + depth-1 > z_max-1:
            z = z_max - depth-1
        
        for i in range(0, width-1):
            for j in range(0, depth-1):
                self.editor.placeBlock((x + i, y_min, z + j), Block("stone"))
                self.grid[x+i,z+j] = True,1
        self.skeleton.append((x, z, width-1, depth-1))
        print("Coordinates of the corners: ", (x, z), (x, z+depth-1), (x+width-1, z), (x+width-1, z+depth-1))
        
        block = ["redstone_block", "gold_block", "diamond_block"]
        
        for _ in range(3):
            print("Rectangle n°", _+1, "en cours de création")
            corners = [(x-1, z-1), (x-1, z+depth-1), (x+width-1, z-1), (x+width-1, z+depth-1)]
            around_corners = [(x-1, z),(x, z-1), (x-1, z+depth-2),(x, z+depth-1), (x+width-2, z-1),(x+width-1, z), (x+width-1, z+depth-2),(x+width-2, z+depth-1)]
            around_around_corners = [(x-1, z+1), (x+1, z-1), (x-1, z+depth-3), (x+1, z+depth-1), (x+width-3, z-1), (x+width-1, z+1), (x+width-1, z+depth-3), (x+width-3, z+depth-1)]
            
            corners = corners + around_corners + around_around_corners
        
            for a in range(100000):  
                new_width = np.random.randint(5, width-2)
                new_depth = np.random.randint(5, depth-2)
                
                new_x = np.random.randint(max(x_min+1, x - new_width ), min(x_max-new_width - 1, x + width ))
                new_z = np.random.randint(max(z_min+1, z - new_depth), min(z_max-new_depth - 1, z + depth ))

                
                #if  (new_x, new_z) in corners or(new_x+new_width-1, new_z) in corners or (new_x, new_z+new_depth-1) in corners or (new_x+new_width-1, new_z+new_depth-1) in corners:
                 #   continue

                # Check if the majority of the small rectangle is adjacent to the first rectangle
                adjacent_blocks = 0
                for i in range(new_x, new_x + new_width):
                    for j in range(new_z, new_z + new_depth):
                        if self.grid[i-1,j]['bool'] and self.grid[i-1,j]['int']==1  or self.grid[i+1,j]['bool'] and self.grid[i+1,j]['int']==1 or self.grid[i,j-1]['bool'] and self.grid[i,j-1]['int']==1 or self.grid[i,j+1]['bool'] and self.grid[i,j+1]['int']==1:   
                            adjacent_blocks += 1

                if adjacent_blocks < 3:
                    continue

                if not np.any(self.grid[new_x:new_x+new_width, new_z:new_z+new_depth]['bool']):
                    for i in range(0, new_width):
                        for j in range(0, new_depth):
                            self.grid[new_x + i, new_z + j] = True,2

                            if i == 0 or i == new_width-1 or j == 0 or j == new_depth-1:
                                continue
                            else:
                                self.editor.placeBlock((new_x + i, y_min, new_z + j), Block(block[_]))

                    self.skeleton.append((new_x, new_z, new_width, new_depth))
                    break
            else:
                print("Failed to place rectangle after 1000 attempts.")

   
    def delete(self):
        for x in range(self.coordinates_min[0], self.coordinates_max[0]):
            for y in range(self.coordinates_min[1], self.coordinates_max[1]):
                for z in range(self.coordinates_min[2], self.coordinates_max[2]):
                    self.editor.placeBlock((x, y, z), Block("air"))
    
    def putWallOnSkeleton(self):
        for k in range(len(self.skeleton)):
            x, z, width, depth = self.skeleton[k]
            if k!= 0:
                x+=1
                z+=1
                width-=2
                depth-=2
            for i in range(-1, width+1):
                for j in range(-1, depth+1):
                    for y in range(self.coordinates_min[1], self.coordinates_max[1]):
                        if i == -1 or i == width or j == -1 or j == depth:
                            if not (self.grid[x + i, z + j]['bool']) and not (self.grid[x + i, z + j]['int'] == 1) or (self.grid[x + i, z + j]['bool'] and self.grid[x + i, z + j]['int'] == 2):
                                self.editor.placeBlock((x + i, y, z + j), Block("stone"))
                                #print( i, y,  j, self.grid[x + i, z + j]['bool'],self.grid[x + i, z + j]['int'])
    
        
    def getAdjacentWalls(self):
        main_rect = self.skeleton[0] 
        x_main, z_main, width_main, depth_main = main_rect
        adjacent_walls = []
        width_main-=1
        depth_main-=1

        for k in range(1, len(self.skeleton)):  
            x, z, width, depth = self.skeleton[k]
            
            walls = [(x, z, x + width-1, z), (x, z, x, z + depth-1), (x, z + depth-1, x + width-1, z + depth-1), (x + width-1, z, x + width-1, z + depth-1)]
            for wall in walls:
                x1, z1, x2, z2 = wall
                if (x_main <= x1 <= x_main + width_main or x_main <= x2 <= x_main + width_main) and (z_main - 1 == z1 or z_main + depth_main + 1 == z1):
                    # Adjust the wall segment to only include the part that is overlapped by the main rectangle
                    x1 = max(x1, x_main-1)
                    x2 = min(x2, x_main + width_main+1)
                    # If there is more than one adjacent block, add it to the list
                    if  abs(x2 - x1) > 1:
                        adjacent_walls.append((x1, z1, x2, z2))
                elif (z_main <= z1 <= z_main + depth_main or z_main <= z2 <= z_main + depth_main) and (x_main - 1 == x1 or x_main + width_main + 1 == x1):
                    # Adjust the wall segment to only include the part that is overlapped by the main rectangle
                    z1 = max(z1, z_main-1)
                    z2 = min(z2, z_main + depth_main+1)
                    # If there is more than one adjacent block, add it to the list
                    if  abs(z2 - z1) > 1:
                        adjacent_walls.append((x1, z1, x2, z2))

        return adjacent_walls

    def placeDoor(self):
        walls = self.getAdjacentWalls()
        for wall in walls:
            x_min, z_min, x_max, z_max = wall
            if x_min == x_max:
                width = z_max - z_min
                if width % 2 != 0:
                    door_pos = width // 2
                    for y in range(self.coordinates_min[1]+1, self.coordinates_min[1]+3):
                        self.editor.placeBlock((x_min, y, z_min + door_pos), Block("air"))
                        self.editor.placeBlock((x_min, y, z_min + door_pos+1), Block("air"))
                else:
                    door_pos = width // 2 
                    for y in range(self.coordinates_min[1]+1, self.coordinates_min[1]+3):
                        self.editor.placeBlock((x_min, y, z_min + door_pos), Block("air"))
            else:
                width = x_max - x_min
                if width % 2 != 0:
                    door_pos = width // 2
                    for y in range(self.coordinates_min[1]+1, self.coordinates_min[1]+3):
                        self.editor.placeBlock((x_min + door_pos, y, z_min), Block("air"))
                        self.editor.placeBlock((x_min + door_pos+1, y, z_min), Block("air"))

                else:
                    door_pos = width // 2 
                    for y in range(self.coordinates_min[1]+1, self.coordinates_min[1]+3):
                        self.editor.placeBlock((x_min + door_pos, y, z_min), Block("air"))
                                   
if __name__ == "__main__":
    editor = Editor(buffering=True)
    buildArea = editor.getBuildArea()    
    coordinates_min = [min(buildArea.begin[i], buildArea.last[i]) for i in range(3)]
    coordinates_max = [max(buildArea.begin[i], buildArea.last[i]) for i in range(3)] 

    
    for i in range(1):
        house = House(editor, coordinates_min, coordinates_max)
        house.createHouseSkeleton()
        house.putWallOnSkeleton()
        print("House n°", i+1, "created")
        print('-----------------------------------')
        print(house.getAdjacentWalls())
        house.placeDoor()
        new_coordinates_min =(coordinates_max[0] + 10, coordinates_min[1], coordinates_min[2])
        new_coordinates_max = (coordinates_max[0] + 10 +24, coordinates_max[1], coordinates_max[2])
        coordinates_min = new_coordinates_min
        coordinates_max = new_coordinates_max

   # delete(editor, coordinates_min, coordinates_max)
    editor.flushBuffer()
    
    
    
    