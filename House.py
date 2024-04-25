
from gdpc import Editor, Block, geometry
from list_block import *
import numpy as np

class House:
    def __init__(self, editor, coordinates_min, coordinates_max):
        self.editor = editor
        self.coordinates_min = coordinates_min
        self.coordinates_max = coordinates_max
        self.grid = np.zeros((coordinates_max[0], coordinates_max[2]), dtype=bool)  # Create a grid of zeros (False)

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
                self.grid[x+i,z+j] = True
        self.skeleton.append((x, z, width, depth))
        
        block = ["redstone_block", "gold_block", "diamond_block"]
        
        for _ in range(3):
            print("Rectangle n°", _+1, "en cours de création")
            for a in range(1000):  
                new_width = np.random.randint(width//2, width-2)
                new_depth = np.random.randint(depth//2, depth-2)
                
                new_x = np.random.randint(max(x_min+1, x - new_width), min(x_max-new_width, x + width))
                new_z = np.random.randint(max(z_min+1, z - new_depth), min(z_max-new_depth, z + depth))

                if not np.any(self.grid[new_x:new_x+new_width, new_z:new_z+new_depth]):
                    for i in range(0, new_width):
                        for j in range(0, new_depth):
                            self.editor.placeBlock((new_x + i, y_min, new_z + j), Block(block[_]))
                            self.grid[new_x + i, new_z + j] = True

                    self.skeleton.append((new_x, new_z, new_width, new_depth))
                    break
            else:
                print("Failed to place rectangle after 1000 attempts.")

    def checkOverlap(self, x, z, width, depth):
        for skeleton in self.skeleton:
            x_skeleton, z_skeleton, width_skeleton, depth_skeleton = skeleton
            if x < x_skeleton + width_skeleton and x + width > x_skeleton and z < z_skeleton + depth_skeleton and z + depth > z_skeleton:
                return True
        
        return False
    
    def delete(self):
        for x in range(self.coordinates_min[0], self.coordinates_max[0]):
            for y in range(self.coordinates_min[1], self.coordinates_max[1]):
                for z in range(self.coordinates_min[2], self.coordinates_max[2]):
                    self.editor.placeBlock((x, y, z), Block("air"))
    

if __name__ == "__main__":
    editor = Editor(buffering=True)
    buildArea = editor.getBuildArea()    
    coordinates_min = [min(buildArea.begin[i], buildArea.last[i]) for i in range(3)]
    coordinates_max = [max(buildArea.begin[i], buildArea.last[i]) for i in range(3)] 
    
    house = House(editor, coordinates_min, coordinates_max)
    house.createHouseSkeleton()
    
    

   # delete(editor, coordinates_min, coordinates_max)
    editor.flushBuffer()
    
    
    
    