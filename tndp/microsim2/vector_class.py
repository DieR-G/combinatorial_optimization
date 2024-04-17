import math

class Vector:
    def __init__(self, p):
        self.x = p[0]
        self.y = p[1]
    
    def __sub__(self, b):
        return Vector((self.x - b.x, self.y - b.y))
    
    def __add__(self, b):
        return Vector((self.x + b.x, self.y + b.y))
    
    def __mul__(self, m):
        return(Vector((self.x*m, self.y*m)))
    
    def norm(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
    
    def __str__(self) -> str:
        return f"x: {self.x}, y:{self.y}"
    
    def normalize(self):
        self.x *= 1/self.length
        self.y *= 1/self.length
    
    def mult(self, m):
        return Vector((self.x*m, self.y*m))