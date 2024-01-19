import math
from statistics import mean

CAP = 40*1.25
TRANSFER_TIME = 5
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
    [(12, 3), (9, 5), (11, 10)], 
    [(3, 10), (10, 10)], 
    [(13, 2), (10, 3), (9, 10)], 
    [(12, 2), (9, 8)], 
    [(7, 2), (6, 2), (5, 3), (8, 8)]
]

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

class Tndp:
    def __init__(self, route_nodes, route_freq):
        # route_nodes = list(filter(test_demand, route_nodes))
        # if len(route_nodes) != len(route_freq):
        #     route_freq = [10]*len(route_nodes)
        self.id = self.get_id(route_nodes)
        self.network = self.sub_graph(route_nodes)
        self.routes = list(map(lambda x: self.path_to_arcset(self.conct(x)), route_nodes))
        self.route_nodes = [set(ri) for ri in route_nodes]
        self.route_arcs = [(ri[0: int(len(ri)/2)], ri[int(len(ri)/2):len(ri)]) for ri in self.routes]
        self.route_arc_flows = [{} for _ in range(len(self.routes))]
        self.route_max_flows = [0]*len(self.routes)
        self.route_freq = route_freq
        self.output_freq = [1]*len(self.route_freq)
        self.route_times = [self.calc_path_time(ri)/2 for ri in self.routes]
        self.route_max_pair = [(0,0)]*len(self.routes)

    
    def get_id(self, route_list):
        generated_id = ""
        for r in route_list:
            generated_id += "["
            for n in r:
                generated_id += str(n) + ","
            generated_id += "]"
        return generated_id
    
    def get_route_time(self, r):
        return self.route_times[r]
    def sub_graph(self, route_set):
        _network = [ [] for _ in range(15) ]
        arcs = []
        routes = route_set
        for r in routes:
            arcs += self.path_to_arcset(r)
        for arc in arcs:
            if next(((arc[0], v[1]) for v in network[arc[0]] if v[0] == arc[1]), 0) not in _network[arc[0]]:
                _network[arc[0]].append((arc[1], next((v[1] for v in network[arc[0]] if v[0] == arc[1]), 0)))
            if next(((arc[1], v[1]) for v in network[arc[0]] if v[0] == arc[1]), 0) not in _network[arc[1]]:
                _network[arc[1]].append((arc[0], next((v[1] for v in network[arc[1]] if v[0] == arc[0]), 0)))
        return _network

    def conct(self, x):
            y = x.copy()
            y.pop()
            y.reverse()
            return x+y

    def calc_path_time(self, path):
        cost = 0
        for arc in path:
            for pair in self.network[arc[0]]:
                if pair[0] == arc[1]:
                    cost += pair[1]
                    break
        return cost

    def path_to_arcset(self, path):
        arcs_set=[]
        for i in range(len(path)-1):
            arcs_set.append((path[i], path[i+1]))
        return arcs_set

    def compute_max_flows(self):
        current_max = 0
        for i in range(len(self.route_max_flows)):
            for pair in self.routes[i]:
                if self.route_arc_flows[i][pair] > current_max:
                    current_max = self.route_arc_flows[i][pair]
                    self.route_max_pair[i] = pair
            self.route_max_flows[i] = current_max
            current_max = 0

    def get_bus_number(self,freq):
        num = 0
        for i in range(len(self.routes)):
            freq[i] = self.route_max_flows[i]/CAP
            num += math.ceil(self.route_times[i]*freq[i]/30)
            # num += math.ceil((self.route_times[i]*self.route_max_flows[i])/(CAP*30))
        return num

    def is_0_transfer(self,i,j):
        ans = []
        for r in range(len(self.route_nodes)):
            if i in self.route_nodes[r] and j in self.route_nodes[r]:
                ans.append(r)
        return ans

    def is_1_transfer(self, i, j):
        ans = []
        for r1 in range(len(self.route_nodes)):
            for r2 in range(len(self.route_nodes)):
                if i in self.route_nodes[r1] and j in self.route_nodes[r2] and r1 != r2:
                    common = self.route_nodes[r1].intersection(self.route_nodes[r2]) 
                    if len(common) > 0:
                        ans.append((r1, r2))
        return ans

    def is_2_transfer(self, i, j):
        ans = []
        for r1 in range(len(self.route_nodes)):
            for r2 in range(len(self.route_nodes)):
                for r3 in range(len(self.route_nodes)):
                    if r1 == r2 or r1 == r3 or r2 == r3: continue
                    if i in self.route_nodes[r1] and j in self.route_nodes[r3]:
                        common1 = self.route_nodes[r1].intersection(self.route_nodes[r2])
                        common2 = self.route_nodes[r2].intersection(self.route_nodes[r3])
                        if common1 and common2:
                            ans.append((r1, r2, r3))
        return ans

    def build_path(self, i,j,route):
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

    def build_transfer(self, i, j, pair):
        r1_transfer = []
        r2_transfer = []
        common = self.route_nodes[pair[0]].intersection(self.route_nodes[pair[1]])
        min_time = 1000000
        for node in common:
            auxr1 = self.build_path(i, node, self.route_arcs[pair[0]])
            auxr2 = self.build_path(node, j, self.route_arcs[pair[1]])
            aux = self.calc_path_time(auxr1) + self.calc_path_time(auxr2)
            if aux < min_time:
                min_time = aux
                r1_transfer = auxr1.copy()
                r2_transfer = auxr2.copy()
        return r1_transfer, r2_transfer

    def build_transfer_2(self, i, j, triple):
        r1_transfer = []
        r2_transfer = []
        r3_transfer = []
        common1 = self.route_nodes[triple[0]].intersection(self.route_nodes[triple[1]])
        min_time = 1000000
        for node in common1:
            auxr1 = self.build_path(i, node, self.route_arcs[triple[0]])
            auxr2, auxr3 = self.build_transfer(node, j, (triple[1], triple[2]))
            aux = self.calc_path_time(auxr1) + self.calc_path_time(auxr2) + self.calc_path_time(auxr3)
            if aux < min_time:
                min_time = aux
                r1_transfer = auxr1.copy()
                r2_transfer = auxr2.copy()
                r3_transfer = auxr3.copy()
        return r1_transfer, r2_transfer, r3_transfer

    def update_arc_flows(self, val, path, r):
        for p in path:
            self.route_arc_flows[r][p] += val

    def compute_0_transfer_time(self, i, j, possible_routes, freq):
        total_freq = 0
        total_time = 0
        total_wait_time = 0
        pi = 0
        min_time = min(possible_routes, key=lambda x: self.calc_path_time(self.build_path(i, j, self.route_arcs[x])))
        min_time = self.calc_path_time(self.build_path(i, j, self.route_arcs[min_time]))
        possible_routes = list(filter(lambda x: self.calc_path_time(self.build_path(i,j,self.route_arcs[x]))/min_time <= ONE_TRANSFER_MAX, possible_routes))
        for r in possible_routes:
            total_freq += freq[r]
        for r in possible_routes:
            pi = demand_matrix[i][j]*(freq[r]/total_freq)
            current_path = self.build_path(i,j,self.route_arcs[r])
            self.update_arc_flows(pi, current_path, r)
            travel_time = self.calc_path_time(current_path)
            wait_time = 30/total_freq
            total_wait_time += wait_time*pi
            total_time += (travel_time)*pi
        return total_time, total_wait_time, 0

    def compute_1_transfer_time(self, i, j, possible_routes, freq):
        min_time = 1e6
        total_freq = 0
        total_time = 0
        total_wait_time = 0
        total_transfer_time = 0
        travel_time = 0
        wait_time = 0
        trip_classes = {}
        min_el = min(possible_routes, key=lambda r: self.calc_path_time(sum(self.build_transfer(i, j, r), [])))
        min_time = self.calc_path_time(sum(self.build_transfer(i, j, min_el), []))
        possible_routes = list(filter(lambda x: self.calc_path_time(sum(self.build_transfer(i, j, x), []))/min_time <= ONE_TRANSFER_MAX, possible_routes))
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
                path_r1, path_r2 = self.build_transfer(i, j, r)
                self.update_arc_flows(pi, path_r1, r[0])
                self.update_arc_flows(pi, path_r2, r[1])
                travel_time += self.calc_path_time(path_r1 + path_r2)
                wait_time += 30/freq[r[1]]
                total_wait_time += wait_time*pi
                total_transfer_time += TRANSFER_TIME*pi
                total_time += (travel_time)*pi
        return total_time, total_wait_time, total_transfer_time

    def compute_2_transfer_time(self, i, j, possible_routes, freq):
        total_freq = 0
        total_time = 0
        travel_time = 0
        wait_time = 0
        total_wait_time = 0
        total_transfer_time = 0
        trip_classes = {}
        min_el = min(possible_routes, key=lambda r: self.calc_path_time(sum(self.build_transfer_2(i, j, r), [])))
        min_time = self.calc_path_time(sum(self.build_transfer_2(i, j, min_el), []))
        possible_routes = list(filter(
            lambda x: self.calc_path_time(sum(self.build_transfer_2(i, j, x),[]))/min_time <= TWO_TRANSFER_MAX, possible_routes
        ))
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
                path_r1, path_r2, path_r3 = self.build_transfer_2(i, j, r)
                self.update_arc_flows(pi, path_r1, r[0])
                self.update_arc_flows(pi, path_r2, r[1])
                self.update_arc_flows(pi, path_r3, r[2])
                travel_time += self.calc_path_time(path_r1 + path_r2 + path_r3)
                wait_time += 30/freq[r[1]]+30/freq[r[2]]
                total_wait_time += wait_time*pi
                total_transfer_time += 2*TRANSFER_TIME*pi
                total_time += (travel_time)*pi
        return total_time, total_wait_time, total_transfer_time

    def evaluate(self, routes, freq):
        total = {'tv':0, 'te':0, 'tt':0}
        unsat = []
        a = 0
        b = 0
        c = 0
        for r in range(len(routes)):
            for pair in routes[r]:
                self.route_arc_flows[r][pair] = 0
        for i in range(len(network)):
            for j in range(len(network)):
                if demand_matrix[i][j] == 0: continue
                x = self.is_0_transfer(i,j)
                y = self.is_1_transfer(i,j)
                z = self.is_2_transfer(i, j)
                if x:
                    a,b,c = self.compute_0_transfer_time(i, j, x, freq)
                    total['tv'] += a
                    total['te'] += b
                    total['tt'] += c
                elif y:
                    a,b,c = self.compute_1_transfer_time(i, j, y, freq)
                    total['tv'] += a
                    total['te'] += b
                    total['tt'] += c
                elif z:
                    a,b,c = self.compute_2_transfer_time(i, j, z, freq)
                    total['tv'] += a
                    total['te'] += b
                    total['tt'] += c
                else:
                    if((i,j) in unsat or (j, i) in unsat):
                        continue
                    unsat.append((i,j))
                    # print('unsatisfied demand', (i,j))
        return total, unsat

    def f(self):
        ans = {}
        while True:
            output_freq = self.route_freq.copy()
            ans, unsat = self.evaluate(self.routes, self.route_freq)
            self.compute_max_flows()
            buses = self.get_bus_number(output_freq)
            u1 = mean(output_freq)
            u2 = mean(self.route_freq)
            if abs(u1 - u2) < 1 or unsat:
                break
            self.route_freq = output_freq.copy()

        return ans, output_freq, buses, unsat
    def get_max_pair(self):
        self.evaluate(self.routes, self.route_freq)
        self.compute_max_flows()
        return self.route_max_pair[self.route_max_flows.index(max(self.route_max_flows))]