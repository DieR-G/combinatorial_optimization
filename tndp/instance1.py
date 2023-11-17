import math
import heapq as hpq
import json
network_file = 'data/bus_assign_network1.json'
routes_file = 'data/route_assign1.json'
network = []
with open(network_file, 'r') as net_file:
    network = json.load(net_file)

network = [[ tuple(y) for y in x ] for x in network]

routes = []
with open(routes_file, 'r') as rout_file:
    routes = json.load(rout_file)

routes = [[ tuple(y) for y in x] for x in routes]


route_arc_flows = {}

def calc_path_time(path):
    cost = 0
    for arc in path:
        for pair in network[arc[0]]:
            if pair[0] == arc[1]:
                cost += pair[1]
                break
    return cost

route_times = [
    calc_path_time(ri)/2 for ri in routes
]

route_max_flows = [0]*len(routes)

route_freq = [0]*len(routes)

demand_matrix = [
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
]

CAP = 40*1.25

def path_to_arcset(path):
    arcs_set=[]
    for i in range(len(path)-1):
        arcs_set.append((path[i], path[i+1]))
    return arcs_set

def shortest_path(s, e):
    visited = []
    path_pq = []
    hpq.heappush(path_pq, (0, [s]))
    while len(path_pq) > 0:
        current_element = hpq.heappop(path_pq)
        current_path = current_element[1]
        path_end = current_path[len(current_path)-1]
        if path_end in visited:
            continue
        visited.append(path_end)
        current_cost = current_element[0]
        for node in network[path_end]:
            aux_path = current_path.copy()
            aux_path.append(node[0])
            hpq.heappush(path_pq, (current_cost + node[1], aux_path))
            if node[0] == e:
                return path_to_arcset(aux_path)
    return []

def compute_network():
    for i in range(0, len(network)):
        for j in range(i+1, len(network)):
            aux_path = shortest_path(i,j)
            for pair in aux_path:
                route_arc_flows[pair] += demand_matrix[i][j]

def compute_max_flows():
    current_max = 0
    for i in range(len(route_max_flows)):
        for pair in routes[i]:
            if route_arc_flows[pair] > current_max:
                current_max = route_arc_flows[pair]
        route_max_flows[i] = current_max
        current_max = 0

def get_bus_number():
    num = 0
    for i in range(len(routes)):
        route_freq[i] = route_max_flows[i]/CAP
        num += math.ceil((route_times[i]*2*route_max_flows[i])/(CAP*60))
    print(num)

for r in routes:
    for pair in r:
        route_arc_flows[pair] = 0

compute_network()
compute_max_flows()
get_bus_number()
with open('data/route_freq1.json', 'w') as freq_file:
    json.dump(route_freq, freq_file)