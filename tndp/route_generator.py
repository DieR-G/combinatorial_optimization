import math
import copy
import time
from class_objective_function import Tndp
import heapq as hpq
from drawtest import GraphVisualizer

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

PENALTY = 10000

def path_to_arcset(path):
    arcs_set=[]
    for i in range(len(path)-1):
        arcs_set.append((path[i], path[i+1]))
    return arcs_set

arcs = set()

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
    [(12, 3), (9, 5), (11, 10)], 
    [(3, 10), (10, 10)], 
    [(13, 2), (10, 3), (9, 10)], 
    [(12, 2), (9, 8)], 
    [(7, 2), (6, 2), (5, 3), (8, 8)]
]

arcset = [(p[0], v[0]) for p in enumerate(network) for v in p[1]]
arcset = set([(x,y) for x,y in arcset]+[(y,x) for x,y in arcset]) 



for i in range(len(network)):
    for j in range(len(network[i])):
        arcs.add((i, network[i][j][0]))
        arcs.add((network[i][j][0], i))

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
                    return aux_path
        return []

def generate_routes(s=0, n=2):
    ans = []
    visited = [False]*len(network)
    current_node = 0
    last_node = -1
    for i in range(len(network)):
        routes = []
        if visited[(i + s)%len(network)]:
            continue
        last_node = -1
        current_node = -1
        visiting_nodes = [(i + s)%len(network)]
        while visiting_nodes:
            last_node = current_node
            current_node = visiting_nodes.pop()
            routes.append(current_node)
            if len(routes) > math.ceil(len(network)/n):
                break
            visited[current_node] = True
            for p in network[current_node]:
                if not visited[p[0]]:
                    visiting_nodes.append(p[0])
                    break
                else:
                    if last_node < 0 or not visited[last_node]:
                        visiting_nodes.append(p[0])
                        break
        ans.append(routes)
    return ans

def sub_graph(route_set):
    _network = [ [] for _ in range(15) ]
    arcs = []
    routes = route_set
    for r in routes:
        arcs += path_to_arcset(r)
    for arc in arcs:
        if next(((arc[0], v[1]) for v in network[arc[0]] if v[0] == arc[1]), 0) not in _network[arc[0]]:
            _network[arc[0]].append((arc[1], next((v[1] for v in network[arc[0]] if v[0] == arc[1]), 0)))
        if next(((arc[1], v[1]) for v in network[arc[0]] if v[0] == arc[1]), 0) not in _network[arc[1]]:
            _network[arc[1]].append((arc[0], next((v[1] for v in network[arc[1]] if v[0] == arc[0]), 0)))
    return _network

def try_connect(r1, r2):
    if len(r1) > len(r2):
        r1, r2 = r2, r1
    for node in r2:
        if (node, r1[0]) in arcs:
            r1.insert(0, node)
            return True
        for i in range(0, len(r1)-1):
            if (r1[i], node) in arcs and (node, r1[i+1]) in arcs:
                r1.insert(i, node)
                return True
        if (r1[len(r1)-1], node) in arcs:
            r1.insert(len(r1), node)
            return True
    return False

def process_routes(routes):
    for i in range(len(routes)):
        for j in range(len(routes)):
            if i == j:
                continue
            if not set(routes[i]).intersection(routes[j]):
                if try_connect(routes[i], routes[j]):
                    break
def conct(x):
            y = x.copy()
            y.pop()
            y.reverse()
            return x+y

def connect_nodes(routes, unconnected):
    candidates = []
    filtered = []
    for i,j in unconnected:
        candidates.append(shortest_path(i,j))
    for r1 in range(len(candidates)):
        for r2 in range(len(candidates)):
            if r1 == r2: continue
            if not set(candidates[r2]).issubset(candidates[r1]) and candidates[r2] not in filtered:
                filtered.append(candidates[r2])
    routes += filtered

def insert_operator(min_val, initial_r, initial_f, tabu_list = set(), min_bus = 1000):
    best_r, best_f = copy.deepcopy(initial_r), copy.deepcopy(initial_f)
    best_b, best_bf = copy.deepcopy(initial_r), copy.deepcopy(initial_f)
    for r1 in range(len(initial_r)):
        for r2 in range(len(initial_r)):
            if(r1 == r2):
                continue
            for i in range(len(initial_r[r1])):
                for j in range(len(initial_r[r2])):
                    insertable = True
                    if initial_r[r1][i] in initial_r[r2]:
                        continue
                    initial_r[r2].insert(j, initial_r[r1][i])
                    if j > 0:
                        if (initial_r[r2][j-1], initial_r[r2][j]) not in arcset:
                            insertable = False                    
                    if j < len(initial_r[r2]) + 1:
                        if (initial_r[r2][j], initial_r[r2][j+1]) not in arcset:
                            insertable = False
                    if insertable:
                        instance = Tndp(initial_r, initial_f)
                        res = instance.f()
                        val_f = round(res[0]['tv']+res[0]['te']+res[0]['tt'], 5)
                        val_b = res[2]
                        if val_b < min_bus and (val_f, val_b) not in tabu_list:
                            min_bus = res[2]
                            best_b, best_bf = copy.deepcopy(initial_r), res[1]
                            tabu_list.add((val_f, val_b))
                        if val_f < min_val and (val_f, val_b) not in tabu_list:
                            min_val = res[0]['tv']+res[0]['te']+res[0]['tt']
                            best_r, best_f = copy.deepcopy(initial_r), res[1]         
                            tabu_list.add((val_f, val_b))
                        else:
                            del initial_r[r2][j]
                    else:
                        del initial_r[r2][j]
    return min_val, best_r, best_f, min_bus, best_b, best_bf

def exchange_operator(min_val, initial_r, initial_f, tabu_list = set(), min_bus = 1000):
    best_r, best_f = copy.deepcopy(initial_r), copy.deepcopy(initial_f)
    best_b, best_bf = copy.deepcopy(initial_r), copy.deepcopy(initial_f)
    for r in initial_r:
        for i in range(len(r)):
            for j in range(i+1, len(r)):
                r[i], r[j] = r[j], r[i]
                exchangeable = True
                if (i > 0):
                    if (r[i-1], r[i]) not in arcset:
                        exchangeable = False
                if (j > 0):
                    if (r[j-1], r[j]) not in arcset:
                        exchangeable = False
                if (i < len(r)-1):
                    if (r[i], r[i+1]) not in arcset:
                        exchangeable = False
                if (j < len(r)-1):
                    if (r[j], r[j+1]) not in arcset:
                        exchangeable = False            
                if exchangeable:
                    instance = Tndp(initial_r, initial_f)
                    res = instance.f()
                    connect_nodes(initial_r, res[3])
                    instance = Tndp(initial_r, [10]*len(initial_r))
                    res = instance.f()
                    val_f = round(res[0]['tv']+res[0]['te']+res[0]['tt'], 5)
                    val_b = res[2]
                    if(res[3]):
                        val_f += len(res[3])*PENALTY
                    if val_b < min_bus and (val_f, val_b) not in tabu_list:
                        min_bus = res[2]
                        best_b, best_bf = copy.deepcopy(initial_r), res[1]
                        tabu_list.add((val_f, val_b))
                    if val_f < min_val and (val_f, val_b) not in tabu_list:
                        min_val = res[0]['tv']+res[0]['te']+res[0]['tt']
                        best_r, best_f = copy.deepcopy(initial_r), res[1]         
                        tabu_list.add((val_f, val_b))
                    else:
                        r[i], r[j] = r[j], r[i]
                else:
                    r[i], r[j] = r[j], r[i]
    return min_val, best_r, best_f, min_bus, best_b, best_bf

def replace_operator(min_val, initial_r, initial_f, tabu_list = set(), min_bus = 1000):
    best_r, best_f = copy.deepcopy(initial_r), copy.deepcopy(initial_f)
    best_b, best_bf = copy.deepcopy(initial_r), copy.deepcopy(initial_f)
    for r1 in range(len(initial_r)):
        for r2 in range(len(initial_r)):
            if r1 == r2:
                continue            
            for i in range(len(initial_r[r1])):
                for j in range(len(initial_r[r2])):
                    if i == j:
                        continue
                    if(i > 0 and i < len(initial_r[r1]) - 1):
                        if (initial_r[r1][i-1],initial_r[r1][i+1]) not in arcset:
                            continue
                    if(initial_r[r1][i], initial_r[r2][j]) not in arcset:
                        continue
                    if(j > 0):
                        if(initial_r[r2][j-1], initial_r[r1][i]) not in arcset:
                            continue
                    if initial_r[r1][i] in initial_r[r2]:
                        continue
                    new_sol = copy.deepcopy(initial_r)
                    new_sol[r2].insert(j, new_sol[r1].pop(i))
                    if len(new_sol[r1]) == 1:
                        del new_sol[r1]
                    res = Tndp(new_sol, initial_f).f()
                    connect_nodes(new_sol, res[3])

                    instance = Tndp(new_sol, [10]*len(new_sol))
                    res = instance.f()
                    val_f = round(res[0]['tv']+res[0]['te']+res[0]['tt'], 5)
                    if(res[3]):
                        val_f += len(res[3])*PENALTY
                    val_b = res[2]
                    if val_b < min_bus and (val_f, val_b) not in tabu_list:
                        min_bus = res[2]
                        best_b, best_bf = copy.deepcopy(new_sol), res[1]
                        tabu_list.add((val_f, val_b))
                    if val_f < min_val and (val_f, val_b) not in tabu_list:
                        min_val = res[0]['tv']+res[0]['te']+res[0]['tt']
                        best_r, best_f = new_sol.copy(), res[1]         
                        tabu_list.add((val_f, val_b))
    return min_val, best_r, best_f, min_bus, best_b, best_bf

def demand_operator(min_val, initial_r, initial_f, tabu_list = set(), min_bus = 1000):
    best_r, best_f = copy.deepcopy(initial_r), copy.deepcopy(initial_f)
    best_b, best_bf = copy.deepcopy(initial_r), copy.deepcopy(initial_f)
    triple_array = []
    for i in range(len(demand_matrix)):
        for j in range(i, len(demand_matrix)):
            if i == j:
                continue
            hpq.heappush(triple_array, (demand_matrix[i][j], i, j))
    priority = hpq.nlargest(10, triple_array)
    for triple in priority:
        new_path = shortest_path(triple[1], triple[2])
        initial_r.append(new_path)
        instance = Tndp(initial_r, [10]*len(initial_r))
        res = instance.f()
        val_f = round(res[0]['tv']+res[0]['te']+res[0]['tt'], 5)
        val_b = res[2]
        if val_b < min_bus and (val_f, val_b) not in tabu_list:
            min_bus = res[2]
            best_b, best_bf = copy.deepcopy(initial_r), res[1]
            tabu_list.add((val_f, val_b))
        if val_f < min_val and (val_f, val_b) not in tabu_list:
            min_val = res[0]['tv']+res[0]['te']+res[0]['tt']
            best_r, best_f = copy.deepcopy(initial_r), res[1]         
            tabu_list.add((val_f, val_b))
        initial_r.remove(new_path)
    return min_val, best_r, best_f, min_bus, best_b, best_bf

def apply_operator(upper_bound, routes, frequencies, operator, tabu_list = set()):
    return operator(upper_bound, routes.copy(), frequencies.copy(), tabu_list)

def compute():
    tabu_list = set()
    bests_r = [[[], []] for _ in range(len(network))]
    for i in range(len(network)):
        print(i)
        route_nodes = generate_routes(i)
        process_routes(route_nodes)
        instance = Tndp(route_nodes, [100]*len(route_nodes))
        res = instance.f()
        connect_nodes(route_nodes, res[3])
        instance = Tndp(route_nodes, [100]*len(route_nodes))
        res = instance.f()
        val = res[0]['tv']+res[0]['tt']+res[0]['te']
        print(route_nodes, res)
        s=0
        b=0
        r1 = route_nodes
        f1 = [100]*len(route_nodes)
        bests_r[i][0] = (val, copy.deepcopy(r1))
        bests_r[i][1] = (res[2], copy.deepcopy(r1))
        min_val = 1000000000
        minb = 10000
        for _ in range(2):
            try:
                # s, r1, f1, b, rb1, rbf1 = apply_operator(1e9, r1, f1, insert_operator, tabu_list)
                # print(s, b)
                # if(s < min_val):
                #     min_val = s
                #     bests_r[i][0] = (min_val, copy.deepcopy(r1))
                # if(b < minb):
                #     minb = b
                #     bests_r[i][1] = (minb, copy.deepcopy(rb1))
                s, r1, f1, b, rb1, rbf1 = apply_operator(1e9, r1, f1, replace_operator, tabu_list) 
                if(s < min_val):
                    min_val = s
                    bests_r[i][0] = (min_val, copy.deepcopy(r1))
                if(b < minb):
                    minb = b
                    bests_r[i][1] = (minb, copy.deepcopy(rb1))
                # s, r1, f1, b, rb1, rbf1 = apply_operator(1e9, r1, f1, exchange_operator, tabu_list) 
                # if(s < min_val):
                #     min_val = s
                #     bests_r[i][0] = (min_val, copy.deepcopy(r1))
                # if(b < minb):
                #     minb = b
                #     bests_r[i][1] = (minb, copy.deepcopy(rb1)) 
            except:
                continue
    for i in range(len(bests_r)):
        s, r1, f1, b, rb1, rbf1 = 0, bests_r[i][0][1], [10]*len(bests_r[i][0][1]), 1000, bests_r[i][1][1], [10]*len(bests_r[i][1][1])
        s, r1, f1, b, rb1, rbf1 = apply_operator(1e9, r1, f1, demand_operator, tabu_list)
        s, r1, f1, b, rb1, rbf1 = apply_operator(1e9, rb1, rbf1, demand_operator, tabu_list)
        print("buscando: ", s, b)
        if(s < min_val):
                min_val = s
                bests_r[i][0] = (min_val, copy.deepcopy(r1))
                print("mejorado: ", s)
        if(b < minb):
            minb = b
            bests_r[i][1] = (minb, copy.deepcopy(rb1))
            print("mejorado2: ", b)
    for i in range(len(bests_r)):
        exploring_route_val = bests_r[i][0][1]
        instance = Tndp(exploring_route_val, [10]*len(exploring_route_val))
        pairs = instance.get_max_pair()
        exploring_route_val.append([pairs[0], pairs[1]])
        instance = Tndp(exploring_route_val, [10]*len(exploring_route_val))
        print(i)
        print(instance.f())
        print("-------------------------------------")

    
compute()
# start = time.time()
# nodes = [[3, 1, 2, 5, 7, 14, 6, 9, 10], [4, 3, 11, 10, 12, 13], [8, 14], [0, 1, 4], [5,7,9]]
# freqs = [58.48640992998091, 20.4, 6.2, 26.4, 10]
# sol = Tndp(nodes, freqs)
# val = sol.f()
# freqs = val[1]
# buses = [math.ceil(freqs[i]*sol.get_route_time(i)/30) for i in range(len(freqs))]
# print(buses)
# end = time.time()
# print(end - start)
# graph_visualizer = GraphVisualizer(network, [(nodes[i], buses[i]) for i in range(len(nodes))], sol.f()[0]['tv']+sol.f()[0]['te']+sol.f()[0]['tt'])
# graph_visualizer.draw_graph()
# graph_visualizer.save_plot("instance_graph.png", dpi=600)