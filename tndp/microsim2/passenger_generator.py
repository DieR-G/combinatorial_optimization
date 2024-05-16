from route_assignation import get_travel_routes
import copy
import math
import numpy as np
demand_matrix = [[0, 400, 200, 60, 80, 150, 75, 75, 30, 160, 30, 25, 35, 0, 0],
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
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

start_time_matrix = []

class Passenger:
    def __init__(self, id, arrival_time, travel_path, start_station, end_station):
        self.id = id
        self.active = True
        self.arrival_time = arrival_time
        self.path=travel_path
        self.path_pos = len(self.path) - 1
        self.current_bus="-1"
        self.start_station = start_station
        self.current_station= self.start_station
        self.end_station = end_station
    def __str__(self):
        str = f"Active: {self.active}\nArrival time: {self.arrival_time}\nStarting Node: {self.start_station}\nEnding Node: {self.end_station}\nNodes: {list(reversed(self.path))}"
        return str
    
    def __eq__(self, other):
        if not isinstance(other, Passenger):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
def generate_passengers_test(routes, stations_set, passengers_at_time):
    passenger_set = set()
    travels = get_travel_routes(routes)
    pass_idx = 0
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix)):
            if len(travels[i][j]) == 0:
                continue
            if demand_matrix[i][j] == 0:
                continue
            total_users = int(demand_matrix[i][j])
            arriving_time = 0
            dt = math.ceil(3600/demand_matrix[i][j])
            for k in range(total_users):
                passengers_at_time[arriving_time] += 1
                new_passenger = Passenger(pass_idx, arriving_time, travels[i][j][k%len(travels[i][j])], i, j)
                stations_set[i].add(new_passenger)
                passenger_set.add(new_passenger)
                arriving_time += dt
                pass_idx += 1
    
    return passenger_set