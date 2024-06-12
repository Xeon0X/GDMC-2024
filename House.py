
from time import sleep
from gdpc import Editor, Block, geometry
from list_block import *
import numpy as np
from skimage.morphology import skeletonize
import math
import matplotlib.pyplot as plt

class House:
    def __init__(self, editor, coordinates_min, coordinates_max, direction):
        self.editor = editor
        self.coordinates_min = coordinates_min
        self.coordinates_max = coordinates_max
        self.grid = np.zeros((coordinates_max[0], coordinates_max[2]), dtype=[('bool', bool), ('int', int)])
        self.skeleton = []
        
        size = [(coordinates_max[i] - coordinates_min[i]) + 10 for i in range(3)]

        self.grid3d = np.zeros(size, dtype=[('bool', bool), ('int', int)])
        
        self.nbEtage = (coordinates_max[1] - coordinates_min[1]) // 5
        
        self.direction = direction
        
        
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
        
        x_min += 1
        z_min += 1
        x_max -= 1
        z_max -= 1
        x = np.random.randint(x_min+1 , x_max-1)  
        z = np.random.randint(z_min+1 , z_max-1 ) 
        
        width = perimeter_width // 2
        depth = perimeter_depth // 2
        height = y_max - y_min
        
        if x + width-1 > x_max-1:
            x = x_max - width-1
        if z + depth-1 > z_max-1:
            z = z_max - depth-1
            
        x_plan3d = x - x_min
        z_plan3d = z - z_min
        
        for i in range(0, width-1):
            for j in range(0, depth-1):
                self.editor.placeBlock((x + i, y_min, z + j), Block("stone"))
                self.grid[x+i,z+j] = True,1
                self.grid3d[x_plan3d+i,0,z_plan3d+j] = True,1
        self.skeleton.append((x, z, width-1, depth-1, height))
        print("Coordinates of the corners: ", (x, z), (x, z+depth-1), (x+width-1, z), (x+width-1, z+depth-1))
        
        block = ["redstone_block", "gold_block", "diamond_block"]
        
        x_min -= 1
        x_max -= 1
        z_min += 1
        z_max += 1
        
        for _ in range(3):
            print("Rectangle n°", _+1, "en cours de création")
            
        
            for a in range(100000):  
                new_width = np.random.randint(5, width-2)
                new_depth = np.random.randint(5, depth-2)
                
                new_x = np.random.randint(max(x_min+1, x - new_width ), min(x_max-new_width - 1, x + width ))
                new_z = np.random.randint(max(z_min+1, z - new_depth), min(z_max-new_depth - 1, z + depth ))

                
                
                adjacent_blocks = 0
                for i in range(new_x, new_x + new_width):
                    for j in range(new_z, new_z + new_depth):
                        if self.grid[i-1,j]['bool'] and self.grid[i-1,j]['int']==1  or self.grid[i+1,j]['bool'] and self.grid[i+1,j]['int']==1 or self.grid[i,j-1]['bool'] and self.grid[i,j-1]['int']==1 or self.grid[i,j+1]['bool'] and self.grid[i,j+1]['int']==1:   
                            adjacent_blocks += 1

                if adjacent_blocks < 3:
                    continue

                if not np.any(self.grid[new_x:new_x+new_width, new_z:new_z+new_depth]['bool']):
                    new_x_plan3d = new_x - x_min
                    new_z_plan3d = new_z - z_min
                    for i in range(0, new_width):
                        for j in range(0, new_depth):
                            self.grid[new_x + i, new_z + j] = True,2
                            self.grid3d[new_x_plan3d + i,0, new_z_plan3d + j] = True,2

                            if i == 0 or i == new_width-1 or j == 0 or j == new_depth-1:
                                continue
                            else:
                                self.editor.placeBlock((new_x + i, y_min, new_z + j), Block(block[_]))

                    self.skeleton.append((new_x, new_z, new_width, new_depth, height))
                    break
            else:
                print("Failed to place rectangle after 1000 attempts.")

   
    def delete(self):
        for x in range(self.coordinates_min[0], self.coordinates_max[0]):
            for y in range(self.coordinates_min[1], self.coordinates_max[1]+10):
                for z in range(self.coordinates_min[2], self.coordinates_max[2]):
                    self.editor.placeBlock((x, y, z), Block("air"))
    
    def putWallOnSkeleton(self):
        for k in range(len(self.skeleton)):
            x, z, width, depth, height = self.skeleton[k]
            
           
            if k!= 0:
                x+=1
                z+=1
                width-=2
                depth-=2
            x_plan3d = x - self.coordinates_min[0]
            z_plan3d = z - self.coordinates_min[2]
            for i in range(-1, width+1):
                for j in range(-1, depth+1):
                    for y in range(0, height):
                        if i == -1 or i == width or j == -1 or j == depth:
                            if not (self.grid[x + i, z + j]['bool']) and not (self.grid[x + i, z + j]['int'] == 1) or (self.grid[x + i, z + j]['bool'] and self.grid[x + i, z + j]['int'] == 2):
                                self.editor.placeBlock((x + i, self.coordinates_min[1] + y, z + j), Block("stone"))
                                self.grid3d[ x_plan3d+i, y, z_plan3d+j] = True
                                #print( i, y,  j, self.grid[x + i, z + j]['bool'],self.grid[x + i, z + j]['int'])
    
        
    def getAdjacentWalls(self):

        main_rect = self.skeleton[0] 
        x_main, z_main, width_main, depth_main, heigt_main = main_rect
        adjacent_walls = []
        width_main-=1
        depth_main-=1

        for k in range(1, len(self.skeleton)):  
            x, z, width, depth, heigt = self.skeleton[k]
            
            
            walls = [(x, z, x + width-1, z), (x, z, x, z + depth-1), (x, z + depth-1, x + width-1, z + depth-1), (x + width-1, z, x + width-1, z + depth-1)]
            for wall in walls:
                x1, z1, x2, z2 = wall
                if (x_main <= x1 <= x_main + width_main or x_main <= x2 <= x_main + width_main) and (z_main - 1 == z1 or z_main + depth_main + 1 == z1):
                    x1 = max(x1, x_main-1)
                    x2 = min(x2, x_main + width_main+1)
                    if  abs(x2 - x1) > 1:
                        adjacent_walls.append((x1, z1, x2, z2))
                elif (z_main <= z1 <= z_main + depth_main or z_main <= z2 <= z_main + depth_main) and (x_main - 1 == x1 or x_main + width_main + 1 == x1):
                    z1 = max(z1, z_main-1)
                    z2 = min(z2, z_main + depth_main+1)
                    if  abs(z2 - z1) > 1:
                        adjacent_walls.append((x1, z1, x2, z2))

        return adjacent_walls

      
    
        
    def placeDoor(self):
        walls = self.getAdjacentWalls()
        for wall in walls:
            for i in range(self.nbEtage):
                x_min, z_min, x_max, z_max = wall
                if x_min == x_max:
                    width = z_max - z_min
                    if width % 2 != 0:
                        door_pos = width // 2
                        for y in range(self.coordinates_min[1]+1+i*4, self.coordinates_min[1]+3+i*4):
                            self.editor.placeBlock((x_min, y, z_min + door_pos), Block("air"))
                            self.editor.placeBlock((x_min, y, z_min + door_pos+1), Block("air"))
                    else:
                        door_pos = width // 2 
                        for y in range(self.coordinates_min[1]+1+i*4 , self.coordinates_min[1]+3+i*4):
                            self.editor.placeBlock((x_min, y, z_min + door_pos), Block("air"))
                else:
                    width = x_max - x_min
                    if width % 2 != 0:
                        door_pos = width // 2
                        for y in range(self.coordinates_min[1]+1+i*4, self.coordinates_min[1]+3+i*4):
                            self.editor.placeBlock((x_min + door_pos, y, z_min), Block("air"))
                            self.editor.placeBlock((x_min + door_pos+1, y, z_min), Block("air"))

                    else:
                        door_pos = width // 2 
                        for y in range(self.coordinates_min[1]+1+i*4, self.coordinates_min[1]+3+i*4):
                            self.editor.placeBlock((x_min + door_pos, y, z_min), Block("air"))
           
    def placeRoof(self):
        for k in range(len(self.skeleton)-1, -1, -1):
            x, z, width, depth, height = self.skeleton[k]
            
            
            
            if k!= 0:
                x+=1
                z+=1
                width-=2
                depth-=2
                if width < depth:
                    if width <=5:
                        n = 1
                    elif width <=10:
                        n = 2
                    else:
                        n = 3
                else:
                    if depth <=5:
                        n = 1
                    elif depth <=10:
                        n = 2
                    else:
                        n = 3
            else:
            
                if width < depth:
                    n = width // 4
                else:
                    n = depth // 4
            
                
            x_plan3d = x - self.coordinates_min[0]
            z_plan3d = z - self.coordinates_min[2]
            
            print(width, depth, n)
            
            if width < depth:
                if n==1:
                    for i in range(-1,depth+1):
                        self.editor.placeBlock((x+width//2, self.coordinates_max[1], z+i), Block("blackstone"))
                else:
                    for k in range(n):
                        for i in range(-1, width+1):
                            for y in range(-1, depth//2+1):
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+k, z+y+k+2), Block("blackstone"))
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+k, z+depth-y-3-k), Block("blackstone"))
            else:
                if n==1:
                    for i in range(-1,width+1):
                        self.editor.placeBlock((x+i, self.coordinates_max[1], z+depth//2), Block("blackstone"))
                else:
                    for k in range(n-1):
                        for i in range(-1, width+1):
                            for y in range(-1, depth//2+1):
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+k, z+y+k+2), Block("blackstone"))
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+k, z+depth-y-3-k), Block("blackstone"))
            
            
            print('-----------------------------------')
           
            for i in range(-1, width+1):
                for j in range(-1, depth+1):
                    if width<depth:
                        if width%2 != 0:
                            if (i == width//2 ):
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+n, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j] = True
                                if j== -1 :
                                    if not self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j-1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+n, z + j-1), Block("quartz_slab",{"type":"bottom"}))
                                        self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j-1] = True
                                    if not self.grid3d[ x_plan3d+i, height+n-1,  z_plan3d+j-1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+n-1, z + j-1), Block("quartz_slab",{"type":"top"}))
                                        self.grid3d[ x_plan3d+i, height+n-1,  z_plan3d+j-1] = True

                                elif j == depth:
                                    if not self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j+1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+n, z + j+1), Block("quartz_slab",{"type":"bottom"}))
                                        self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j+1] = True
                                    if not self.grid3d[ x_plan3d+i, height+n-1,  z_plan3d+j+1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+n-1, z + j+1), Block("quartz_slab",{"type":"top"}))
                                        self.grid3d[ x_plan3d+i, height+n-1,  z_plan3d+j+1] = True
                                
                    else:
                        if depth%2 != 0:
                            if (j == depth//2 ):
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+n, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                self.grid3d[ x_plan3d+i, height+n,  z_plan3d+j] = True
                                if i== -1 :
                                    if not self.grid3d[ x_plan3d+i-1, height+n,  z_plan3d+j]:
                                        self.editor.placeBlock((x + i-1, self.coordinates_max[1]+n, z + j), Block("quartz_slab",{"type":"bottom"}))
                                        self.grid3d[ x_plan3d+i-1, height+n,  z_plan3d+j] = True
                                    if not self.grid3d[ x_plan3d+i-1, height+n-1,  z_plan3d+j]:
                                        self.editor.placeBlock((x + i-1, self.coordinates_max[1]+n-1, z + j), Block("quartz_slab",{"type":"top"}))
                                        self.grid3d[ x_plan3d+i-1, height+n-1,  z_plan3d+j] = True
                                    
                                elif i == width:
                                    if not self.grid3d[ x_plan3d+i+1, height+n,  z_plan3d+j]:
                                        self.editor.placeBlock((x + i+1, self.coordinates_max[1]+n, z + j), Block("quartz_slab",{"type":"bottom"}))
                                        self.grid3d[ x_plan3d+i+1, height+n,  z_plan3d+j] = True
                                    if not self.grid3d[ x_plan3d+i+1, height+n-1,  z_plan3d+j]:
                                        self.editor.placeBlock((x + i+1, self.coordinates_max[1]+n-1, z + j), Block("quartz_slab",{"type":"top"}))
                                        self.grid3d[ x_plan3d+i+1, height+n-1,  z_plan3d+j] = True
                                
            if width<depth:
                
                    h = 0
                    for i in range(-1, width//2):
                        for j in range(-1, depth+1):
                            if i != -1:
                                if h % 1 == 0:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"top"}))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"top"}))
                                    self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j] = True 
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j] = True
                                   
                                    if j == -1 :
                                        
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j -1), Block("quartz_block"))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j -1), Block("quartz_block"))
                                        self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j-1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j-1] = True
                                    elif j == depth:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j +1), Block("quartz_block"))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j +1), Block("quartz_block"))
                                        self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j+1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j+1] = True
                                else:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h-0.5, z + j), Block("blackstone"))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-0.5, z + j), Block("blackstone"))
                                    
                                    self.grid3d[ x_plan3d+ i, round(height+h+0.5),  z_plan3d+ j] = True
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h+0.5),  z_plan3d+ j] = True
                                    self.grid3d[ x_plan3d+ i, round(height+h-0.5),  z_plan3d+ j] = True
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h-0.5),  z_plan3d+ j] = True
                                    
                                    if j == -1 :
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j -1), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j -1), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h-1, z + j -1), Block("quartz_slab", {"type": "top"}))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-1, z + j -1), Block("quartz_slab", {"type": "top"}))
                                        
                                        self.grid3d[ x_plan3d+ i, round(height+h-1),  z_plan3d+ j-1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h-1),  z_plan3d+ j-1] = True
                                        self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j-1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j-1] = True
                                    elif j == depth:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j +1), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j +1), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h-1, z + j +1), Block("quartz_slab", {"type": "top"}))
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-1, z + j +1), Block("quartz_slab", {"type": "top"}))
                                        
                                        self.grid3d[ x_plan3d+ i, round(height+h-1),  z_plan3d+ j+1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h-1),  z_plan3d+ j+1] = True
                                        self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j+1] = True
                                        self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j+1] = True
                            else:  
                                self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"bottom"}))
                                self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j), Block("blackstone_slab",{"type":"bottom"})) 
                                
                                self.grid3d[ x_plan3d+ i, round(height+h),  z_plan3d+ j] = True
                                self.grid3d[ x_plan3d+ width-1-i, round(height+h),  z_plan3d+ j] = True

                                if j == -1 :
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j -1), Block("quartz_slab", {"type": "bottom"}))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j -1), Block("quartz_slab", {"type": "bottom"}))
                                    if not self.grid3d[ x_plan3d+i, height+h-1,  z_plan3d+j-1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h-1, z + j -1), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ x_plan3d+i, height+h-1,  z_plan3d+j-1] = True
                                    if not self.grid3d[ x_plan3d+width-1-i, height+h-1,  z_plan3d+j-1]:
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-1, z + j -1), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ x_plan3d+width-1-i, height+h-1,  z_plan3d+j-1] = True
                                    
                                    self.grid3d[ x_plan3d+ i, round(height+h-1),  z_plan3d+ j-1] = True
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h-1),  z_plan3d+ j-1] = True
                                elif j == depth:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]+h, z + j +1), Block("quartz_slab", {"type": "bottom"}))
                                    self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h, z + j +1), Block("quartz_slab", {"type": "bottom"}))
                                    if not self.grid3d[ x_plan3d+i, height+h-1,  z_plan3d+j+1]:
                                        self.editor.placeBlock((x + i, self.coordinates_max[1]+h-1, z + j +1), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ x_plan3d+i, height+h-1,  z_plan3d+j+1] = True
                                    if not self.grid3d[ x_plan3d+width-1-i, height+h-1,  z_plan3d+j+1]:
                                        self.editor.placeBlock((x + width-1-i, self.coordinates_max[1]+h-1, z + j +1), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ x_plan3d+width-1-i, height+h-1,  z_plan3d+j+1] = True
                                    
                                    self.grid3d[ x_plan3d+ i, round(height+h-1),  z_plan3d+ j+1] = True 
                                    self.grid3d[ x_plan3d+ width-1-i, round(height+h-1),  z_plan3d+ j+1] = True
                        if i != -1:
                            h += 0.5
            else:
            
                    h = 0
                    for i in range(-1, depth//2):
                        for j in range(-1, width+1):
                            if i != -1:
                                if h % 1 == 0:  
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + i), Block("blackstone_slab",{"type":"top"}))
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + depth-1-i), Block("blackstone_slab",{"type":"top"}))
                                    
                                    self.grid3d[ x_plan3d+j, round(height+h), z_plan3d+ i] = True
                                    self.grid3d[ x_plan3d+j, round(height+h), z_plan3d+ depth-1-i] = True
                                    
                                    if j == -1 :
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + i ), Block("quartz_block"))
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_block"))
                                        
                                        self.grid3d[ x_plan3d+j-1, round(height+h), z_plan3d+ i] = True
                                        self.grid3d[ x_plan3d+j-1, round(height+h), z_plan3d+ depth-1-i] = True
                                    elif j == width:
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + i ), Block("quartz_block"))
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_block"))
                                        
                                        self.grid3d[ x_plan3d+j+1, round(height+h), z_plan3d+ i] = True
                                        self.grid3d[ x_plan3d+j+1, round(height+h), z_plan3d+ depth-1-i] = True
                                    
                                else:  
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + i), Block("blackstone_slab",{"type":"bottom"}))
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + depth-1-i), Block("blackstone_slab",{"type":"bottom"}))
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h-0.5, z + i), Block("blackstone"))
                                    self.editor.placeBlock((x + j, self.coordinates_max[1]+h-0.5, z + depth-1-i), Block("blackstone"))
                                    
                                    self.grid3d[ j, round(height+h+0.5),  i] = True
                                    self.grid3d[ j, round(height+h+0.5),  depth-1-i] = True
                                    self.grid3d[ j, round(height+h-0.5),  i] = True
                                    self.grid3d[ j, round(height+h-0.5),  depth-1-i] = True
                                
                                    if j == -1 :
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + i ), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h-1, z + i ), Block("quartz_slab", {"type": "top"}))
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h-1, z + depth-1-i ), Block("quartz_slab", {"type": "top"}))
                                        
                                        self.grid3d[ j, round(height+h),  i] = True
                                        self.grid3d[ j, round(height+h),  depth-1-i] = True
                                        self.grid3d[ j, round(height+h-1),  i] = True
                                        self.grid3d[ j, round(height+h-1),  depth-1-i] = True
                                    elif j == width:
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + i ), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_slab", {"type": "bottom"}))
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h-1, z + i ), Block("quartz_slab", {"type": "top"}))
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h-1, z + depth-1-i ), Block("quartz_slab", {"type": "top"}))
                                        
                                        self.grid3d[ j, round(height+h),  i] = True
                                        self.grid3d[ j, round(height+h),  depth-1-i] = True
                                        self.grid3d[ j, round(height+h-1),  i] = True
                                        self.grid3d[ j, round(height+h-1),  depth-1-i] = True
                            else:   
                                self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + i), Block("blackstone_slab",{"type":"bottom"}))
                                self.editor.placeBlock((x + j, self.coordinates_max[1]+h, z + depth-1-i), Block("blackstone_slab",{"type":"bottom"}))
                                
                                self.grid3d[ j, round(height+h),  i] = True
                                self.grid3d[ j, round(height+h),  depth-1-i] = True
                                
                                if j == -1 :
                                    self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + i ), Block("quartz_slab", {"type": "bottom"}))
                                    self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_slab", {"type": "bottom"}))
                                    if not self.grid3d[ j, height+h-1,  i]:
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h-1, z + i ), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ j, height+h-1,  i] = True
                                    if not self.grid3d[ j, height+h-1,  depth-1-i]:
                                        self.editor.placeBlock((x + j -1, self.coordinates_max[1]+h-1, z + depth-1-i ), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ j, height+h-1,  depth-1-i] = True
                                    
                                    self.grid3d[ j, round(height+h),  i] = True
                                    self.grid3d[ j, round(height+h),  depth-1-i] = True
                                elif j == width:
                                    self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + i ), Block("quartz_slab", {"type": "bottom"}))
                                    self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h, z + depth-1-i ), Block("quartz_slab", {"type": "bottom"}))
                                    if not self.grid3d[ j, height+h-1,  i]:
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h-1, z + i ), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ j, height+h-1,  i] = True
                                    if not self.grid3d[ j, height+h-1,  depth-1-i]:
                                        self.editor.placeBlock((x + j +1, self.coordinates_max[1]+h-1, z + depth-1-i ), Block("quartz_slab", {"type": "top"}))
                                        self.grid3d[ j, height+h-1,  depth-1-i] = True
                                    
                                    self.grid3d[ j, round(height+h),  i] = True
                                    self.grid3d[ j, round(height+h),  depth-1-i] = True
                                    
                                    
                                self.grid3d[ j, round(height+h),  i] = True
                                self.grid3d[ j, round(height+h),  depth-1-i] = True
                            
                       
                        if i != -1:
                            h += 0.5
            
            QUARTZ_SLAB = Block("quartz_slab", {"type": "top"})
           
            
            for i in range(-2, width+2):
                for j in range(-2, depth+2):
                    if i == -2 or i == width+1 or j == -2 or j == depth+1:
                        if not self.grid3d[x_plan3d+i, height-1,  z_plan3d+j]['bool']:
                            if width<depth:
                                if i == -2 or i == width+1:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]-1, z + j), QUARTZ_SLAB)
                                
                            else:
                                if j == -2 or j == depth+1:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1]-1, z + j), QUARTZ_SLAB)
                                

            
        
    def putCelling(self):
        for k in range(0, len(self.skeleton)):
            x, z, width, depth, height = self.skeleton[k]
            
            if k!= 0:
                x+=1
                z+=1
                width-=2
                depth-=2
            x_plan3d = x - self.coordinates_min[0]
            z_plan3d = z - self.coordinates_min[2]
            for y in range(1,self.nbEtage+1):
                for i in range(0, width):
                    for j in range(0, depth):
                            self.editor.placeBlock((x + i, self.coordinates_min[1] +4*y, z + j), Block("quartz_block"))    
                            self.grid3d[ x_plan3d+i, 4*y, z_plan3d+j] = True
             

    def placeWindow(self):
        pass

    def placeStairs(self):
        pass

    
    def WallFacingDirection(self):
        
        if self.direction == "N":
            closest_wall = min(self.skeleton, key=lambda wall: wall[1])
            wall = (closest_wall[0], closest_wall[1], closest_wall[0] + closest_wall[2], closest_wall[1])
        elif self.direction == "S":
            closest_wall = max(self.skeleton, key=lambda wall: wall[1] + wall[3])
            wall = (closest_wall[0], closest_wall[1] + closest_wall[3], closest_wall[0] + closest_wall[2], closest_wall[1] + closest_wall[3])
        elif self.direction == "E":
            closest_wall = max(self.skeleton, key=lambda wall: wall[0] + wall[2])
            wall = (closest_wall[0] + closest_wall[2], closest_wall[1], closest_wall[0] + closest_wall[2], closest_wall[1] + closest_wall[3])
        elif self.direction == "W":
            closest_wall = min(self.skeleton, key=lambda wall: wall[0])
            wall = (closest_wall[0], closest_wall[1], closest_wall[0], closest_wall[1] + closest_wall[3])
        else:
            return []
        
        if wall != self.skeleton[0]:
     
            wall = (wall[0]+1, wall[1]+1,  wall[2]-2,  wall[3]-2)
             
        return wall
    

    def placeEntrance(self):
        wall = self.WallFacingDirection()
        
        match self.direction:
            case "N":
                if (wall[2] - wall[0]) % 2 != 0:
                    self.editor.placeBlock(((wall[0] + wall[2]) // 2 +1, self.coordinates_min[1]+1, wall[1]-1), Block("air"))
                    self.editor.placeBlock(((wall[0] + wall[2]) // 2 +1, self.coordinates_min[1]+2, wall[1]-1), Block("air"))
                    print((wall[0] + wall[2]) // 2, self.coordinates_min[1]+1, wall[1])
                self.editor.placeBlock(((wall[0] + wall[2]) // 2, self.coordinates_min[1]+1, wall[1]-1), Block("air"))                
                self.editor.placeBlock(((wall[0] + wall[2]) // 2, self.coordinates_min[1]+2, wall[1]-1), Block("air"))
                print((wall[0] + wall[2]) // 2, self.coordinates_min[1]+1, wall[1]+1)
            case "S":
                pass
            case "E":
                pass
            case "W":
                pass
            case _:
                pass
    
if __name__ == "__main__":
    editor = Editor(buffering=True)
    buildArea = editor.getBuildArea()    
    coordinates_min = [min(buildArea.begin[i], buildArea.last[i]) for i in range(3)]
    coordinates_max = [max(buildArea.begin[i], buildArea.last[i]) for i in range(3)] 

    
    for i in range(1):
        house = House(editor, coordinates_min, coordinates_max,"N")
        
        house.createHouseSkeleton()
        house.putWallOnSkeleton()
        print("House n°", i+1, "created")
        print('-----------------------------------')
        print(house.getAdjacentWalls())
        house.placeDoor()
        house.placeRoof()
        house.putCelling()
        house.placeEntrance()
      
        new_coordinates_min =(coordinates_max[0] + 10, coordinates_min[1], coordinates_min[2])
        new_coordinates_max = (coordinates_max[0] + 10 +24, coordinates_max[1], coordinates_max[2])
        coordinates_min = new_coordinates_min
        coordinates_max = new_coordinates_max

   # delete(editor, coordinates_min, coordinates_max)
    editor.flushBuffer()
    
    
    
    