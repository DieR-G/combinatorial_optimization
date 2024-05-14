from collections import defaultdict
import numpy as np
import datetime
import json

DEMAND_MATRIX_FILE = "obj_func_data/Mandl/demand_matrix.json"
ROAD_NETWORK_FILE = "obj_func_data/Mandl/network.json"
CAP = 40*1.25
TRANSFER_TIME = 5
ZERO_TRANSFER_MAX = 1.5
ONE_TRANSFER_MAX = 1.1
TWO_TRANSFER_MAX = 1.1
DELTA_F = 0.1

def load_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

demand_matrix = np.array(load_file(DEMAND_MATRIX_FILE))
network = load_file(ROAD_NETWORK_FILE)

TOTAL_DEMAND = np.sum(demand_matrix)

def frequency_deviation(f, o):
    sq_diff = 0
    for i in range(len(f)):
        sq_diff += (f[i]-o[i])**2
    return sq_diff**0.5

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

def filter_trips_by_class(filtered_routes):
    trip_classes = defaultdict(list)
    for trip in filtered_routes:
        trip_classes[trip[0]].append(trip)
    return trip_classes

def compute_0_time(i, j, Ri, Rj, routes, frequencies, arcs):
    possible_routes = set(Ri).intersection(Rj)
    t_cij = get_min_time(i, j, possible_routes, routes)
    filtered_routes = list(filter(lambda x: compute_time(i, j, routes[x]) < t_cij*ZERO_TRANSFER_MAX, possible_routes))
    total_freq = sum([frequencies[i] for i in filtered_routes])
    tt = 0
    wt = 0
    for k in filtered_routes:
        P_ijk = frequencies[k]/total_freq
        tt += P_ijk*compute_time(i, j, routes[k])
        wt += P_ijk*60/(2*total_freq)
        for arc in get_path(i, j, routes[k]):
            arcs[k][arc] += P_ijk*demand_matrix[i][j]
    return tt, wt

def compute_1_time(i, j, Ri, Rj, routes, input_freq, arcs):
    tt,wt,trt = 0,0,0
    possible_routes = [(ri, rj) for ri in Ri for rj in Rj if set(routes[ri]).intersection(routes[rj])]
    possible_transfers = [(p[0], p[1], tf) for p in possible_routes for tf in set(routes[p[0]]).intersection(routes[p[1]])]

    min_time = min(
        compute_time(i, p[2], routes[p[0]]) + compute_time(p[2], j, routes[p[1]]) + 60/(2*input_freq[p[0]]) + 60/(2*input_freq[p[1]]) + TRANSFER_TIME 
        for p in possible_transfers
    )

    filtered_routes = [
        p for p in possible_transfers
        if compute_time(i, p[2], routes[p[0]]) + compute_time(p[2], j, routes[p[1]]) + 60/(2*input_freq[p[0]]) + 60/(2*input_freq[p[1]]) + TRANSFER_TIME
        < ONE_TRANSFER_MAX * min_time
    ]

    trip_classes = filter_trips_by_class(filtered_routes)

    total_class_frequency = sum(input_freq[x] for x in trip_classes)
    for key, value in trip_classes.items():
        P_ijk = input_freq[key] / total_class_frequency
        travel, transfer = 0, 0
        for depart, arrive, transfer_node in value:
            P_ijkm = 1/len(value)
            P_ijkm *= P_ijk
            travel += P_ijkm * (
                    compute_time(i, transfer_node, routes[depart]) +
                    compute_time(transfer_node, j, routes[arrive])
            )
            wt += P_ijkm*(60 / (2*input_freq[depart]))
            wt += P_ijkm*(60 / (2*input_freq[arrive]))
            transfer += TRANSFER_TIME * P_ijkm

            for arc in get_path(i, transfer_node, routes[depart]):
                arcs[depart][arc] += P_ijkm * demand_matrix[i][j]

            for arc in get_path(transfer_node, j, routes[arrive]):
                arcs[arrive][arc] +=  P_ijkm * demand_matrix[i][j]
        tt += travel
        trt += transfer

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
    trip_classes = filter_trips_by_class(filtered_routes)

    total_class_frequency = sum(input_freq[x] for x in trip_classes)

    for key, value in trip_classes.items():
        P_ijk = input_freq[key] / total_class_frequency
        travel, transfer = 0, 0
        for r1, r2, r3, tf1, tf2 in value:
            P_ijkm = 1 / len(value)
            P_ijkm *= P_ijk
            travel += P_ijkm * (
                    compute_time(i, tf1, routes[r1]) +
                    compute_time(tf1, tf2, routes[r3]) +
                    compute_time(tf2, j, routes[r2])
            )
            wt += P_ijkm*(60 / (2 * input_freq[r1]))
            wt += P_ijkm*(60 / (2 * input_freq[r2]))
            wt += P_ijkm*(60 / (2 * input_freq[r3]))
            
            transfer += 2 * TRANSFER_TIME * P_ijkm

            for arc in get_path(tf2, j, routes[r2]):
                arcs[r2][arc] += P_ijkm * demand_matrix[i][j]

            for arc in get_path(tf1, tf2, routes[r3]):
                arcs[r3][arc] += P_ijkm * demand_matrix[i][j]
                
            for arc in get_path(i, tf1, routes[r1]):
                arcs[r1][arc] += P_ijkm * demand_matrix[i][j]
            
        #wt += P_ijk * waiting
        tt +=  travel
        trt += transfer
        #wt +=  P_ijk * 60 / (2 * total_class_frequency)

    return tt, wt, trt

def update_frequencies(frequencies, arcs):
    for i, _ in enumerate(frequencies):
        val = max(arcs[i], key = arcs[i].get)
        frequencies[i] = arcs[i][val]/CAP
        #print(f"Maximum flow: {frequencies[i]*CAP} in {val}")

def assign(routes, frequencies):
    print("\n")
    D_NS = 0
    D_0 = 0
    D_1 = 0
    D_2 = 0
    output_freq = frequencies
    input_freq = output_freq
    total_tt, total_wt, total_trt = 0, 0, 0
    iterations = 0
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
                        #print((i, j), wt*demand_matrix[i][j])
                    elif is_one_transfer(Ri, Rj, routes):
                        D_1 += demand_matrix[i][j]/TOTAL_DEMAND
                        tt, wt, trt = compute_1_time(i, j, Ri, Rj, routes, input_freq, arcs)
                        total_tt += tt*demand_matrix[i][j]
                        total_wt += wt*demand_matrix[i][j]
                        total_trt += trt*demand_matrix[i][j]
                        #print((i, j), wt*demand_matrix[i][j])
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
        iterations += 1
    print(iterations)
    buses = 0
    for e, r in enumerate(routes):
        buses += output_freq[e]*(compute_time(r[0], r[-1], r)/30)
    print(f"Travel time: {total_tt}\t Waiting time: {total_wt}\t Transfer time: {total_trt}\n Frequencies:{output_freq} \n Buses:{buses}")
    print("\n")

#ts = datetime.datetime.now()
#assign([[10,12,13,9,7,14,5,2,1,0],[6,14,5,3,4],[11,3,5,14,8]], [10,1,1])
#te = datetime.datetime.now()
#print(te-ts)

#assign([[10,12,13,9,7,14,5,2,1,0],[6,14,5,3,4],[11,3,5,14,8]], [10, 10, 10])
ts = datetime.datetime.now()
assign([[0,1,2,5,7,9,10,12], [4,3,5,7,14,6], [11,3,5,14,8],[9,13,12]], [10,10,10,10])
te = datetime.datetime.now()
print(te - ts)
#assign([[9,13,12]], [10])
#assign([[0,1,2,5,7,9,10,12]],[1])
#assign([[0,1,2,5,7,9,10]], [10])
#assign([[0,1,2,5,7,9,10,12],[4,3,5,7,14,6],[11,3,5,14,8],[9,13,12]],[1,1,1,1])
#assign([[6,14,7,9,10,11],[6,14,5,7,9,13,12],[0,1,2,5,7],[8,14,6,9],[4,3,5,7,9],[0,1,2,5,14,8]],[35,35,35,35,35,35])
#assign([[9,12],[9,10,11],[9,13],[0,1,2,5,7,9],[8,14,6,9],[4,3,5,7,9],[0,1,3,4]],[100,100,100,100,100,100,100])
#assign([[0,1,3,11,10,12,13],[2,5,7,14,6,9],[9,10,12],[9,10,11],[7,9,13],[0,1,3,5],[8,14,5,7,9],[4,1,2,5,14,6,9]],[100,100,100,100,100,100,100,100])
#x = sum([demand_matrix[y][x] for y in [0,1,2,5,7,9,10,12] for x in [0,1,2,5,7,9,10,12]]) * 60/(2*38) 
#print(x)