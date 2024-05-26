import random as rd
from buildings.elements.Window import Window

class Balcony:
    def __init__(self, rdata, length : int, max_width : int, windows : Window):
        self.rdata = rdata
        self.length = length
        self.max_width = max_width
        self.windows = windows
        
    def has_multiple_balcony(self):
        if self.max_width < self.rdata["balcony"]["multiple"]["min_width"]: return False
        return self.rdata["balcony"]["multiple"]["proba"] >= rd.random()