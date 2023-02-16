import pandas as pd
import time
import numpy as np

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



def get_cut_nodes_value(initial_val, path, i, j, dist_matrix):
    n = len(path)
    
    cut_cost = 0
    cut_cost += dist_matrix[path[(i-1) % n]][path[i]] 
    cut_cost += dist_matrix[path[i]][path[(i+1) % n]]

    cut_cost += dist_matrix[path[(j-1) % n]][path[j]]
    cut_cost += dist_matrix[path[j]][path[(j+1) % n]] 
    
    path[i], path[j] = path[j], path[i]

    add_cost = 0
    add_cost += dist_matrix[path[(i-1) % n]][path[i]] 
    add_cost += dist_matrix[path[i]][path[(i+1) % n]]

    add_cost += dist_matrix[path[(j-1) % n]][path[j]]
    add_cost += dist_matrix[path[j]][path[(j+1) % n]] 

    return initial_val - cut_cost + add_cost

def is_close_to_any(val, arr):
    return np.any(np.isclose(val, arr))

def exchange(path, i, j):
    path[i], path[j] = path[j], path[i]

def exchange_operator(initial_sol, dist_matrix, tabu_list = []):
    n = len(initial_sol)
    best_solution = initial_sol.copy()
    min_val = 10000000
    initial_val = compute_obj_function(initial_sol, dist_matrix)
    for i in range(n):
        for j in range(i + 1, n):
            current_sol = initial_sol.copy()
            current_val = get_cut_nodes_value(initial_val, current_sol, i, j, dist_matrix)
            if current_val < min_val and round(current_val,10) not in tabu_list:
                best_solution = current_sol.copy()
                min_val = current_val
    return best_solution
            
def iterate_exchange_operator(initial_sol, dist_matrix):
    current_sol = initial_sol
    min = 100000
    tabu_list = []
    for i in range(1000):
        current_sol = exchange_operator(current_sol, dist_matrix, tabu_list)
        current_val = compute_obj_function(current_sol, dist_matrix)
        if current_val < min:
            min = current_val
        tabu_list.append(round(current_val,10))
    print(min)

mat = [ [0, 132, 217, 164, 58],
        [132, 0, 290, 201, 79],
        [217, 290, 0, 113, 303],
        [164, 201, 113, 0, 196],
        [58, 79, 303, 196, 0]]

Datos=pd.read_csv("dj38.tsp", sep=" ")

distance_matrix = generate_distance_city(Datos)

result = compute_tsp(distance_matrix, 6)


start_time = time.time()
iterate_exchange_operator(result, distance_matrix)
print(time.time() - start_time)