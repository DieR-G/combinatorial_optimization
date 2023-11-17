import heapq as hpq
import json
import math
from statistics import mean

network_file = 'data/bus_assign_network1.json'
routes_file = 'data/route_assign1.json'
route_nodes_file = 'data/route_nodes1.json'
route_freq_file = 'data/route_freq1.json'
network = []

with open(network_file, 'r') as net_file:
    network = json.load(net_file)

network = [[ tuple(y) for y in x ] for x in network]
routes = []
with open(routes_file, 'r') as rout_file:
    routes = json.load(rout_file)

routes = [[ tuple(y) for y in x] for x in routes]

route_nodes = []

with open(route_nodes_file, 'r') as node_file:
    route_nodes = [ set(ri) for ri in json.load(node_file)]

route_arcs = [(ri[0: int(len(ri)/2)], ri[int(len(ri)/2):len(ri)]) for ri in routes]

route_arc_flows = [{} for _ in range(len(routes))]

route_max_flows = [0]*len(routes)

route_freq = []

with open(route_freq_file, 'r') as freq_file:
    route_freq = json.load(freq_file)
output_freq = [0]*len(route_freq)

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
TRANSFER_TIME = 5

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

def compute_max_flows():
    current_max = 0
    for i in range(len(route_max_flows)):
        for pair in routes[i]:
            if route_arc_flows[i][pair] > current_max:
                current_max = route_arc_flows[i][pair]
        route_max_flows[i] = current_max
        current_max = 0

def get_bus_number(freq):
    num = 0
    for i in range(len(routes)):
        freq[i] = route_max_flows[i]/CAP
        num += math.ceil((route_times[i]*route_max_flows[i])/(CAP*30))
    return num

def is_0_transfer(i,j):
    ans = []
    for r in range(len(route_nodes)):
        if i in route_nodes[r] and j in route_nodes[r]:
            ans.append(r)
    return ans

def is_1_transfer(i, j):
    ans = []
    for r1 in range(len(route_nodes)):
        for r2 in range(len(route_nodes)):
            if i in route_nodes[r1] and j in route_nodes[r2] and r1 != r2:
                common = route_nodes[r1].intersection(route_nodes[r2]) 
                if len(common) > 0:
                    ans.append((r1, r2))
    return ans

def is_2_transfer(i, j):
    ans = []
    for r1 in range(len(route_nodes)):
        for r2 in range(len(route_nodes)):
            for r3 in range(len(route_nodes)):
                if r1 == r2 or r1 == r3 or r2 == r3: continue
                if i in route_nodes[r1] and j in route_nodes[r3]:
                    common1 = route_nodes[r1].intersection(route_nodes[r2])
                    common2 = route_nodes[r2].intersection(route_nodes[r3])
                    if common1 and common2:
                        ans.append((r1, r2, r3))
    return ans

def build_path(i,j,route):
    direction = 0
    s = next((x for x, v in enumerate(route[direction]) if v[0] == i), -1)
    e = next((x for x, v in enumerate(route[direction]) if v[1] == j and x >= s), -1)
    if s < 0 or e < 0:
        direction = 1
        s = next((x for x, v in enumerate(route[direction]) if v[0] == i), -1)
        e = next((x for x, v in enumerate(route[direction]) if v[1] == j and x >= s), -1)
    arc_list = []
    arc_list += route[direction][s:e+1]
    return arc_list

def build_transfer(i, j, pair):
    r1_transfer = []
    r2_transfer = []
    common = route_nodes[pair[0]].intersection(route_nodes[pair[1]])
    min_time = 1000000
    for node in common:
        auxr1 = build_path(i, node, route_arcs[pair[0]])
        auxr2 = build_path(node, j, route_arcs[pair[1]])
        aux = calc_path_time(auxr1) + calc_path_time(auxr2)
        if aux < min_time:
            min_time = aux
            r1_transfer = auxr1.copy()
            r2_transfer = auxr2.copy()
    return r1_transfer, r2_transfer

def build_transfer_2(i, j, triple):
    r1_transfer = []
    r2_transfer = []
    r3_transfer = []
    common1 = route_nodes[triple[0]].intersection(route_nodes[triple[1]])
    min_time = 1000000
    for node in common1:
        auxr1 = build_path(i, node, route_arcs[triple[0]])
        auxr2, auxr3 = build_transfer(node, j, (triple[1], triple[2]))
        aux = calc_path_time(auxr1) + calc_path_time(auxr2) + calc_path_time(auxr3)
        if aux < min_time:
            min_time = aux
            r1_transfer = auxr1.copy()
            r2_transfer = auxr2.copy()
            r3_transfer = auxr3.copy()
    return r1_transfer, r2_transfer, r3_transfer

def update_arc_flows(val, path, r):
    for p in path:
        route_arc_flows[r][p] += val

def compute_0_transfer_time(i, j, possible_routes, freq):
    total_freq = 0
    total_time = 0
    total_wait_time = 0
    pi = 0
    for r in possible_routes:
        total_freq += freq[r]
    for r in possible_routes:
        pi = demand_matrix[i][j]*(freq[r]/total_freq)
        current_path = build_path(i,j,route_arcs[r])
        update_arc_flows(pi, current_path, r)
        travel_time = calc_path_time(current_path)
        wait_time = 30/total_freq
        total_wait_time += wait_time*pi
        total_time += (travel_time)*pi
    return total_time, total_wait_time, 0

def compute_1_transfer_time(i, j, possible_routes, freq):
    total_freq = 0
    total_time = 0
    total_wait_time = 0
    total_transfer_time = 0
    travel_time = 0
    wait_time = 0
    trip_classes = {}
    for p in possible_routes:
        if p[0] not in trip_classes:
            trip_classes[p[0]] = []
            total_freq += freq[p[0]]
        trip_classes[p[0]].append(p)
    for key, val in trip_classes.items():
        travel_time = 0
        wait_time = 30/total_freq
        demand_factor = 1/len(val)
        for r in val:
            pi = demand_matrix[i][j]*freq[key]/total_freq*demand_factor
            path_r1, path_r2 = build_transfer(i, j, r)
            update_arc_flows(pi, path_r1, r[0])
            update_arc_flows(pi, path_r2, r[1])
            travel_time += calc_path_time(path_r1 + path_r2)
            wait_time += 30/freq[r[1]]
            total_wait_time += wait_time*pi
            total_transfer_time += TRANSFER_TIME*pi
            total_time += (travel_time)*pi
    return total_time, total_wait_time, total_transfer_time

def compute_2_transfer_time(i, j, possible_routes, freq):
    total_freq = 0
    total_time = 0
    travel_time = 0
    wait_time = 0
    total_wait_time = 0
    total_transfer_time = 0
    trip_classes = {}
    for p in possible_routes:
        if p[0] not in trip_classes:
            trip_classes[p[0]] = []
            total_freq += freq[p[0]]
        trip_classes[p[0]].append(p)
    for key, val in trip_classes.items():
        travel_time = 0
        wait_time = 30/total_freq
        demand_factor = 1/len(val)
        for r in val:
            pi = demand_matrix[i][j]*freq[key]/total_freq*demand_factor
            path_r1, path_r2, path_r3 = build_transfer_2(i, j, r)
            update_arc_flows(pi, path_r1, r[0])
            update_arc_flows(pi, path_r2, r[1])
            update_arc_flows(pi, path_r3, r[2])
            travel_time += calc_path_time(path_r1 + path_r2 + path_r3)
            wait_time += 30/freq[r[1]]+30/freq[r[2]]
            total_wait_time = wait_time*pi
            total_transfer_time = 2*TRANSFER_TIME*pi
            total_time += (travel_time)*pi
    return total_time, total_wait_time, total_transfer_time

def evaluate(routes, freq):
    total = {'tv':0, 'te':0, 'tt':0}
    a = 0
    b = 0
    c = 0
    for r in range(len(routes)):
        for pair in routes[r]:
            route_arc_flows[r][pair] = 0
    for i in range(len(network)):
        for j in range(len(network)):
            if demand_matrix[i][j] == 0: continue
            x = is_0_transfer(i,j)
            y = is_1_transfer(i,j)
            z = is_2_transfer(i, j)
            if x:
                a,b,c = compute_0_transfer_time(i, j, x, freq)
                total['tv'] += a
                total['te'] += b
                total['tt'] += c
            elif y:
                a,b,c = compute_1_transfer_time(i, j, y, freq)
                total['tv'] += a
                total['te'] += b
                total['tt'] += c
            elif z:
                a,b,c = compute_2_transfer_time(i, j, z, freq)
                total['tv'] += a
                total['te'] += b
                total['tt'] += c
            else:
                print('unsatisfied demand', (i,j))
    return total

def f(routes, input_freq):
    ans = {}
    while True:
        output_freq = input_freq.copy()
        ans = evaluate(routes, input_freq)
        compute_max_flows()
        buses = get_bus_number(output_freq)
        u1 = mean(output_freq)
        u2 = mean(input_freq)
        if abs(u1 - u2) < 1:
            break
        input_freq = output_freq.copy()

    return ans, output_freq, buses

s, fr, n = f(routes, route_freq)

print(s['tv']+s['te']+s['tt'],n)