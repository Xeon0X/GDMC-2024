import random as rd
from buildings.geometry.Polygon import Polygon

class Roof:
    def __init__(self,rdata, polygon : Polygon):
        self.rdata = rdata
        self.polygon = polygon
        self.has_rembard = self.has_rembard()
        
    def build(self, editor, materials : list[str]):
        self.polygon.fill(editor, materials[0])
        if self.has_rembard: self.polygon.fill_vertice(editor, materials[9],1)
        
    def has_rembard(self):
        return rd.random() <= self.rdata["rembard"]
