import pandas as pd
import copy
from random import shuffle
import os

here = os.path.dirname(os.path.abspath(__file__))

file = open(os.path.join(here, 'R101.txt'), 'r')

file2 = open(os.path.join(here, 'R202.txt'), 'r')

routes = pd.DataFrame(columns=file.readline().split(), data=[ [float(y) for y in x.split()] for x in file.readlines() ])

routes2 = pd.DataFrame(columns=file2.readline().split(), data=[ [float(y) for y in x.split()] for x in file2.readlines() ])

def distance(p1, p2):
    return ( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )**0.5

def make_distance_matrix(data):
    mat = []
    n = data.shape[0]
    for i in range(n):
        l = []
        for j in range(n):
            p1 = (data['XCOORD'][i],data['YCOORD'][i])
            p2 = (data['XCOORD'][j],data['YCOORD'][j])
            l.append(distance(p1,p2))
        mat.append(l)
    return mat

def is_feasible(data, distance_matrix, route, capacity):
    load = capacity
    n = len(route)
    cost = 0
    t = 0
    for i in range(0, n-1):
        t += distance_matrix[route[i]][route[i+1]]
        if t > data['DUE_DATE'][route[i+1]]:
            return (False, 0)
        load -= data['DEMAND'][route[i+1]]
        if load < 0:
            return (False, 0)
        if t < data['READY_TIME'][route[i+1]]:
            t = data['READY_TIME'][route[i+1]]
        t += data['SERVICE_TIME'][route[i+1]]
        cost += distance_matrix[route[i]][route[i+1]]
    return (True, cost)

def get_routes(data, distance_matrix, node_list, capacity):
    graph = node_list.copy()
    min_cost = 10000000
    route_list = []
    route = [0, graph.pop(),0]
    current_best_route = route.copy()
    changed = False
    while len(graph) > 0:
        route = current_best_route.copy()
        for i in range(1,len(route)):
            for node in graph:
                route.insert(i, node)
                feasibility = is_feasible(data, distance_matrix, route, capacity)
                if feasibility[0]:
                    if feasibility[1] < min_cost:
                        min_cost = feasibility[1]
                        current_best_route = route.copy()
                        changed = True
                route.remove(node)

        if not changed:
            route_list.append(current_best_route)
            current_best_route = [0, graph.pop(), 0]
        
        min_cost = 10000000
        graph = list(set(graph) - set(current_best_route))
        changed = False
    return route_list

def get_cost(distance_matrix, route):
    res = 0
    for i in range(len(route)-1):
        res += distance_matrix[route[i]][route[i+1]]
    return res

def get_total_cost(distance_matrix, routes):
    res = 0
    for r in routes:
        res += get_cost(distance_matrix, r)
    return res

def or_opt_operator(d_m, data, capacity, s, initial_cost):
    sol = s.copy()
    c_s = s.copy()
    cost = initial_cost
    min_cost = 10000000
    n = len(s)
    for i in range(1, n-2):
        for j in range(i+1, n-1):
            current_cost = cost
            cost -= d_m[c_s[i-1]][c_s[i]] + d_m[c_s[i+1]][c_s[i+2]] + d_m[c_s[j]][c_s[j+1]]
            c_s[i], c_s[i+2] = c_s[i+2], c_s[i]
            c_s[i+1], c_s[j] = c_s[j], c_s[i+1]
            cost += d_m[c_s[i-1]][c_s[i]] + d_m[c_s[i+1]][c_s[i+2]] + d_m[c_s[j]][c_s[j+1]]
            if cost < min_cost and is_feasible(data, d_m, c_s, capacity)[0]:
                min_cost = cost
                sol = c_s.copy()

            c_s[i], c_s[i+2] = c_s[i+2], c_s[i]
            c_s[i+1], c_s[j] = c_s[j], c_s[i+1]

            cost = current_cost
    
    return sol
            

def exchange_operator(d_m, data, capacity, s, initial_cost):
    sol = s.copy()
    c_s = s.copy()
    cost = initial_cost
    min_cost = 10000000
    n = len(s)
    for i in range(1,n-1):
        for j in range(i+1, n-1):
            current_cost = cost
            cost -= d_m[c_s[i-1]][c_s[i]] + d_m[c_s[i]][c_s[i+1]] + d_m[c_s[j-1]][c_s[j]] + d_m[c_s[j]][c_s[j+1]]
            c_s[i], c_s[j] = c_s[j], c_s[i]
            cost += d_m[c_s[i-1]][c_s[i]] + d_m[c_s[i]][c_s[i+1]] + d_m[c_s[j-1]][c_s[j]] + d_m[c_s[j]][c_s[j+1]]
            
            if cost < min_cost and is_feasible(data, d_m, c_s, capacity)[0]:
                min_cost = cost
                sol = c_s.copy()
            
            c_s[i], c_s[j] = c_s[j], c_s[i]
            cost = current_cost

    return sol

def validate_feasibility(r1,r2,data,dist_m, capacity):
    feasibility_1 = is_feasible(data, dist_m, r1, capacity)
    feasibility_2 = is_feasible(data, dist_m, r2, capacity)
    feasible = feasibility_1[0] and feasibility_2[0]
    total_cost = feasibility_1[1] + feasibility_2[1]
    return (feasible, total_cost)


def route_exchange_operator(r1, r2, data, dist_m, capacity):
    min_cost = 100000
    best = (0,0)
    n = len(r1)
    m = len(r2)
    for i in range(1, n-1):
        for j in range(1, m-1):
            r1[i], r2[j] = r2[j], r1[i]
            feasible, total_cost = validate_feasibility(r1, r2, data, dist_m, capacity)
            if feasible and total_cost < min_cost:
                best = (i,j)
                min_cost = total_cost
            r1[i], r2[j] = r2[j], r1[i]

    r1[best[0]], r2[best[1]] = r2[best[1]], r1[best[0]]

def route_relocate_operator(r1, r2, data, dist_m, capacity):
    min_cost = 100000
    best = (0,0)
    n = len(r1)
    m = len(r2)
    for i in range(1, n-1):
        aux_i = r1[i]
        r1.remove(aux_i)
        for j in range(1, m):    
            r2.insert(j, aux_i)
            feasible, total_cost = validate_feasibility(r1, r2, data, dist_m, capacity)
            if feasible and total_cost < min_cost:
                best = (i,j)
                min_cost = total_cost
            r2.remove(aux_i)
        r1.insert(i, aux_i)
    if best != (0,0):
        aux_i = r1[best[0]]
        r1.remove(aux_i)
        r2.insert(best[1], aux_i)

def cross_exchange_operator(r1, r2, data, dist_m, capacity):
    min_cost = 100000
    best = (0,0)
    n = len(r1)
    m = len(r2)
    for i in range(1, n-2):
        for j in range(1, m-2):
            r1[i], r2[j] = r2[j], r1[i]
            r1[i+1], r2[j+1] = r2[j+1], r1[i+1]
            feasible, total_cost = validate_feasibility(r1, r2, data, dist_m, capacity)
            if feasible and total_cost < min_cost:
                best = (i,j)
                min_cost = total_cost
            r1[i], r2[j] = r2[j], r1[i]
            r1[i+1], r2[j+1] = r2[j+1], r1[i+1]

    if best == (0,0): return

    r1[best[0]], r2[best[1]] = r2[best[1]], r1[best[0]]
    r1[best[0]+1], r2[best[1]+1] = r2[best[1]+1], r1[best[0]+1]

def apply_operator(data, distance_matrix, solution, operator, capacity, tabu_list):
    current_sol = solution
    n = len(current_sol)
    min_cost = 100000
    min_sol = []
    for i in range(n-1):
        for j in range(i+1, n):
            operator(current_sol[i], current_sol[j], data, distance_matrix, capacity)
            current_cost = get_total_cost(distance_matrix, current_sol)
            if current_cost < min_cost and round(current_cost, 7) not in tabu_list:
                min_cost = current_cost
                min_sol = copy.deepcopy(current_sol)

    return (min_sol, min_cost)
    
def iterate_operator(data, distance_matrix, solution, operator, capacity, tabu_list):
    min_cost = 100000
    min_sol = solution
    current_sol = solution
    current_cost = 0 
    current_sol, current_cost = apply_operator(data, distance_matrix, current_sol, operator, capacity, tabu_list)
    if current_cost < min_cost:
        min_sol = copy.deepcopy(current_sol)
        min_cost = current_cost
    return (min_sol, min_cost)

operators = [route_exchange_operator, route_relocate_operator, route_exchange_operator]

def reduce_routes(solution):
    while len(solution) != 19:
        for op in operators:
            print(len(solution))
            iterate_operator(routes, distance_matrix, solution, op, 200, tabu_list)
            for k in range(1, len(solution)):
                route_relocate_operator(solution[0], solution[k], routes, distance_matrix, 200)
                if(solution[0] == [0,0]):
                    solution.pop(0)
                    break
            
            solution = list(sorted(solution, key=len))

distance_matrix = make_distance_matrix(routes)

nodes = [ i for i in range(1,len(distance_matrix)) ]

#shuffle(nodes)

solution = sorted(get_routes(routes, distance_matrix, nodes, 200), key=len)

solution = [[0, 92, 42, 15, 87, 57, 43, 13, 58, 0], [0, 59, 2, 21, 73, 41, 56, 74, 0], [0, 45, 98, 16, 85, 96, 60, 89, 0], [0, 83, 82, 7, 8, 46, 17, 93, 0], [0, 63, 30, 51, 9, 20, 32, 0], [0, 65, 71, 81, 50, 1, 70, 0], [0, 39, 23, 67, 55, 4, 25, 0], [0, 28, 12, 76, 78, 3, 68, 0], [0, 72, 40, 53, 26, 24, 77, 0], [0, 33, 29, 79, 34, 35, 0], [0, 62, 11, 90, 66, 80, 0], [0, 36, 47, 19, 49, 48, 0], [0, 14, 44, 38, 91, 100, 0], [0, 27, 52, 84, 97, 0], [0, 5, 61, 86, 37, 0], [0, 31, 88, 10, 0], [0, 95, 99, 94, 0], [0, 75, 22, 54, 0], [0, 69, 18, 6, 0]]
#solution = list(sorted(solution, key=len))
best = (copy.deepcopy(solution), get_total_cost(distance_matrix, solution))
current = best
print(best[1])
print()
tabu_list = [round(best[1],7)]
 
#reduce_routes(solution)
print(solution)

for i in range(10):
    solution = list(sorted(solution, key=len, reverse=True))
    for op in operators:
        for k in range(2000):
            current = iterate_operator(routes, distance_matrix, solution, op, 200, tabu_list)
            if current[1] > 3000:
                break
            print(current[1])
            if current[1] < best[1]:
                best = current
            tabu_list.append(round(current[1], 7))


print(best)