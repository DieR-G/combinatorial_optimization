from collections import defaultdict

ZERO_TRANSFER_MAX = 1.5
ONE_TRANSFER_MAX = 1.1
TWO_TRANSFER_MAX = 1.1

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

def compute_time(i, j, r):
    if i == j:
        return 0
    start, end = sorted((r.index(i), r.index(j)))
    edges = [(network[r[m]], r[m + 1]) for m in range(start, end)]
    cost = sum(list(map(lambda p: next((c for a, c in p[0] if a == p[1]), (0, 0)), edges)))
    return cost

def compute_time_first_bus(i, j, r):
    start, end = r.index(i), r.index(j)
    if(start > end):
        return compute_time(r[-1], i, r)
    return compute_time(r[0], i, r)

def get_min_time(i, j, search_routes, routes):
    return min(map(lambda x: compute_time(i,j,routes[x]), search_routes))    

def get_min_first_route(i, j, search_routes, routes):
    return min(map(lambda x: compute_time_first_bus(i,j,routes[x]), search_routes))

def get_path(i, j, r):
    f_index, s_index = (r.index(i), r.index(j))
    start, end = sorted((f_index, s_index))
    pairs = [r[i] for i in range (start, end+1)]
    if f_index > s_index:
        pairs.reverse()
    return pairs

def get_transfers_routes(i, j, routes):
    Ri = [e for (e, x) in enumerate(routes) if i in x]
    Rj = [e for (e, x) in enumerate(routes) if j in x]
    filtered_routes = []
    if is_zero_transfer(Ri, Rj):
        possible_routes = set(Ri).intersection(Rj)
        t_cij = get_min_time(i, j, possible_routes, routes)
        filtered_routes = list(filter(lambda x: compute_time(i, j, routes[x]) < t_cij*ONE_TRANSFER_MAX, possible_routes))
        filtered_routes = [[j] for _ in filtered_routes]
    elif is_one_transfer(Ri, Rj, routes):
        possible_routes = [(ri, rj) for ri in Ri for rj in Rj if set(routes[ri]).intersection(routes[rj])]
        possible_transfers = [(p[0], p[1], tf) for p in possible_routes for tf in set(routes[p[0]]).intersection(routes[p[1]])]

        min_time = min(
            compute_time(i, p[2], routes[p[0]]) + compute_time(p[2], j, routes[p[1]])
            for p in possible_transfers
        )

        filtered_routes = [
            p for p in possible_transfers
            if compute_time(i, p[2], routes[p[0]]) + compute_time(p[2], j, routes[p[1]]) <
            ONE_TRANSFER_MAX * min_time
        ]
        
        filtered_routes = [
            [j, p[2]]
            for p in filtered_routes]
    
    elif is_two_transfer(Ri, Rj, routes):
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
            compute_time(tf2, j, routes[r2])
            for (r1, r2, r3, tf1, tf2) in possible_transfers
        )

        filtered_routes = [
            (r1, r2, r3, tf1, tf2) 
            for (r1, r2, r3, tf1, tf2) in possible_transfers 
            if compute_time(i, tf1, routes[r1]) + compute_time(tf1, tf2, routes[r3]) + 
            compute_time(tf2, j, routes[r2]) < TWO_TRANSFER_MAX * min_time
        ]

        filtered_routes = [
            [j, p[4], p[3]]
            for p in filtered_routes
        ]
    return filtered_routes #Gives the nodes in reverse

def get_transfers_routes_prop(i, j, routes, frequencies):
    Ri = find_routes_with_node(i, routes)
    Rj = find_routes_with_node(j, routes)
    filtered_routes = []

    if is_zero_transfer(Ri, Rj):
        filtered_routes = handle_zero_transfer(i, j, Ri, Rj, routes, frequencies)
    elif is_one_transfer(Ri, Rj, routes):
        filtered_routes = handle_one_transfer(i, j, Ri, Rj, routes, frequencies)
    elif is_two_transfer(Ri, Rj, routes):
        filtered_routes = handle_two_transfer(i, j, Ri, Rj, routes, frequencies)

    return filtered_routes

def get_complement_routes(Ri, Rj, routes):
    aux_set = set(Ri).union(Rj)
    return [index for index, _ in enumerate(routes) if index not in aux_set]

def get_possible_double_transfers(Ri, Rj, complement, routes):
    return [
        (route1, route2, route3, transfer1, transfer2) for route1 in Ri for route2 in Rj for route3 in complement
        for transfer1 in set(routes[route3]).intersection(routes[route1])
        for transfer2 in set(routes[route3]).intersection(routes[route2])
    ]

def find_routes_with_node(node, routes):
    return [index for index, route in enumerate(routes) if node in route]

def get_possible_transfers(Ri, Rj, routes):
    return [
        (ri, rj, transfer_point) for ri in Ri for rj in Rj
        for transfer_point in set(routes[ri]).intersection(routes[rj])
    ]

def filter_trips_by_class(filtered_routes):
    trip_classes = defaultdict(list)
    for trip in filtered_routes:
        trip_classes[trip[0]].append(trip)
    return trip_classes

def handle_zero_transfer(i, j, Ri, Rj, routes, frequencies):
    possible_routes = set(Ri).intersection(Rj)
    t_cij = get_min_time(i, j, possible_routes, routes)
    filtered_routes = list(filter(lambda x: compute_time(i, j, routes[x]) < t_cij*ZERO_TRANSFER_MAX, possible_routes))
    total_freq = sum([frequencies[i] for i in filtered_routes])
    path_with_proportions = [([j], frequencies[p]/total_freq) for p in possible_routes if compute_time(i, j, routes[p]) < t_cij * ONE_TRANSFER_MAX]
    return path_with_proportions

def handle_one_transfer(i, j, Ri, Rj, routes, frequencies):
    possible_transfers = get_possible_transfers(Ri, Rj, routes)
    min_time = min_time = min(
        compute_time(i, p[2], routes[p[0]]) + compute_time(p[2], j, routes[p[1]]) + 60/(2*frequencies[p[0]]) + 60/(2*frequencies[p[1]])
        for p in possible_transfers
    )
    
    filtered_routes = [
        p for p in possible_transfers
        if compute_time(i, p[2], routes[p[0]]) + compute_time(p[2], j, routes[p[1]]) + 60/(2*frequencies[p[0]]) + 60/(2*frequencies[p[1]])
        < ONE_TRANSFER_MAX * min_time
    ]
    
    trip_classes = filter_trips_by_class(filtered_routes)
    
    total_class_frequency = sum(frequencies[x] for x in trip_classes)
    
    path_with_proportions = [
        ([j, p[2]], frequencies[p[0]]/(total_class_frequency*len(trip_classes[p[0]]))) for p in filtered_routes
    ]
    
    return path_with_proportions

def handle_two_transfer(i, j, Ri, Rj, routes, frequencies):
    complement = get_complement_routes(Ri, Rj, routes)
    possible_transfers = get_possible_double_transfers(Ri, Rj, complement, routes)
    min_time = min(
        compute_time(i, tf1, routes[r1]) + compute_time(tf1, tf2, routes[r3]) + 
        compute_time(tf2, j, routes[r2]) + 
        60 / (2 * frequencies[r1]) + 60 / (2 * frequencies[r2]) + 60 / (2 * frequencies[r3])
        for (r1, r2, r3, tf1, tf2) in possible_transfers
    )

    filtered_routes = [
        (r1, r2, r3, tf1, tf2) 
        for (r1, r2, r3, tf1, tf2) in possible_transfers 
        if compute_time(i, tf1, routes[r1]) + compute_time(tf1, tf2, routes[r3]) + 
           compute_time(tf2, j, routes[r2]) + 
           60 / (2 * frequencies[r1]) + 60 / (2 * frequencies[r2]) + 60 / (2 * frequencies[r3]) < TWO_TRANSFER_MAX * min_time
    ]
    trip_classes = filter_trips_by_class(filtered_routes)

    total_class_frequency = sum(frequencies[x] for x in trip_classes)
    
    path_with_proportions = [
        ([j, p[4], p[3]], frequencies[p[0]]/(total_class_frequency*len(trip_classes[p[0]]))) for p in filtered_routes
    ]
    
    return path_with_proportions

def get_first_transfers_routes(i, j, routes):
    Ri = [e for (e, x) in enumerate(routes) if i in x]
    Rj = [e for (e, x) in enumerate(routes) if j in x]
    min_time = 0
    if is_zero_transfer(Ri, Rj):
        possible_routes = set(Ri).intersection(Rj)
        min_time = get_min_first_route(i, j, possible_routes, routes)
    elif is_one_transfer(Ri, Rj, routes):
        possible_routes = [(ri, rj) for ri in Ri for rj in Rj if set(routes[ri]).intersection(routes[rj])]
        possible_transfers = [(p[0], p[1], tf) for p in possible_routes for tf in set(routes[p[0]]).intersection(routes[p[1]])]

        min_time = min(
            compute_time_first_bus(i, p[2], routes[p[0]]) + compute_time_first_bus(p[2], j, routes[p[1]])
            for p in possible_transfers
        )
        min_time = min(
            max(compute_time_first_bus(i, p[2], routes[p[0]]), compute_time_first_bus(p[2], j, routes[p[1]]) - compute_time(i, p[2], routes[p[0]]))
            for p in possible_transfers
        )
        
    elif is_two_transfer(Ri, Rj, routes):
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
            compute_time_first_bus(i, tf1, routes[r1]) + compute_time_first_bus(tf1, tf2, routes[r3]) + 
            compute_time_first_bus(tf2, j, routes[r2])
            for (r1, r2, r3, tf1, tf2) in possible_transfers
        )
        min_time = min(
            max([compute_time_first_bus(i, tf1, routes[r1]), compute_time_first_bus(tf1, tf2, routes[r3]) - compute_time(i, tf1, routes[r1]), compute_time_first_bus(tf2, j, routes[r2]) - (compute_time(i, tf1, routes[r1]) + compute_time(tf1, tf2, routes[r3]))])
            for (r1, r2, r3, tf1, tf2) in possible_transfers
        )
    return min_time

def get_travel_routes_prop(routes, frequencies):
    travel = [[[] for _ in range(len(network))] for _ in range(len(network))]

    for i in range(len(network)):
        for j in range(len(network)):
            if i == j: continue
            travel[i][j] = get_transfers_routes_prop(i, j, routes, frequencies)

    return travel

def get_travel_routes(routes):
    travel = [[[] for _ in range(len(network))] for _ in range(len(network))]

    for i in range(len(network)):
        for j in range(len(network)):
            if i == j: continue
            travel[i][j] = get_transfers_routes(i, j, routes)

    return travel

def get_first_travel_route(routes):
    travel = dict(((i, j), []) for i in range(len(network)) for j in range(len(network)) if i != j)
    for i in range(len(network)):
        for j in range(len(network)):
            if i == j: continue
            key, val = (i,j), get_first_transfers_routes(i, j, routes)
            travel[key] = val

    return travel

#print(get_first_travel_route(routes = [
#    [0, 1, 2, 5, 7, 9, 10, 12],
#    [4, 3, 5, 7, 14, 6],
#    [11, 3, 5, 14, 8],
#    [9, 13, 12]
#]))