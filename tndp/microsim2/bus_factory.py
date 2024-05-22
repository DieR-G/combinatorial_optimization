from bus_class import Bus

class BusFactory:
    def __init__(self, network):
        self.network = network

    def node_at_time(self, route):
        node_time_map = {}
        index_time_list = [0] * len(route)
        current_node = route[0]
        t = 0
        for idx, node in enumerate(route):
            t += next((c for a, c in self.network[node] if a == current_node), 0)
            node_time_map[t * 60] = node
            index_time_list[idx] = t * 60
            current_node = node
        return node_time_map, index_time_list

    def create_bus(self, id, route, capacity, starting_time, total_time, node_time_map, index_time_list):
        return Bus(id, route, capacity, starting_time, total_time, node_time_map, index_time_list)
