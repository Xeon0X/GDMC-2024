from gdpc import Editor
from buildings.geometry.Vertice import Vertice

class Glass:
    def __init__(self, x1 : int, x2 : int, group1 : list[Vertice], group2 : list[Vertice] = None):
        self.x1, self.x2 = x1, x2
        self.group1, self.group2 = group1, group2
        
        
    def build(self, editor : Editor, material1 : str, material2 : str):
        for elt in self.group1:
            elt.fill(editor, material1)
        if self.group2 is None: return
        for elt in self.group2:
            elt.fill(editor, material2)
            
    def reset_groups(self):
        self.group1, self.group2 = [], []
    
    def __len__(self):
        return self.x2 - self.x1 + 1
        