from gdpc import Editor, Block, geometry
from list_block import *
import numpy as np
import math


class House :
    def __init__(self, editor,startX, startY, startZ, endX, endY, endZ,style,houseDirection="north"):
        self.editor = editor
        self.startX = startX
        self.startY = startY
        self.startZ = startZ
        self.endX = endX
        self.endY = endY
        self.endZ = endZ
        self.houseDirection = houseDirection
        self.hasGarder = True
        self.gardenSide = "right"
        self.hasGarage = True
        
        self.wall = style['mur']
        self.ground = style['sol']
        self.grass = style['grass']
        self.path = style['chemin']
        self.fence = style['fence']
        self.glass = style['glass']
        self.door = style['door']
        self.roof = style['toit']
        
    def placeGround(self,CoStart, CoEnd,block):
        for x in range(CoStart[0], CoEnd[0]):
            for z in range(CoStart[2], CoEnd[2]):
                self.editor.placeBlock((x, CoStart[1], z), Block(block) )
                
    def placeRoof(self,CoStart,CoEnd):
        for x in range(CoStart[0], CoEnd[0]):
            for z in range(CoStart[2], CoEnd[2]):
                self.editor.placeBlock((x, CoEnd[1]-1, z), Block(self.roof))
                
                
    def placeWall(self,CoStart,CoEnd):
        if CoStart[0] == CoEnd[0]:
            for y in range(CoStart[1]+1, CoEnd[1]-1):
                for z in range(CoStart[2], CoEnd[2]):
                    self.editor.placeBlock((CoStart[0], y, z), Block(self.wall))
            CoStart = (CoStart[0],CoStart[1],CoStart[2]+1)
            CoEnd = (CoEnd[0],CoEnd[1],CoEnd[2]-1)
        elif CoStart[2] == CoEnd[2]:
            for y in range(CoStart[1]+1, CoEnd[1]-1):
                for x in range(CoStart[0], CoEnd[0]):
                    self.editor.placeBlock((x, y, CoStart[2]), Block(self.wall))
            CoStart = (CoStart[0]+1,CoStart[1],CoStart[2])
            CoEnd = (CoEnd[0]-1,CoEnd[1],CoEnd[2])
                    
        self.placeWindow(CoStart,CoEnd)
        
                    
       
    
    def placeDoor(self, direction="north", x=0, z=0, y=0):   
        door_directions = {
            "south": {"facing": "north", "half": "lower"},
            "north": {"facing": "south", "half": "lower"},
            "east": {"facing": "west", "half": "lower"},
            "west": {"facing": "east", "half": "lower"}
        }
        
        door_properties = door_directions.get(direction)
        
        if door_properties:
            self.editor.placeBlock((x, y + 1, z), Block(self.door, door_properties))
            self.editor.placeBlock((x, y + 2, z), Block(self.door, {"facing": door_properties["facing"], "half": "upper"}))
            self.doorDirection = direction
        
    def placeWindow(self, CoStart, CoEnd):
        x = abs(CoEnd[0] - CoStart[0])
        z = abs(CoEnd[2] - CoStart[2])
        type = Block(self.glass)
        
        def placeBlock(axis, is_x_axis):
            print(axis, is_x_axis)
            if axis % 2 == 0:
                if axis == 4:
                    if is_x_axis:
                        self.editor.placeBlock((CoStart[0] + 1, CoStart[1] + 2, CoStart[2]), type)
                        self.editor.placeBlock((CoStart[0] + 2, CoStart[1] + 2, CoStart[2]), type)
                    else:
                        self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + 1), type)
                        self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + 2), type)
                else:
                    for i in range(axis // 2):
                        if i % 2 == 0:
                            if is_x_axis:
                                self.editor.placeBlock((CoStart[0] + i * 2 + 1, CoStart[1] + 2, CoStart[2]), type)
                                self.editor.placeBlock((CoStart[0] + i * 2 + 2, CoStart[1] + 2, CoStart[2]), type)
                            else:
                                self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + 1 + i * 2), type)
                                self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + i * 2 + 2), type)
            else:
                if axis <= 5:
                    for i in range(axis):
                        if is_x_axis:
                            self.editor.placeBlock((CoStart[0] + i, CoStart[1] + 2, CoStart[2]), type)
                        else:
                            self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + i), type)
                else:
                    for i in range(axis // 3):
                        if 3 * (i + 1) + i > abs(CoEnd[2] - CoStart[2]):
                            break
                        else:
                            if is_x_axis:
                                self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + i * 4), type)
                                self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + i * 4 + 1), type)
                                self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + i * 4 + 2), type)
                            else:
                                self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + i * 4), type)
                                self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + i * 4 + 1), type)
                                self.editor.placeBlock((CoStart[0], CoStart[1] + 2, CoStart[2] + i * 4 + 2), type)

        if CoStart[0] == CoEnd[0]:
            placeBlock(z, False)

        if CoStart[2] == CoEnd[2]:
            placeBlock(x, True)



    def clearInside(self):
            for x in range(self.startX+1, self.endX):
                for y in range(self.startY+1, self.endY):
                    for z in range(self.startZ+1, self.endZ):
                        self.editor.placeBlock((x, y, z), air)
                
                
    def deleteWall(self,CoStart,CoEnd):
        if CoStart[0] == CoEnd[0]:
            for y in range(CoStart[1]+1, CoEnd[1]-1):
                for z in range(CoStart[2], CoEnd[2]):
                    self.editor.placeBlock((CoStart[0], y, z), air)
        elif CoStart[2] == CoEnd[2]:
            for y in range(CoStart[1]+1, CoEnd[1]-1):
                for x in range(CoStart[0], CoEnd[0]):
                    self.editor.placeBlock((x, y, CoStart[2]), air)
                    
                                
    def placeGarage(self,CoStart,CoEnd):
        self.deleteWall(CoStart,CoEnd)
        
        
        
        
        
                     
    def placeHouse(self):
        self.clear()
        self.clearInside()
        self.placeGround((self.startX, self.startY, self.startZ), (self.endX, self.endY, self.endZ),self.ground)

        if self.hasGarder:
            if self.houseDirection == "north" :
                if self.gardenSide == "left":
                    self.placeGround((self.startX+ (self.endX - self.startX)//2, self.startY, self.startZ), (self.endX, self.endY, self.startZ + (self.endZ - self.startZ)//2), self.grass)
                    self.placeRoof((self.startX, self.startY, self.startZ), (self.endX - (self.endX - self.startX)//2, self.endY, self.endZ))
                    self.placeRoof((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ + (self.endZ - self.startZ)//2), (self.endX, self.endY, self.endZ))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.startX +(self.endX - self.startX)//2 , self.endY, self.startZ))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.startX, self.endY, self.endZ ))
                    self.placeWall((self.startX, self.startY, self.endZ-1), (self.endX , self.endY, self.endZ-1))
                    self.placeWall((self.endX-1, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.endX-1, self.endY, self.endZ))
                    self.placeWall((self.startX + (self.endX - self.startX)//2 , self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.endX , self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    self.placeWall((self.startX + (self.endX - self.startX)//2 -1, self.startY, self.startZ), (self.startX + (self.endX - self.startX)//2 -1, self.endY, self.startZ+ (self.endZ - self.startZ)//2 ))
                    self.placeDoor("north", self.endX - (self.endX -self.startX) // 4 -1 , (self.startZ + self.endZ) //2,self.startY)
                    if self.hasGarage:
                        self.placeGarage((self.startX+1, self.startY, self.startZ), (self.startX +(self.endX - self.startX)//2 -1 , self.endY, self.startZ))
                   
                else:
                    self.placeGround((self.startX, self.startY, self.startZ), (self.startX + (self.endX-self.startX)//2, self.endY, self.startZ + (self.endZ - self.startZ)//2), self.grass)
                    self.placeRoof((self.endX- (self.endX - self.startX)//2, self.startY, self.startZ), (self.endX , self.endY, self.endZ))
                    self.placeRoof((self.startX , self.startY, self.startZ + (self.endZ - self.startZ)//2), (self.endX - (self.endX - self.startX)//2, self.endY, self.endZ))
                    self.placeWall((self.startX, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.endX - (self.endX - self.startX)//2, self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    self.placeWall((self.startX, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.startX, self.endY, self.endZ ))
                    self.placeWall((self.startX, self.startY, self.endZ-1), (self.endX  , self.endY, self.endZ-1))
                    self.placeWall((self.endX-1, self.startY, self.startZ), (self.endX-1, self.endY, self.endZ))
                    self.placeWall((self.startX+ (self.endX - self.startX)//2, self.startY, self.startZ), (self.endX, self.endY, self.startZ))
                    self.placeWall((self.startX+ (self.endX - self.startX)//2, self.startY, self.startZ), (self.startX+ (self.endX - self.startX)//2, self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    self.placeDoor("north", self.startX + (self.endX -self.startX) // 4 , (self.startZ + self.endZ) //2,self.startY)
                    if self.hasGarage:
                        self.placeGarage((self.startX+ (self.endX - self.startX)//2 +1, self.startY, self.startZ), (self.endX-1, self.endY, self.startZ))
                    
            elif self.houseDirection == "south":
                if self.gardenSide == "left":
                    self.placeGround((self.startX , self.startY, self.startZ + (self.endZ - self.startZ)//2), (self.startX+ (self.endX - self.startX)//2, self.endY, self.endZ), self.grass)
                    self.placeRoof((self.startX, self.startY, self.startZ), (self.endX, self.endY, self.startZ + (self.endZ - self.startZ)//2))
                    self.placeRoof((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ), (self.endX, self.endY, self.endZ))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.endX , self.endY, self.startZ))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.startX  , self.endY, self.startZ + (self.endZ - self.startZ)//2))
                    self.placeWall((self.startX, self.startY, self.startZ + (self.endZ - self.startZ)//2 -1), (self.startX + (self.endX - self.startX)//2 , self.endY, self.startZ + (self.endZ - self.startZ)//2 -1))
                    self.placeWall((self.startX + (self.endX - self.startX)//2, self.startY, self.endZ-1), (self.endX , self.endY, self.endZ-1))
                    self.placeWall((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ + (self.endZ - self.startZ)//2), (self.startX + (self.endX - self.startX)//2, self.endY, self.endZ))
                    self.placeWall((self.endX-1, self.startY, self.startZ), (self.endX-1, self.endY, self.endZ))
                    
                    self.placeDoor("south", self.startX + (self.endX -self.startX) // 4 , (self.startZ + self.endZ) //2 -1,self.startY)
                    if self.hasGarage:
                        self.placeGarage((self.startX+1, self.startY, self.startZ + (self.endZ - self.startZ)//2 +1), (self.startX +(self.endX - self.startX)//2 -1, self.endY, self.endZ -1))
                    
                else:
                    self.placeGround((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.endX, self.endY, self.endZ), self.grass)
                    self.placeRoof((self.startX, self.startY, self.startZ), (self.startX+(self.endX - self.startX)//2 , self.endY, self.endZ))
                    self.placeRoof((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ), (self.endX, self.endY, self.startZ+(self.endZ - self.startZ)//2))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.endX , self.endY, self.startZ))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.startX , self.endY, self.endZ))
                    self.placeWall((self.startX, self.startY, self.endZ-1), (self.startX + (self.endX - self.startX)//2  , self.endY, self.endZ-1))
                    self.placeWall((self.startX + (self.endX - self.startX)//2 -1, self.startY, self.startZ + (self.endZ - self.startZ)//2), (self.startX + (self.endX - self.startX)//2 -1, self.endY, self.endZ ))
                    self.placeWall((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ + (self.endZ - self.startZ)//2 -1), (self.endX , self.endY, self.startZ + (self.endZ - self.startZ)//2 -1))
                    self.placeWall((self.endX -1, self.startY, self.startZ ), (self.endX -1, self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    
                    
                    self.placeDoor("south", self.endX - (self.endX -self.startX) // 4 -1 , (self.startZ + self.endZ) //2 -1,self.startY)
                    if self.hasGarage:
                        self.placeGarage((self.startX+ (self.endX - self.startX)//2 +1, self.startY, self.startZ + (self.endZ - self.startZ)//2 +1), (self.endX-1, self.endY, self.endZ -1))
                    
            elif self.houseDirection == "west":
                if self.gardenSide == "left":
                    self.placeGround((self.startX, self.startY, self.startZ), (self.startX + (self.endX - self.startX)//2, self.endY, self.startZ+ (self.endZ - self.startZ)//2), self.grass)
                    self.placeRoof((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ), (self.endX, self.endY, self.endZ))
                    self.placeRoof((self.startX, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.startX + (self.endX - self.startX)//2, self.endY, self.endZ))
                    self.placeWall((self.startX+ (self.endX - self.startX)//2, self.startY, self.startZ), (self.endX, self.endY, self.startZ))
                    self.placeWall((self.startX+ (self.endX - self.startX)//2, self.startY, self.startZ), (self.startX+ (self.endX - self.startX)//2, self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    self.placeWall((self.endX-1, self.startY, self.startZ), (self.endX-1, self.endY, self.endZ))
                    self.placeWall((self.startX, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.startX+ (self.endX - self.startX)//2, self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    self.placeWall((self.startX, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.startX, self.endY, self.endZ))
                    self.placeWall((self.startX, self.startY, self.endZ-1), (self.endX, self.endY, self.endZ-1))
                    self.placeDoor("west", self.endX - (self.endX -self.startX) // 2 , self.startZ + (self.endZ - self.startZ)//4 ,self.startY)
                    if self.hasGarage:
                        self.placeGarage((self.startX, self.startY, self.startZ+ (self.endZ - self.startZ)//2 +1), (self.startX , self.endY, self.endZ -1))
                else:
                    self.placeGround((self.startX, self.startY, self.startZ+ (self.endZ - self.startZ)//2 ), (self.startX+ (self.endX-self.startX)//2, self.endY, self.endZ), self.grass)
                    self.placeRoof((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.endX, self.endY, self.endZ))
                    self.placeRoof((self.startX, self.startY, self.startZ), (self.endX, self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    self.placeWall((self.startX, self.startY, self.startZ+ (self.endZ - self.startZ)//2 -1), (self.startX+ (self.endX - self.startX)//2, self.endY, self.startZ+ (self.endZ - self.startZ)//2 -1))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.endX, self.endY, self.startZ))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.startX, self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    self.placeWall((self.startX + (self.endX - self.startX)//2, self.startY, self.endZ-1), (self.endX, self.endY, self.endZ-1))
                    self.placeWall((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.startX + (self.endX - self.startX)//2, self.endY, self.endZ))
                    self.placeWall((self.endX-1, self.startY, self.startZ), (self.endX-1, self.endY, self.endZ))
                    
                    self.placeDoor("west", self.startX + (self.endX -self.startX) // 2 , self.endZ - (self.endZ - self.startZ)//4  -1,self.startY)
                    if self.hasGarage:
                        self.placeGarage((self.startX, self.startY, self.startZ+1), (self.startX, self.endY, self.startZ+ (self.endZ - self.startZ)//2 -1))
                    
            elif self.houseDirection == "east":
                if self.gardenSide == "left":
                    self.placeGround((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.endX , self.endY, self.endZ, self.grass), self.grass)
                    self.placeRoof((self.startX, self.startY, self.startZ), (self.startX + (self.endX - self.startX)//2, self.endY, self.endZ))
                    self.placeRoof((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ), (self.endX, self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.endX , self.endY, self.startZ))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.startX, self.endY, self.endZ))
                    self.placeWall((self.startX, self.startY, self.endZ-1), (self.startX + (self.endX - self.startX)//2, self.endY, self.endZ-1))
                    self.placeWall((self.startX + (self.endX - self.startX)//2 -1, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.startX + (self.endX - self.startX)//2 -1, self.endY, self.endZ))
                    self.placeWall((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ+ (self.endZ - self.startZ)//2 -1), (self.endX , self.endY, self.startZ+ (self.endZ - self.startZ)//2 -1))
                    self.placeWall((self.endX-1, self.startY, self.startZ), (self.endX-1, self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    
                    self.placeDoor("east", self.startX + (self.endX -self.startX) // 2 -1 ,self.endZ - (self.endZ - self.startZ)//4 -1,self.startY)
                    if self.hasGarage:
                        self.placeGarage((self.endX-1, self.startY, self.startZ +1), (self.endX-1, self.endY, self.startZ+ (self.endZ - self.startZ)//2 -1))
                else :
                    self.placeGround((self.startX+ (self.endX -self.startX) // 2 , self.startY, self.startZ), (self.endX, self.endY, self.startZ+ (self.endZ - self.startZ)//2), self.grass)
                    self.placeRoof((self.startX, self.startY, self.startZ), (self.startX + (self.endX - self.startX)//2, self.endY, self.endZ))
                    self.placeRoof((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.endX, self.endY, self.endZ))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.startX+ (self.endX - self.startX)//2 , self.endY, self.startZ))
                    self.placeWall((self.startX, self.startY, self.startZ), (self.startX, self.endY, self.endZ))
                    self.placeWall((self.startX, self.startY, self.endZ-1), (self.endX , self.endY, self.endZ-1))
                    self.placeWall((self.startX + (self.endX - self.startX)//2, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.endX , self.endY, self.startZ+ (self.endZ - self.startZ)//2))
                    self.placeWall((self.startX + (self.endX - self.startX)//2 -1, self.startY, self.startZ), (self.startX + (self.endX - self.startX)//2 -1, self.endY, self.startZ+ (self.endZ - self.startZ)//2 ))
                    self.placeWall((self.endX-1, self.startY, self.startZ+ (self.endZ - self.startZ)//2), (self.endX-1, self.endY, self.endZ))
                    
                    self.placeDoor("east", self.endX - (self.endX -self.startX) // 2 -1 , self.startZ + (self.endZ - self.startZ)//4 ,self.startY)
                    if self.hasGarage:
                        self.placeGarage((self.endX-1, self.startY, self.startZ+ (self.endZ - self.startZ)//2 +1), (self.endX-1, self.endY, self.endZ -1))
         
        else:
            self.houseWithoutGarden(self.houseDirection)    
        
        
    def placeDoorBasedOnDirection(self, direction):
        if direction in ["north", "south"]:
            z = self.startZ if direction == "north" else self.endZ - 1
            if (self.endX - self.startX) % 2 != 0:
                self.placeDoor(direction, (self.startX + self.endX)//2, z, self.startY)
            else:
                self.placeDoor(direction, (self.startX + self.endX)//2, z, self.startY)
                self.placeDoor(direction, ((self.startX + self.endX)//2)-1, z, self.startY)
        else:  
            x = self.startX if direction == "west" else self.endX - 1
            if (self.endZ - self.startZ) % 2 != 0:
                self.placeDoor(direction, x, (self.startZ + self.endZ)//2, self.startY)
            else:
                self.placeDoor(direction, x, (self.startZ + self.endZ)//2, self.startY)
                self.placeDoor(direction, x, ((self.startZ + self.endZ)//2)-1, self.startY)

    def houseWithoutGarden(self, direction="north"):  
        self.placeRoof((self.startX, self.startY, self.startZ), (self.endX, self.endY, self.endZ))
        self.placeWall((self.startX, self.startY, self.startZ), (self.endX, self.endY, self.startZ))
        self.placeWall((self.startX, self.startY, self.startZ), (self.startX, self.endY, self.endZ))
        self.placeWall((self.startX, self.startY, self.endZ-1), (self.endX, self.endY, self.endZ-1))
        self.placeWall((self.endX-1, self.startY, self.startZ), (self.endX-1, self.endY, self.endZ))

        self.placeDoorBasedOnDirection(direction)       
                
    
    
    
    def clear(self):
        for x in range(self.startX-1, self.endX+1):
            for y in range(self.startY-1, self.endY+1):
                for z in range(self.startZ-1, self.endZ+1):
                    self.editor.placeBlock((x, y, z), air)
        
if __name__ == "__main__":
    editor = Editor(buffering=True)
    buildArea = editor.getBuildArea()    
    coordinates_min = [min(buildArea.begin[i], buildArea.last[i]) for i in range(3)]
    coordinates_max = [max(buildArea.begin[i], buildArea.last[i]) for i in range(3)] 
    
    house = House(editor,coordinates_min[0],coordinates_min[1],coordinates_min[2],coordinates_max[0],coordinates_max[1],coordinates_max[2], style_basique,"east")

   # house.placeHouse()
   
    house.clear()
    editor.flushBuffer()
    
    
    
    
    
    