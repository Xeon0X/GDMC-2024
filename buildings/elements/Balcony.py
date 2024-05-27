import random as rd
from buildings.elements.Window import Window

class Balcony:
    def __init__(self, rdata, max_width : int, windows : Window):
        self.rdata = rdata
        self.max_width = max_width
        self.windows = windows
        self.length = self.get_len()
        self.has_multiple = self.has_multiple_balcony()
        
    def follow_window(self) -> bool:
        pass
        
        
    def has_multiple_balcony(self) -> bool:
        if self.max_width < self.rdata["balcony"]["multiple"]["min_width"]: return False
        return self.rdata["balcony"]["multiple"]["proba"] >= rd.random()
    
    def get_len(self) -> int:
        return rd.randint(self.rdata["balcony"]["size"]["min_len"], self.rdata["balcony"]["size"]["max_len"])