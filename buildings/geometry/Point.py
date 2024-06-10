class Point:
    def __init__(self, x : int = None, y : int = None, z : int = None, p : tuple[int] = None):
        if p != None: x,y,z = p
        self.x = x
        self.y = y
        self.z = z
        self.position = (x,y,z)
        
    def set_position(self, x : int = None, y : int = None, z : int = None, p : tuple[int] = None):
        if p != None: x,y,z = p
        self.x = x if x != None else self.x
        self.y = y if y != None else self.y
        self.z = z if z != None else self.z
        self.position = (self.x,self.y,self.z)