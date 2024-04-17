from collections import deque

class Passenger:
    def __init__(self, path):
        self.active = True
        self.path = deque(path)
        
    def get_next_node(self):
        return self.path[0]
    
    def alight(self):
        self.path.popleft()