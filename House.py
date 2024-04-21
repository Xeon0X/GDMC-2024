from gdpc import Editor, Block, geometry
import networks.curve as curve
import numpy as np


class House :
    def __init__(self, editor,startX, startY, startZ, endX, endY, endZ):
        self.editor = editor
        self.startX = startX
        self.startY = startY
        self.startZ = startZ
        self.endX = endX
        self.endY = endY
        self.endZ = endZ
       
    
    def placeGround(self):
        for x in range(self.startX, self.endX):
            for z in range(self.startZ, self.endZ):
                self.editor.placeBlock((x, self.startY, z), Block("stone"))
                
    def placeWall(self):
        for x in range(self.startX, self.endX+1):
            for y in range(self.startY, self.endY):
                self.editor.placeBlock((x, y, self.startZ), Block("oak_planks"))
                self.editor.placeBlock((x, y, self.endZ), Block("oak_planks"))
        for z in range(self.startZ, self.endZ+1):
            for y in range(self.startY, self.endY):
                self.editor.placeBlock((self.startX, y, z), Block("oak_planks"))
                self.editor.placeBlock((self.endX, y, z), Block("oak_planks"))
    
    def placeRoof(self):
        for x in range(self.startX, self.endX+1):
            for z in range(self.startZ, self.endZ+1):
                self.editor.placeBlock((x, self.endY, z), Block("stone"))
                
    def placeDoor(self,direction="north"):
        if direction == "north":
            x = (self.startX + self.endX) // 2
            self.editor.placeBlock((x, self.startY, self.startZ), Block("air"))
            self.editor.placeBlock((x, self.startY+1, self.startZ), Block("air"))
            self.editor.placeBlock((x, self.startY+2, self.startZ), Block("air"))
        elif direction == "south":
            x = (self.startX + self.endX) // 2
            self.editor.placeBlock((x, self.startY, self.endZ), Block("air"))
            self.editor.placeBlock((x, self.startY+1, self.endZ), Block("air"))
            self.editor.placeBlock((x, self.startY+2, self.endZ), Block("air"))
        elif direction == "west":
            z = (self.startZ + self.endZ) // 2
            self.editor.placeBlock((self.startX, self.startY, z), Block("air"))
            self.editor.placeBlock((self.startX, self.startY+1, z), Block("air"))
            self.editor.placeBlock((self.startX, self.startY+2, z), Block("air"))
        elif direction == "east":
            z = (self.startZ + self.endZ) // 2
            self.editor.placeBlock((self.endX, self.startY, z), Block("air"))
            self.editor.placeBlock((self.endX, self.startY+1, z), Block("air"))
            self.editor.placeBlock((self.endX, self.startY+2, z), Block("air"))
 
    def placeHouse(self):
        self.clearInside()
        self.placeGround()
        self.placeWall()
        self.placeRoof()
        self.placeDoor()
    
    def clearInside(self):
        for x in range(self.startX+1, self.endX):
            for y in range(self.startY+1, self.endY):
                for z in range(self.startZ+1, self.endZ):
                    self.editor.placeBlock((x, y, z), Block("air"))

    def clear(self):
        for x in range(self.startX, self.endX+1):
            for y in range(self.startY, self.endY+1):
                for z in range(self.startZ, self.endZ+1):
                    self.editor.placeBlock((x, y, z), Block("air"))
        
if __name__ == "__main__":
    editor = Editor(buffering=True)
    house = House(editor, 17, -58, 8, 30, -50, 20)
    house.placeHouse()
    #house.clear()
    editor.flushBuffer()
    
    
    
    
    
    
