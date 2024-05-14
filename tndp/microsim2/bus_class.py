from vector_class import Vector

EPS = (1e-9)*(1e-9)

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
    def __init__(self, id, route, route_coords, capacity, starting_time, total_time):
        self.id = id
        self.route = route
        self.route_coords = route_coords
        self.time = 0
        self.capacity = capacity
        self.passengers = 0
        self.pos = Vector(route_coords[0])
        self.route_position = 1
        self.dir = 1
        self.current_node = route[0]
        self.state = "on_station"
        self.starting_time = starting_time
        self.node_time_map, self.index_time_list = self.node_at_time()
        self.time_node_map = self.time_at_node()
        self.total_time = 60*total_time
        self.step = Vector((0,0))
        self.set_pos_at_time(self.starting_time)
        self.stations_map = {i:[] for i in self.route}
        # Careful with routes with only one node!
        
    def __str__(self):
        str = f"Bus {self.id} at:{self.current_node}, capacity: {self.capacity}"
        return str
    
    def move(self):
        self.pos = self.pos + self.step
        vec = self.pos - self.get_next_coord()
        if vec.norm_sq < EPS:
            self.state = "on_station"
            self.current_node = self.get_next_pos()
            self.update_pos()
        else:
            self.state = "on_road"
    
    def update_pos(self):
        self.pos = self.get_next_coord()
        if(self.route_position + self.dir >= len(self.route) or self.route_position + self.dir < 0):
            self.dir *= -1
            #print("Changing direction!!")
        self.route_position += self.dir
        dt = abs(self.time_node_map[self.get_next_pos()] - self.time_node_map[self.get_last_pos()])
        self.step = (self.get_next_coord() - self.get_last_coord())*(1/dt)

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
        return Vector(self.route_coords[self.in_bounds(self.route_position)])
        
    
    def get_last_coord(self):
        return Vector(self.route_coords[self.in_bounds(self.route_position - self.dir)])
    
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
        t %= 2*self.total_time 
        if t >= self.total_time:
            t -= self.total_time
            idx = self.binary_search(lambda x: self.index_time_list[-1] - self.index_time_list[x] < t)
            self.dir = -1
            computed_time = t - self.index_time_list[-1] + self.index_time_list[idx]
        else:
            idx = self.binary_search(lambda x: self.index_time_list[x] > t)
            idx -= 1
            computed_time = t - self.index_time_list[idx]
        current_cord = self.route_coords[idx]
        next_idx = idx+self.dir
        next_cord = self.route_coords[next_idx]
        factor = (1/abs(self.time_node_map[self.route[next_idx]]-self.time_node_map[self.route[idx]]))
        pos = (Vector(next_cord) - Vector(current_cord))
        step = pos*factor
        pos = step*computed_time
        pos = Vector(current_cord) + pos
        return idx, next_idx, pos, step
    
    def set_pos_at_time(self, t):
        at, next, pos, step = self.get_pos_at_time(t)
        self.step = step
        self.route_position = next
        self.pos = pos
        vec1, vec2 = (Vector(self.route_coords[at]) - pos), (Vector(self.route_coords[next]) - pos)
        if vec1.norm_sq < EPS:
            self.state = "on_station"
            self.current_node = self.route[at]
        elif vec2.norm_sq < EPS:
            self.state = "on_station"
            self.current_node = self.route[next]
            self.update_pos()
        else:
            self.state = "on_road"
            
    def node_at_time(self):
        node_time_map = {}
        node_time_list = [0]*len(self.route)
        current_node = self.route[0]
        t = 0
        for idx, node in enumerate(self.route):
            t += next((c for a,c in network[node] if a == current_node), 0)
            node_time_map[t] = node
            node_time_list[idx] = t*60
            current_node = node
        return node_time_map, node_time_list
    
    def time_at_node(self):
        time_node_map = {v:x*60 for x,v in self.node_time_map.items()}
        return time_node_map