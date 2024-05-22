import numpy as np
from bus_class import Bus

def interpolate_coordinates(start, end, num_points):
    lon_values = np.linspace(start[0], end[0], num_points + 1)
    lat_values = np.linspace(start[1], end[1], num_points + 1)
    return list(zip(lon_values, lat_values))

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

edge_coordinates = { 
    (i, j): interpolate_coordinates(coordinates[i], coordinates[j], weight)
    for i, connections in enumerate(network)
    for j, weight in connections
}
network_routes = [[0, 1, 2, 5, 7, 9, 10, 12]]

network_coordinates = [
    list(map(lambda x: tuple(coordinates[x]), r)) for r in network_routes
]
st = 0
test_bus = Bus('1', [0, 1, 2, 5, 7, 9, 10, 12], 50, st, 1980)