from bus_class import *
import math

def compute_time(i, j, r):
    start, end = sorted((r.index(i), r.index(j)))
    edges = [(network[r[m]], r[m + 1]) for m in range(start, end)]
    cost = sum(
        list(map(lambda p: next((c for a, c in p[0] if a == p[1]), (0, 0)), edges)))
    return cost

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
    buses = [[] for _ in range(len(routes))]
    for k in range(len(routes)):
        route_time = compute_time(routes[k][0], routes[k][-1], routes[k])
        bus_number = math.ceil(frequencies[k]*route_time/30)
        time_delta = math.ceil(3600 / frequencies[k])
        start_time = 0
        for i in range(bus_number):
            new_bus = Bus(str(k) + str(i), routes[k],
                            capacity, start_time, route_time)
            buses[k].append(new_bus)
            start_time += time_delta
            i += 1
    return buses