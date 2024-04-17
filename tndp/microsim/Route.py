from Bus import Bus
CAP = 40*1.25

class Route:
    def __init__(self, route, frequency):
        self.route = route
        self.frequency = frequency
        self.buses = [Bus(self.route, CAP), Bus(list(reversed(self.route)), CAP)]
        self.on_station_buses = []
        self.has_bus_on_station = False
        self.time = 0
        self.last_time = 0

    def advance_time(self, city_nodes):
        self.time += 1
        if self.time - self.last_time > self.frequency:
            new_bus = Bus(self.route, CAP)
            new_bus.nodes.remove(new_bus.node_queue[0])
            new_bus.node_queue.popleft()
            self.buses.append(new_bus)
            self.last_time = self.time
        for bus in self.buses:
            bus.advance_time(city_nodes)
            if bus.on_station:
                self.has_bus_on_station = True
                self.on_station_buses.append(bus)
    
    def get_on_station_buses(self):
        return self.on_station_buses
    
    def leave_stations(self):
        self.has_bus_on_station = False
        for bus in self.on_station_buses:
            bus.leave_station()
        self.on_station_buses = []