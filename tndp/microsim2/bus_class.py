network = [
    [(1, 8)], 
    [(2, 2), (3, 3), (4, 6), (0, 8)],
    [(1, 2), (5, 3)], 
    [(1, 3), (4, 4), (5, 4), (11, 10)], 
    [(3, 4), (1, 6)], 
    [(7, 2), (2, 3), (14, 3), (3, 4)], 
    [(14, 2), (9, 7)], 
    [(5, 2), (14, 2), (9, 8)], 
    [(14, 8)], 
    [(10, 5), (6, 7), (7, 8), (13, 8), (12, 10)], 
    [(12, 5), (9, 5), (11, 10)], 
    [(3, 10), (10, 10)], 
    [(13, 2), (10, 5), (9, 10)], 
    [(12, 2), (9, 8)], 
    [(7, 2), (6, 2), (5, 3), (8, 8)]
]

class Bus:
    def __init__(self, id, route, capacity, starting_time, total_time):
        self.id = id
        self.route = route
        self.capacity = capacity
        self.route_position = 1
        self.dir = 1
        self.current_node = route[0]
        self.state = "on_station"
        self.pos = 0
        self.starting_time = starting_time
        self.node_time_map, self.index_time_list = self.node_at_time()
        self.total_time = 60*total_time
        self.pos_index = {v:e for e,v in enumerate(self.route)}
        self.set_pos_at_time(self.starting_time)
        self.stations_map = {i:[] for i in self.route}
        
    def __str__(self):
        str = f"Bus {self.id} at:{self.current_node}, capacity: {self.capacity}"
        return str
    
    def move(self):
        self.pos += self.dir
        if self.pos in self.node_time_map:
            self.state = "on_station"
            self.current_node = self.node_time_map[self.pos]
            self.update_pos()
        else:
            self.state = "on_road"
    
    def update_pos(self):
        if(self.route_position + self.dir >= len(self.route) or self.route_position + self.dir < 0):
            self.dir *= -1
        self.route_position += self.dir
        
    def in_bounds(self, val):
        if val < 0:
            return 0
        if val >= len(self.route):
            return len(self.route) - 1
        return val
    
    def get_last_pos(self):
        return self.route[self.in_bounds(self.route_position - self.dir)]
    
    def get_next_pos(self):
        return self.route[self.in_bounds(self.route_position)]
    
    def get_next_coord(self):
        pass
        
    def get_last_coord(self):
        pass
    
    def binary_search(self, f):
        n = len(self.route) - 1
        l, h = 0, n
        while l < h:
            m = (h+l)//2
            if f(m):
                h = m
            else:
                l = m + 1
        return l
    
    def get_pos_at_time(self, t):
        if t >= self.total_time:
            t -= self.total_time
            idx = self.binary_search(lambda x: self.index_time_list[-1] - self.index_time_list[x] < t)
            self.dir = -1
        else:
            idx = self.binary_search(lambda x: self.index_time_list[x] > t)
            idx -= 1
        next_idx = idx+self.dir
        return idx, next_idx
    
    def set_pos_at_time(self, t):
        t %= 2*self.total_time 
        at, next = self.get_pos_at_time(t)
        self.route_position = next
        self.state = "on_station"
        if t in self.node_time_map:
            self.current_node = self.route[at]
        elif 2*self.total_time - t in self.node_time_map:
            self.current_node = self.route[next]
            self.update_pos()
        else:
            self.state = "on_road"
        if self.dir > 0:
            self.pos = t
        else:
            self.pos = 2*self.total_time - t
                 
    def node_at_time(self):
        node_time_map = {}
        node_time_list = [0]*len(self.route)
        current_node = self.route[0]
        t = 0
        for idx, node in enumerate(self.route):
            t += next((c for a,c in network[node] if a == current_node), 0)
            node_time_map[t*60] = node
            node_time_list[idx] = t*60
            current_node = node
        return node_time_map, node_time_list
    