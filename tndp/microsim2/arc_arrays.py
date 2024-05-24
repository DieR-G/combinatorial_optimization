import numpy as np
from bus_generator import generate_buses_on_space

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


network_routes = [[0, 1, 2, 5, 7, 9, 10, 12]]

network_coordinates = [
    list(map(lambda x: tuple(coordinates[x]), r)) for r in network_routes
]

network_routes = [[0,1,2,5,7,9,10,12], [4,3,5,7,14,6], [11,3,5,14,8],[9,13,12]]
network_frequencies = [68.2, 19.900000000000002, 15.210936746793037, 5.446410882717701]

bus_routes = generate_buses_on_space(network_routes, network_frequencies, 50, arc_positions)

import matplotlib.pyplot as plt
import numpy as np

# Function to draw the buses as points on the map
def draw_buses(bus_routes, arc_coordinates):
    fig, ax = plt.subplots()

    # Draw the bus routes
    for arc, coordinates in arc_coordinates.items():
        lons, lats = zip(*coordinates)
        ax.plot(lons, lats, 'k-', linewidth=0.5, alpha=0.6)  # Plot the route as a thin line

    # Draw the buses
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # Different colors for different routes
    for route_idx, route in enumerate(bus_routes):
        color = colors[route_idx % len(colors)]
        for bus in route:
            arc = bus.get_arc()
            if arc in arc_coordinates:
                coordinates = arc_coordinates[arc]
                position_within_arc = bus.get_arc_position()
                position = min(max(0, position_within_arc), len(coordinates) - 1)  # Ensure index is within bounds
                lon, lat = coordinates[position]
                ax.plot(lon, lat, marker='o', markersize=2, color=color)  # Plot the bus as a small point

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Bus Positions on Routes')
    plt.show()

# Assuming bus_routes and arc_coordinates are defined as per the provided code
draw_buses(bus_routes, arc_coordinates)
