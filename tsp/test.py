import pandas as pd

def compute_distance(x1,y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def generate_distance_city(data):
    n = data.shape[0]
    result = []
    for i in range(n):
        L = []
        cx1 = data.at[i, 'cx']
        cy1 = data.at[i, 'cy']
        for j in range(n):
            cx2 = data.at[j, 'cx']
            cy2 = data.at[j, 'cy']
            L.append(compute_distance(cx1, cy1, cx2, cy2))
        result.append(L)

    return result

def compute_obj_function(s, dist_m):
    d = 0
    n = len(s)
    for i in range(n):
        d += dist_m[s[i]][s[(i+1) % n]]
    return d

def get_min_distance_node(adj_list, computed):
    if len(computed) == len(adj_list):
        return -1
    index = 0
    min = 10000000
    for i in range(len(adj_list)):
        if adj_list[i] < min and i not in computed:
            index = i
            min = adj_list[i]
    return index

def compute_tsp(graph, starting_node = 0):
    solution = []
    current_node = starting_node
    node_count = len(graph)
    next = 0

    while next != -1:
        solution.append(current_node)
        next = get_min_distance_node(graph[current_node], solution)
        current_node = next
        node_count -= 1

    #solution.append(solution[0])
    return solution

Datos=pd.read_csv("dj38.tsp", sep=" ")

distance_matrix = generate_distance_city(Datos)

result = compute_tsp(distance_matrix, 6)

val = compute_obj_function(result, distance_matrix)

print(val)