from bus_factory import BusFactory
import math
from route_assignation import compute_time

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

def generate_buses(routes, frequencies, capacity):
    bus_factory = BusFactory(network)
    buses = [[] for _ in range(len(routes))]
    for k in range(len(routes)):
        route_time = compute_time(routes[k][0], routes[k][-1], routes[k])
        node_time_map, index_time_list = bus_factory.node_at_time(routes[k])
        bus_number = math.ceil(frequencies[k] * route_time / 30)
        time_delta = math.ceil(3600 / frequencies[k])
        start_time = 0
        for i in range(bus_number):
            new_bus = bus_factory.create_bus(str(k) + str(i), routes[k],
                                             capacity, start_time, route_time, node_time_map, index_time_list)
            buses[k].append(new_bus)
            start_time += time_delta
    return buses
