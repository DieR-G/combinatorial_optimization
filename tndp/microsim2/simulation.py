from bus_generator import generate_buses
from passenger_generator import generate_passengers_test
import datetime
import itertools
import numpy as np


STATION_NUMBER = 15
MAX_TIME_SIMULATED = 10000
TRANSFER_TIME = 5*60

station_passengers_history = []
time_history = []

coordinates = [[-46.449444, -25.874734],
               [-46.350297, -25.973882],
               [-46.216734, -25.977159],
               [-46.349477, -26.083682],
               [-46.506802, -26.083682],
               [-46.217553, -26.08614],
               [-45.884057, -26.218064],
               [-46.09956, -26.218883],
               [-45.836531, -26.08532],
               [-45.978288, -26.376208],
               [-46.04466, -26.461426],
               [-46.38635, -26.331961],
               [-45.936499, -26.504035],
               [-45.855378, -26.439302],
               [-45.9873, -26.084501]]

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

def interpolate_coordinates(start, end, num_points):
    lon_values = np.linspace(start[0], end[0], num_points + 1)
    lat_values = np.linspace(start[1], end[1], num_points + 1)
    return list(zip(lon_values, lat_values))

arc_coordinates = { 
    (i, j): interpolate_coordinates(coordinates[i], coordinates[j], weight*60)
    for i, connections in enumerate(network)
    for j, weight in connections
}

arc_positions = {
    (i, j): [False]*weight*60
    for i, arc in enumerate(network)
    for j, weight in arc
}

def simulate(network_frequencies, network_routes, CAP):    
    passengers_at_time = [0]*MAX_TIME_SIMULATED
    stations = [set() for _ in range(STATION_NUMBER)]
    passengers = generate_passengers_test(network_routes, stations, passengers_at_time)
    bus_routes = generate_buses(network_routes, network_frequencies, CAP)
    passengers_pref_time = list(itertools.accumulate(passengers_at_time))
    print(len(passengers))
    t_s = datetime.datetime.now()
    n = len(passengers)
    inv_time = 0
    t_time = 0
    w_time = 0
    on_bus = 0
    
    def alight_passengers(bus):
        nonlocal on_bus, t_time, stations
        for passenger in bus.stations_map[bus.current_node]:
            passenger.current_bus = "-1"
            passenger.current_station = passenger.path[passenger.path_pos]
            passenger.path_pos -= 1
            if passenger.path_pos < 0:
                passengers.remove(passenger)
                continue
            stations[passenger.current_station].add(passenger)
            t_time += TRANSFER_TIME
        bus.capacity += len(bus.stations_map[bus.current_node])
        on_bus -= len(bus.stations_map[bus.current_node])
        bus.stations_map[bus.current_node] = []
            
    def board_passengers(bus, t):
        nonlocal on_bus, stations
        to_remove = []
        for passenger in stations[bus.current_node]:
            if passenger.arrival_time > t:
                continue
            if bus.capacity > 0:
                to = bus.route[bus.route_position:] if bus.direction > 0 else bus.route[:bus.route_position + 1]
                if passenger.path[passenger.path_pos] in to:
                    passenger.current_bus = bus.id
                    bus.capacity -= 1
                    on_bus += 1
                    bus.stations_map[passenger.path[passenger.path_pos]].append(passenger)
                    to_remove.append(passenger)  # Add passenger to the removal list
            else:
                break
        for passenger in to_remove:
            stations[bus.current_node].discard(passenger)
         
    def move_bus(bus, time):
        if bus.state == "on_station":
            alight_passengers(bus)
            board_passengers(bus, time) 
        bus.move()
        assert(bus.capacity >= 0 and bus.capacity <= 50)
        
    def move_bus_on_arcs(bus, arc_positions, time):
        arc = bus.get_arc()
        if bus.stop_time > 0:
            bus.stop_time -= 1
            return
        arc_positions[arc][bus.get_arc_position()] = False
        bus.move()
        if arc_positions[bus.get_arc()][bus.get_arc_position()]:
            bus.undo_move()
            arc_positions[bus.get_arc()][bus.get_arc_position()] = True
            return
        arc_positions[bus.get_arc()][bus.get_arc_position()] = True
        if bus.state == 'on_station':
            bus.stop_time = 30
            alight_passengers(bus)
            board_passengers(bus, time) 
            
    time = 0
    while len(passengers) > 0:
        for route in bus_routes:
            for bus in route:
                move_bus_on_arcs(bus, arc_positions, time)
        inactives = n - len(passengers)
        w_time += passengers_pref_time[time] - on_bus - inactives
        inv_time += on_bus
        time += 1
    print(time)
    print(inv_time//60, w_time//60, t_time//60, (inv_time+w_time+t_time)//60)
    t_e = datetime.datetime.now()
    print(t_e-t_s)

coordinates = [[-46.449444, -25.874734],
               [-46.350297, -25.973882],
               [-46.216734, -25.977159],
               [-46.349477, -26.083682],
               [-46.506802, -26.083682],
               [-46.217553, -26.08614],
               [-45.884057, -26.218064],
               [-46.09956, -26.218883],
               [-45.836531, -26.08532],
               [-45.978288, -26.376208],
               [-46.04466, -26.461426],
               [-46.38635, -26.331961],
               [-45.936499, -26.504035],
               [-45.855378, -26.439302],
               [-45.9873, -26.084501]]
CAP = 50
""" network_frequencies = [1000]
network_routes = [
    [0,1,2,5,7,9,10,12]
]
simulation_time = 600 """

network_routes = [[0,1,2,5,7,9,10,12], [4,3,5,7,14,6], [11,3,5,14,8],[9,13,12]]
network_frequencies = [68.2, 19.900000000000002, 15.210936746793037, 5.446410882717701] 

""" network_routes = [[10,12,13,9,7,14,5,2,1,0],[6,14,5,3,4],[11,3,5,14,8]]
network_frequencies = [68.5, 19.900000000000002, 16.45525002610718] """

""" network_routes = [[0,1,2,5,7,9,10]]
network_frequencies = [10] 
simulation_time = 5580
"""


simulate(network_frequencies, network_routes, CAP)