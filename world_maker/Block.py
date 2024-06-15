from gdpc import Editor, Block, geometry
from gdpc.lookup import *
import numpy as np
import math

SOLID_NATURAL_BLOCKS = SOILS | STONES | ORES | LIQUIDS

class Block:
    def __init__(self, coordinates:tuple, name:str):
        self.coordinates = coordinates
        self.name = name
        self.neighbors = []
        self.surface = None


    def addNeighbors(self, neighbors:list[Block]):
        for neighbor in neighbors:
            self.neighbors.append(neighbor)

    def isSurface(self):
        if self.surface == None:
            if str(self.name) in SOLID_NATURAL_BLOCKS:
                for neighbor in self.neighbors:
                    if str(neighbor.name) not in SOLID_NATURAL_BLOCKS:
                        self.surface = True
                        return True
                if len(self.neighbors) != 0:
                    self.surface = False
                    return False
            else:
                self.surface = False
                return False
        else:
            return self.surface