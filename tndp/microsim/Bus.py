from collections import deque
import numpy as np
import math

CAP = 40*1.25
TRANSFER_TIME = 5
ZERO_TRANSFER_MAX = 1.5
ONE_TRANSFER_MAX = 1.1
TWO_TRANSFER_MAX = 1.1
DELTA_F = 0.1

demand_matrix = np.array([
    [0, 400, 200, 60, 80, 150, 75, 75, 30, 160, 30, 25, 35, 0, 0],
    [400, 0, 50, 120, 20, 180, 90, 90, 15, 130, 20, 10, 10, 5, 0],
    [200, 50, 0, 40, 60, 180, 90, 90, 15, 45, 20, 10, 10, 5, 0],
    [60, 120, 40, 0, 50, 100, 50, 50, 15, 240, 40, 25, 10, 5, 0],
    [80, 20, 60, 50, 0, 50, 25, 25, 10, 120, 20, 15, 5, 0, 0],
    [150, 180, 180, 100, 50, 0, 100, 100, 30, 880, 60, 15, 15, 10, 0],
    [75, 90, 90, 50, 25, 100, 0, 50, 15, 440, 35, 10, 10, 5, 0],
    [75, 90, 90, 50, 25, 100, 50, 0, 15, 440, 35, 10, 10, 5, 0],
    [30, 15, 15, 15, 10, 30, 15, 15, 0, 140, 20, 5, 0, 0, 0],
    [160, 130, 45, 240, 120, 880, 440, 440, 140, 0, 600, 250, 500, 200, 0],
    [30, 20, 20, 40, 20, 60, 35, 35, 20, 600, 0, 75, 95, 15, 0],
    [25, 10, 10, 25, 15, 15, 10, 10, 5, 250, 75, 0, 70, 0, 0],
    [35, 10, 10, 10, 5, 15, 10, 10, 0, 500, 95, 70, 0, 45, 0],
    [0, 5, 5, 5, 0, 10, 5, 5, 0, 200, 15, 0, 45, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

passengers = np.zeros((15,15))

TOTAL_DEMAND = np.sum(demand_matrix)

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
    def __init__(self, route, capacity):
        self.route = route
        self.capacity = capacity
        self.passengers = []
        self.nodes = set(route)
        self.node_queue = deque(route)
        self.node_queue.popleft()
        self.last_node = route[0]
        self.time = 0
        self.last_time = 0
        self.on_station = False
        self.current_station = -1
        
    def get_next_station_time(self):
        if len(self.node_queue) > 0 and self.last_node == self.node_queue[0]:
            return 0
        if len(self.node_queue) > 0:
            time = next(c for a,c in network[self.last_node] if a == self.node_queue[0])
            return time*60
        else:
            return -1
    
    def leave_station(self):
        self.on_station = False
        self.last_time = self.time
        self.last_node = self.node_queue.popleft()
        self.nodes.remove(self.last_node)
        
    def alight(self, passenger_list):
        to_add = []
        for passenger in self.passengers:
            if self.current_station == passenger.path[0]:
                to_add.append(passenger)
        self.passengers = list(filter(lambda p: p not in to_add, self.passengers))
        for passenger in to_add:
            passenger.path.popleft()
            if len(passenger.path) > 0:
                passenger_list.append(passenger)
                assert len(passenger.path) > 0
        passenger_list =  list(filter(lambda p: len(p.path) > 0, passenger_list))
    def board(self, passenger_list):
        to_remove = []
        passenger_list =  list(filter(lambda p: len(p.path) > 0, passenger_list))
        for passenger in passenger_list:
            assert len(passenger.path) > 0
                
        for passenger in passenger_list:
            if passenger.path[0] in self.nodes:
                self.passengers.append(passenger)
                to_remove.append(passenger)
        passenger_list = list(filter(lambda p: p not in to_remove, passenger_list))
        
    
    def advance_time(self, active_stations):
        self.time += 1
        if len(self.node_queue) > 0 and  self.time - self.last_time + 50 >= self.get_next_station_time():
            print(self.get_next_station_time())
            active_stations[self.node_queue[0]] = True
        if self.time - self.last_time == self.get_next_station_time():
            self.on_station = True
            self.current_station = self.node_queue[0]
    
    