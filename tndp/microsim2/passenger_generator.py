from route_assignation import get_travel_routes, get_first_travel_route, get_travel_routes_prop
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
    def __init__(self, arrival_time, travel_path, start_station, end_station):
        self.active = True
        self.arrival_time = arrival_time
        self.path=travel_path
        self.current_bus="-1"
        self.start_station = start_station
        self.current_station= self.start_station
        self.end_station = end_station
    def __str__(self):
        str = f"Active: {self.active}\nArrival time: {self.arrival_time}\nStarting Node: {self.start_station}\nEnding Node: {self.end_station}\nNodes: {list(reversed(self.path))}"
        return str
    
def initialize_start_matrix(routes):
    st = [[0 for _ in range(len(demand_matrix))] for _ in range(len(demand_matrix))]
    for p, v in get_first_travel_route(routes).items():
        if p[0] >= len(demand_matrix) or p[1] >= len(demand_matrix):
            break
        st[p[0]][p[1]] = v
    global start_time_matrix
    start_time_matrix = st

def generate_passengers_test(routes, max_route_time = 0):
    passenger_vector = []
    #initialize_start_matrix(routes)
    travels = get_travel_routes(routes)
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix)):
            if len(travels[i][j]) == 0:
                continue
            if demand_matrix[i][j] == 0:
                continue
            total_users = int(demand_matrix[i][j])
            #remember to change back to start_time_matrix[i][j]*60
            arriving_time = max_route_time
            dt = math.ceil(3600/demand_matrix[i][j])
            for k in range(total_users):
                new_passenger = Passenger(arriving_time, copy.deepcopy(travels[i][j][k%len(travels[i][j])]), i, j)
                passenger_vector.append(new_passenger)
                arriving_time += dt
    
    return passenger_vector

def generate_passengers_test_prop(routes, frequencies):
    passenger_vector = []
    travels = get_travel_routes_prop(routes, frequencies)
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix)):
            if len(travels[i][j]) == 0:
                continue
            if demand_matrix[i][j] == 0:
                continue
            for path, proportion in travels[i][j]:
                total_users = math.ceil(demand_matrix[i][j]*proportion)
                for _ in range(total_users):
                    new_passenger = Passenger(0, copy.deepcopy(path), i, j)
                    passenger_vector.append(new_passenger)
    return passenger_vector

def generate_passengers(simulation_time_left, routes):
    passenger_vector=[]
    initialize_start_matrix(routes)
    travels = get_travel_routes(routes)
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix[i])):
            if len(travels[i][j]) == 0:
                continue
            if demand_matrix[i][j] == 0: continue
            total_users=demand_matrix[i][j]
            time_delta=3600/total_users #Segundos por pasajero
            arrival_time=0 
            for k in range(total_users):
                arrival_time+=time_delta
                if arrival_time >= start_time_matrix[i][j]*60:
                    new_passenger = Passenger(int(arrival_time), copy.deepcopy(travels[i][j][k%len(travels[i][j])]), i, j)
                    assert(len(new_passenger.path) > 0)
                    passenger_vector.append(new_passenger)
                    
            remaining_users=int(simulation_time_left/time_delta)
            for k in range(remaining_users):
                arrival_time+=time_delta
                new_passenger = Passenger(int(arrival_time), copy.deepcopy(travels[i][j][k%len(travels[i][j])]), i, j)
                assert(len(new_passenger.path) > 0)
                passenger_vector.append(new_passenger)

    return passenger_vector