import numpy as np
from Stations import Stations
from Route import Route

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

TOTAL_DEMAND = np.sum(demand_matrix)

print(TOTAL_DEMAND)

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

network_routes = [
    [0, 1, 2, 5, 7, 9, 10, 12],
    [4, 3, 5, 7, 14, 6],
    [11, 3, 5, 14, 8],
    [9, 13, 12]
]

routes = [
    Route(network_routes[0], 3600/68.2),
    Route(network_routes[1], 3600/22.58),
    Route(network_routes[2], 3600/14.91),
    Route(network_routes[3], 3600/5.66),
]

city = Stations([i for i in range(15)])

def change_to_one(val):
    val[0] = 1

end_time = 60*10
for t in range(1, end_time):
    city.advance_time()
    for r in routes:
        r.advance_time(city.active_nodes)
        if r.has_bus_on_station:
            on_station_buses = r.get_on_station_buses()
            for bus in on_station_buses:
                bus.alight(city.stations[bus.current_station])
                bus.board(city.stations[bus.current_station])
            r.leave_stations()
    
    if(t % 60 == 0):
        pass_list = {key:len(val) for key, val in city.stations.items()}
        print(pass_list)
        print('*')