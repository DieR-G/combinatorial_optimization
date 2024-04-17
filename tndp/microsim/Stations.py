import numpy as np
from Passenger import Passenger
import route_assignation
import math

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

class Stations:
    def __init__(self, nodes):
        self.stations = {x: [] for x in nodes}
        self.time = 0
        self.node_times = [0]*len(nodes)
        self.nodes = nodes
        self.active_nodes = [False]*len(nodes)
        self.travels = route_assignation.get_travel_routes()
        self.passenger_count = {key:0 for key in self.travels}
    
    def compute_passengers(self, i, j):
            new_passenger_count = math.floor((demand_matrix[i][j]/3600)*self.time) - self.passenger_count[(i, j)]        
            if(new_passenger_count > 0):
                for _ in range(new_passenger_count):
                    new_passenger = Passenger(self.travels[(i,j)][self.passenger_count[(i,j)] % len(self.travels[(i, j)])])
                    assert(len(new_passenger.path) > 0)
                    self.stations[i].append(new_passenger)
                    self.passenger_count[(i, j)] += 1
    
    def advance_time(self):
        self.time += 1
        if(self.time <= 128*60):
            for starting_node in self.nodes:
                if self.active_nodes[starting_node]:
                    for ending_node in self.nodes:
                        if starting_node == ending_node:
                            continue
                        self.compute_passengers(starting_node, ending_node)