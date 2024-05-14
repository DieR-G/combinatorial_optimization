from bus_generator import generate_buses
from passenger_generator import generate_passengers_test
import datetime
import itertools

STATION_NUMBER = 15
MAX_TIME_SIMULATED = 10000
TRANSFER_TIME = 5*60

station_passengers_history = []
time_history = []
def simulate(network_frequencies, network_routes, CAP):    
    passengers_at_time = [0]*MAX_TIME_SIMULATED
    stations = [set() for _ in range(STATION_NUMBER)]
    passengers = generate_passengers_test(network_routes, stations, passengers_at_time)
    bus_routes = generate_buses(network_routes, network_frequencies, CAP)
    passengers_pref_time = list(itertools.accumulate(passengers_at_time))
    print(len(passengers))
    t_s = datetime.datetime.now()
    n = len(passengers)
    inv_time = 0
    t_time = 0
    w_time = 0
    on_bus = 0
    
    def alight_passengers(bus):
        nonlocal on_bus, t_time, stations
        for passenger in bus.stations_map[bus.current_node]:
            passenger.current_bus = "-1"
            passenger.current_station = passenger.path.pop()
            if len(passenger.path) == 0:
                passengers.remove(passenger)
                continue
            stations[passenger.current_station].add(passenger)
            t_time += TRANSFER_TIME
        bus.capacity += len(bus.stations_map[bus.current_node])
        on_bus -= len(bus.stations_map[bus.current_node])
        bus.stations_map[bus.current_node] = []
            
    def board_passengers(bus, t):
        nonlocal on_bus, stations
        to_remove = []
        for passenger in stations[bus.current_node]:
            if passenger.arrival_time > t:
                continue
            if bus.capacity > 0:
                to = bus.route[bus.route_position:] if bus.dir > 0 else bus.route[:bus.route_position + 1]
                if passenger.path[-1] in to:
                    passenger.current_bus = bus.id
                    bus.capacity -= 1
                    on_bus += 1
                    bus.stations_map[passenger.path[-1]].append(passenger)
                    to_remove.append(passenger)  # Add passenger to the removal list
            else:
                break
        for passenger in to_remove:
            stations[bus.current_node].discard(passenger)
         
    
    time = 0
    while len(passengers) > 0:
        for route in bus_routes:
            for bus in route:
                if bus.state == "on_station":
                    alight_passengers(bus)
                    board_passengers(bus, time) 
                bus.move()
                assert(bus.capacity >= 0 and bus.capacity <= 50)
        inactives = n - len(passengers)
        w_time += passengers_pref_time[time] - on_bus - inactives
        inv_time += on_bus
        time += 1
    print(time)
    print(inv_time//60, w_time//60, t_time//60, (inv_time+w_time+t_time)//60)
    t_e = datetime.datetime.now()
    print(t_e-t_s)

coordinates = [[-46.449444, -25.874734],
               [-46.350297, -25.973882],
               [-46.216734, -25.977159],
               [-46.349477, -26.083682],
               [-46.506802, -26.083682],
               [-46.217553, -26.08614],
               [-45.884057, -26.218064],
               [-46.09956, -26.218883],
               [-45.836531, -26.08532],
               [-45.978288, -26.376208],
               [-46.04466, -26.461426],
               [-46.38635, -26.331961],
               [-45.936499, -26.504035],
               [-45.855378, -26.439302],
               [-45.9873, -26.084501]]
CAP = 50
""" network_frequencies = [1000]
network_routes = [
    [0,1,2,5,7,9,10,12]
]
simulation_time = 600 """

network_routes = [[0,1,2,5,7,9,10,12], [4,3,5,7,14,6], [11,3,5,14,8],[9,13,12]]
network_frequencies = [68.2, 19.900000000000002, 15.210936746793037, 5.446410882717701] 

""" network_routes = [[10,12,13,9,7,14,5,2,1,0],[6,14,5,3,4],[11,3,5,14,8]]
network_frequencies = [68.5, 19.900000000000002, 16.45525002610718] """

""" network_routes = [[0,1,2,5,7,9,10]]
network_frequencies = [10] 
simulation_time = 5580
"""


simulate(network_frequencies, network_routes, CAP)