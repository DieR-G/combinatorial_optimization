import matplotlib.pyplot as plt
import matplotlib.animation as animation
from vector_class import *
from route_assignation import compute_time
from bus_class import Bus

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

network_routes = [[0, 1, 2, 5, 7, 9, 10, 12]]

network_coordinates = [
    list(map(lambda x: tuple(coordinates[x]), r)) for r in network_routes
]

def create_coordinate_arrays(route, coordinates):
    point_array = []
    for i in range(len(route) - 1):
        current_node, next_node = route[i], route[i + 1]
        v1, v2 = Vector(coordinates[i]), Vector(coordinates[i + 1])
        v3 = v2 - v1
        pos = v1
        total_time = compute_time(current_node, next_node, route) * 60
        v3 *= 1 / total_time
        for i in range(total_time):
            point_array.append(pos)
            pos += v3
    point_array.append(Vector(coordinates[-1]))
    return [v.to_tup() for v in point_array]

positions = create_coordinate_arrays(network_routes[0], network_coordinates[0])
space = [0] * len(positions)

# Create a list of buses
n_buses = 31
buses = [Bus(f'{i+1}', network_routes[0], 50, i * 10, 1980) for i in range(n_buses)]

fig, ax = plt.subplots()
ax.set_xlim(min(x[0] for x in positions), max(x[0] for x in positions))
ax.set_ylim(min(x[1] for x in positions), max(x[1] for x in positions))

# Create a list of plot objects for each bus
bus_dots = [ax.plot([], [], 'o', markersize=1)[0] for _ in range(n_buses)]

wt = 0

def init():
    for dot in bus_dots:
        dot.set_data([], [])
    return bus_dots

def update(frame):
    global wt
    for b in buses:
        if b.stop_time > 0:
            b.stop_time -= 1
            continue
        if space[b.pos + 1] == 0 and space[b.pos + 2] == 0 and space[b.pos + 3] == 0 and space[b.pos + 4] == 0:
            space[b.pos] = 0
            b.move()
            space[b.pos] = 1
        else:
            continue
        if b.state == 'on_station':
            b.stop_time = 30
    for i, b in enumerate(buses):
        bus_dots[i].set_data(positions[b.pos][0], positions[b.pos][1])
    return bus_dots

ani = animation.FuncAnimation(fig, update, frames=3000, init_func=init, blit=True, interval=20)

plt.show()