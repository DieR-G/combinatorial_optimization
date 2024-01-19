import math
from statistics import mean
import numpy as np
CAP = 40*1.25
TRANSFER_TIME = 5
ZERO_TRANSFER_MAX = 1.5
ONE_TRANSFER_MAX = 1.1
TWO_TRANSFER_MAX = 1.1
DELTA_F = 0.5

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

mandl_routes = [[0,1,2,5,7,9,10,12],[4,3,5,7,14,6],[11,3,5,14,8],[12,13,9]]
mandl_frequencies = [10,10,10,10]

def frequency_deviation(f, o):
    return abs(mean(f) - mean(o))

def get_arcs_flow(routes):
    arcs = [{a:0 for x in range(len(r)-1) for a in ((r[x],r[x+1]),(r[x+1],r[x]))} for r in routes]
    return arcs

mandl_arcs = get_arcs_flow(mandl_routes)

def get_path(i, j, r):
    start, end = sorted((r.index(i), r.index(j)))
    pairs = []
    if i < j:
        pairs = [(r[i], r[i+1]) for i in range (start, end)]
    else:
        pairs = [(r[i+1], r[i]) for i in range (start, end)]
    return pairs

def compute_time(i, j, r):
    start, end = sorted((r.index(i), r.index(j)))
    edges = [(network[r[m]], r[m + 1]) for m in range(start, end)]
    cost = sum(list(map(lambda p: next((c for a, c in p[0] if a == p[1]), (0, 0)), edges)))
    return cost
    
def get_min_time(i, j, search_routes, routes):
    return min(map(lambda x: compute_time(i,j,routes[x]), search_routes))

def is_zero_transfer(Ri, Rj):
    possible_routes = set(Ri).intersection(Rj)
    if not possible_routes:
        return False
    return True
    
def is_one_transfer(Ri, Rj, routes):
    for ri in Ri:
        for rj in Rj:
            if set(routes[ri]).intersection(routes[rj]):
                return True

    return False

def is_two_transfer(Ri, Rj, routes):
    aux_set = set(Ri).union(Rj)
    complement = [e for (e, _) in enumerate(routes) if e not in aux_set]
    for r3 in complement:
        for r1 in Ri:
            for r2 in Rj:
                if set(routes[r3]).intersection(routes[r1]) and set(routes[r3]).intersection(routes[r2]):
                    return True
    return False

def compute_0_time(i, j, Ri, Rj, routes, frequencies, arcs):
    possible_routes = set(Ri).intersection(Rj)
    t_cij = get_min_time(i, j, possible_routes, routes)
    filtered_routes = list(filter(lambda x: compute_time(i, j, routes[x]) < t_cij*ONE_TRANSFER_MAX, possible_routes))
    total_freq = sum([frequencies[i] for i in filtered_routes])
    tt = 0
    wt = 0
    for k in filtered_routes:
        P_ijk = frequencies[k]/total_freq
        tt += P_ijk*compute_time(i, j, routes[k])
        wt += 1/2*total_freq
        for arc in get_path(i, j, routes[k]):
            arcs[k][arc] += P_ijk*demand_matrix[i][j]
    return tt, wt
def assign(routes, frequencies):
    D_NS = 0
    D_0 = 0
    D_1 = 0
    D_2 = 0
    output_freq = frequencies
    input_freq = output_freq
    arcs = get_arcs_flow(routes)
    total_tt, total_wt = 0,0
    while True:
        input_freq = output_freq
        for i in range(len(demand_matrix)):
            for j in range(len(demand_matrix)):
                Ri = [e for (e, x) in enumerate(routes) if i in x]
                Rj = [e for (e, x) in enumerate(routes) if j in x]
                if not Ri or not Rj:
                    D_NS += demand_matrix[i][j]/TOTAL_DEMAND
                else:
                    if is_zero_transfer(Ri, Rj):
                        D_0 += demand_matrix[i][j]/TOTAL_DEMAND
                        tt, wt = compute_0_time(i, j, Ri, Rj, routes, input_freq, arcs)
                        total_tt += tt*demand_matrix[i][j]
                        total_wt += wt*demand_matrix[i][j]
                    elif is_one_transfer(Ri, Rj, routes):
                        D_1 += demand_matrix[i][j]/TOTAL_DEMAND
                        #todo: filter and compute times
                    elif is_two_transfer(Ri, Rj, routes):
                        D_2 += demand_matrix[i][j]/TOTAL_DEMAND
                        #todo: filter and compute times
                    else:
                        D_NS += demand_matrix[i][j]/TOTAL_DEMAND
        if frequency_deviation(input_freq, output_freq) < DELTA_F:
            break
    
        
def test_assign(routes, frequencies):
    D_NS = 0
    D_0 = 0
    D_1 = 0
    D_2 = 0
    output_freq = frequencies
    input_freq = output_freq
    arcs = get_arcs_flow(routes)
    total_tt, total_wt = 0,0
    for i in range(len(demand_matrix)):
        for j in range(len(demand_matrix)):
            Ri = [e for (e, x) in enumerate(routes) if i in x]
            Rj = [e for (e, x) in enumerate(routes) if j in x]
            if not Ri or not Rj:
                D_NS += demand_matrix[i][j]/TOTAL_DEMAND
            else:
                if is_zero_transfer(Ri, Rj):
                    D_0 += demand_matrix[i][j]/TOTAL_DEMAND
                    tt, wt = compute_0_time(i, j, Ri, Rj, routes, input_freq, arcs)
                    total_tt += tt*demand_matrix[i][j]
                    total_wt += wt*demand_matrix[i][j]
                elif is_one_transfer(Ri, Rj, routes):
                    D_1 += demand_matrix[i][j]/TOTAL_DEMAND
                    #todo: filter and compute times
                elif is_two_transfer(Ri, Rj, routes):
                    D_2 += demand_matrix[i][j]/TOTAL_DEMAND
                else:
                    D_NS += demand_matrix[i][j]/TOTAL_DEMAND
    print(total_tt, total_wt)
    return D_0, D_1, D_2, D_NS

print(test_assign([[0,1,2,5,7,9,10,12],[4,3,5,7,14,6],[11,3,5,14,8],[12,13,9]],[1,1,1,1]))
print(test_assign(
    [[6,14,7,9,10,11],
    [6,14,5,7,9,13,12],
    [0,1,2,5,7],
    [8,14,6,9],
    [4,3,5,7,9],
    [0,1,2,5,14,8]], [1]*6))