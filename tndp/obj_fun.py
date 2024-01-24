import math
from statistics import mean
import numpy as np
CAP = 40*1.25
TRANSFER_TIME = 5
ZERO_TRANSFER_MAX = 1.5
ONE_TRANSFER_MAX = 1.1
TWO_TRANSFER_MAX = 1.1
DELTA_F = 0.1

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
    [(12, 5), (9, 5), (11, 10)], 
    [(3, 10), (10, 10)], 
    [(13, 2), (10, 5), (9, 10)], 
    [(12, 2), (9, 8)], 
    [(7, 2), (6, 2), (5, 3), (8, 8)]
]

def frequency_deviation(f, o):
    return abs(mean(f) - mean(o))

def get_arcs_flow(routes):
    arcs = [{a:0 for x in range(len(r)-1) for a in ((r[x],r[x+1]),(r[x+1],r[x]))} for r in routes]
    return arcs

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
        wt += 60/(2*total_freq)
        for arc in get_path(i, j, routes[k]):
            arcs[k][arc] += P_ijk*demand_matrix[i][j]
    return tt, wt

def compute_1_time(i, j, Ri, Rj, routes, input_freq, arcs):
    tt,wt,trt = 0,0,0
    possible_routes = [(ri, rj) for ri in Ri for rj in Rj if set(routes[ri]).intersection(routes[rj])]
    possible_transfers = [(p[0], p[1], tf) for p in possible_routes for tf in set(routes[p[0]]).intersection(routes[p[1]])]

    min_time = min(
        compute_time(i, p[2], routes[p[0]]) + compute_time(p[2], j, routes[p[1]]) +
        60 / (2 * input_freq[p[0]]) + 60 / (2 * input_freq[p[1]]) + TRANSFER_TIME
        for p in possible_transfers
    )

    filtered_routes = [
        p for p in possible_transfers
        if compute_time(i, p[2], routes[p[0]]) + compute_time(p[2], j, routes[p[1]]) +
           60 / (2 * input_freq[p[0]]) + 60 / (2 * input_freq[p[1]]) + TRANSFER_TIME <
           ONE_TRANSFER_MAX * min_time
    ]

    trip_classes = {route: [(r, _, transfer_node) for r, _, transfer_node in filtered_routes if r == route]
                    for route in set(r for r, _, _ in filtered_routes)}

    total_class_frequency = sum(input_freq[x] for x in trip_classes)

    for key, value in trip_classes.items():
        P_ijk = input_freq[key] / total_class_frequency
        travel, waiting, transfer = 0, 0, 0

        for depart, arrive, transfer_node in value:
            P_ijkm = 1 / len(value)
            travel += P_ijkm * (
                    compute_time(i, transfer_node, routes[depart]) +
                    compute_time(transfer_node, j, routes[arrive])
            )
            waiting += P_ijkm * (60 / (2 * input_freq[arrive]))
            transfer += TRANSFER_TIME * P_ijkm

            for arc in get_path(transfer_node, j, routes[arrive]):
                arcs[arrive][arc] += P_ijk * P_ijkm * demand_matrix[i][j]

        for arc in get_path(i, transfer_node, routes[depart]):
            arcs[depart][arc] += P_ijk * demand_matrix[i][j]

        tt += P_ijk * travel
        wt += P_ijk * waiting
        trt += P_ijk * transfer
        wt += P_ijk * 60 / (2 * total_class_frequency)

    return tt, wt, trt

def compute_2_time(i, j, Ri, Rj, routes, input_freq, arcs):
    tt, wt, trt = 0, 0, 0

    aux_set = set(Ri).union(Rj)
    complement = [e for (e, _) in enumerate(routes) if e not in aux_set]

    possible_routes = [
        (r1, r2, r3) 
        for r1 in Ri 
        for r2 in Rj 
        for r3 in complement 
        if set(routes[r3]).intersection(routes[r1]) and set(routes[r3]).intersection(routes[r2])
    ]

    possible_transfers = [
        (r1, r2, r3, tf1, tf2) 
        for (r1, r2, r3) in possible_routes 
        for tf1 in set(routes[r3]).intersection(routes[r1]) 
        for tf2 in set(routes[r3]).intersection(routes[r2])
    ]

    min_time = min(
        compute_time(i, tf1, routes[r1]) + compute_time(tf1, tf2, routes[r3]) + 
        compute_time(tf2, j, routes[r2]) + 
        60 / (2 * input_freq[r1]) + 60 / (2 * input_freq[r2]) + 60 / (2 * input_freq[r3]) + 
        2 * TRANSFER_TIME 
        for (r1, r2, r3, tf1, tf2) in possible_transfers
    )

    filtered_routes = [
        (r1, r2, r3, tf1, tf2) 
        for (r1, r2, r3, tf1, tf2) in possible_transfers 
        if compute_time(i, tf1, routes[r1]) + compute_time(tf1, tf2, routes[r3]) + 
           compute_time(tf2, j, routes[r2]) + 
           60 / (2 * input_freq[r1]) + 60 / (2 * input_freq[r2]) + 60 / (2 * input_freq[r3]) + 
           2 * TRANSFER_TIME < TWO_TRANSFER_MAX * min_time
    ]

    trip_classes = {route: [(r1, r2, r3, tf1, tf2) for r1, r2, r3, tf1, tf2 in filtered_routes if r1 == route]
                    for route in set(r1 for r1, _, _, _, _ in filtered_routes)}

    total_class_frequency = sum(input_freq[x] for x in trip_classes)

    for key, value in trip_classes.items():
        P_ijk = input_freq[key] / total_class_frequency
        travel, waiting, transfer = 0, 0, 0

        for r1, r2, r3, tf1, tf2 in value:
            P_ijkm = 1 / len(value)
            travel += P_ijkm * (
                    compute_time(i, tf1, routes[r1]) +
                    compute_time(tf1, tf2, routes[r3]) +
                    compute_time(tf2, j, routes[r2])
            )
            waiting += P_ijkm * (60 / (2 * input_freq[r2]))
            transfer += 2 * TRANSFER_TIME * P_ijkm

            for arc in get_path(tf2, j, routes[r2]):
                arcs[r2][arc] += P_ijk * P_ijkm * demand_matrix[i][j]

            for arc in get_path(i, tf1, routes[r1]):
                arcs[r1][arc] += P_ijk * demand_matrix[i][j]

            for arc in get_path(tf1, tf2, routes[r3]):
                arcs[r3][arc] += P_ijk * P_ijkm * demand_matrix[i][j]

        wt += P_ijk * waiting
        tt += P_ijk * travel
        trt += P_ijk * transfer
        wt += P_ijk * 60 / (2 * total_class_frequency)

    return tt, wt, trt


def update_frequencies(frequencies, arcs):
    for i, _ in enumerate(frequencies):
        frequencies[i] = arcs[i][max(arcs[i], key = arcs[i].get)]/CAP

def assign(routes, frequencies):
    print("\n")
    D_NS = 0
    D_0 = 0
    D_1 = 0
    D_2 = 0
    output_freq = frequencies
    input_freq = output_freq
    total_tt, total_wt, total_trt = 0, 0, 0
    while True:
        arcs = []
        arcs = get_arcs_flow(routes)
        input_freq = output_freq.copy()
        total_tt, total_wt, total_trt = 0, 0, 0
        D_0, D_1, D_2, D_NS = 0, 0, 0, 0
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
                        tt, wt, trt = compute_1_time(i, j, Ri, Rj, routes, input_freq, arcs)
                        total_tt += tt*demand_matrix[i][j]
                        total_wt += wt*demand_matrix[i][j]
                        total_trt += trt*demand_matrix[i][j]
                    elif is_two_transfer(Ri, Rj, routes):
                        D_2 += demand_matrix[i][j]/TOTAL_DEMAND
                        tt, wt, trt = compute_2_time(i, j, Ri, Rj, routes, input_freq, arcs)
                        total_tt += tt*demand_matrix[i][j]
                        total_wt += wt*demand_matrix[i][j]
                        total_trt += trt*demand_matrix[i][j]
                    else:
                        D_NS += demand_matrix[i][j]/TOTAL_DEMAND
        update_frequencies(output_freq, arcs)
        if frequency_deviation(input_freq, output_freq) < DELTA_F:
            break
    print(f"Travel time: {total_tt}\t Waiting time: {total_wt}\t Transfer time: {total_trt}")
    print("\n")

def test_assign(routes, frequencies):
    print("\n")
    D_NS = 0
    D_0 = 0
    D_1 = 0
    D_2 = 0
    output_freq = frequencies
    input_freq = output_freq
    arcs = get_arcs_flow(routes)
    total_tt, total_wt, total_trt = 0, 0, 0
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
                    tt, wt, trt = compute_1_time(i, j, Ri, Rj, routes, input_freq, arcs)
                    total_tt += tt*demand_matrix[i][j]
                    total_wt += wt*demand_matrix[i][j]
                    total_trt += trt*demand_matrix[i][j]
                elif is_two_transfer(Ri, Rj, routes):
                    D_2 += demand_matrix[i][j]/TOTAL_DEMAND
                    tt, wt, trt = compute_2_time(i, j, Ri, Rj, routes, input_freq, arcs)
                    total_tt += tt*demand_matrix[i][j]
                    total_wt += wt*demand_matrix[i][j]
                    total_trt += trt*demand_matrix[i][j]
                else:
                    D_NS += demand_matrix[i][j]/TOTAL_DEMAND
    print(f"In vehicle time: {total_tt}\t Waiting time: {total_wt}\t Transfer time: {total_trt}")
    print("\n")
    return D_0, D_1, D_2, D_NS

#print(test_assign([[0,1,2,5,7,9,10,12],[4,3,5,7,14,6],[11,3,5,14,8],[12,13,9]],[10,1,5,1]))
#print(test_assign([[10,12,13,9,7,14,5,2,1,0],[6,14,5,3,4],[11,3,5,14,8]], [1,10,1]))
#print(test_assign([[6,14,7,9,10,11],[6,14,5,7,9,13,12],[0,1,2,5,7],[8,14,6,9],[4,3,5,7,9],[0,1,2,5,14,8]],[1,1,1,1,1,1]))

assign([[10,12,13,9,7,14,5,2,1,0],[6,14,5,3,4],[11,3,5,14,8]], [1,1,1])
assign([[0,1,2,5,7,9,10,12],[4,3,5,7,14,6],[11,3,5,14,8],[12,13,9]],[10,1,5,1])
assign([[6,14,7,9,10,11],[6,14,5,7,9,13,12],[0,1,2,5,7],[8,14,6,9],[4,3,5,7,9],[0,1,2,5,14,8]],[35,35,35,35,35,35])
assign([[9,12],[9,10,11],[9,13],[0,1,2,5,7,9],[8,14,6,9],[4,3,5,7,9],[0,1,3,4]],[100,100,100,100,100,100,100])
assign([[0,1,3,11,10,12,13],[2,5,7,14,6,9],[9,10,12],[9,10,11],[7,9,13],[0,1,3,5],[8,14,5,7,9],[4,1,2,5,14,6,9]],[100,100,100,100,100,100,100,100])