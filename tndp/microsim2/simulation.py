from bus_generator import generate_buses, generate_bus_test
from passenger_generator import *
from route_assignation import compute_time
import datetime

def simulate(coordinates, network_frequencies, network_routes, simulation_time, CAP):
    network_coordinates = [
        list(map(lambda x: tuple(coordinates[x]), r)) for r in network_routes
    ]
    total_time = max(list(map(lambda x: compute_time(x[0], x[-1], x), network_routes)))*60
    total_time = 0
    #passengers = generate_passengers(total_time, network_routes)
    #passengers = [Passenger(0, [9], 5, 9), Passenger(0, [9], 7, 9)]
    passengers = generate_passengers_test(network_routes)
    #passengers = generate_passengers_test_prop(network_routes, network_frequencies)
    #bus_routes = generate_bus_test(network_routes, network_frequencies, network_coordinates, CAP)
    bus_routes = generate_buses(network_routes, network_frequencies, network_coordinates, CAP)
    print(len(passengers))
    n = len(passengers)
    t_s = datetime.datetime.now()

    inv_time = 0
    t_time = 0
    w_time = 0
    inactives = 0
    on_bus = 0
    def alight_passengers(bus, passenger, t):
        nonlocal on_bus, t_time
        if passenger.current_bus == bus.id and bus.current_node == passenger.path[-1]:
            bus.capacity += 1
            bus.passengers -= 1
            on_bus -= 1
            passenger.current_bus = "-1"
            passenger.current_station = passenger.path.pop()
            if len(passenger.path) == 0:
                passenger.active = False
                return
            if t >= total_time:
                t_time += 5*60
            
    def board_passengers(bus, passenger, t):
        nonlocal on_bus
        if passenger.active and passenger.current_bus == "-1" and bus.capacity > 0 and passenger.current_station == bus.current_node:
            to = []
            if bus.dir > 0:
                to = bus.route[bus.route_position:]
            else:
                to = bus.route[0: bus.route_position - 1]
            if passenger.path[-1] in to:
                passenger.current_bus = bus.id
                bus.capacity -= 1
                bus.passengers += 1
                on_bus += 1                    
    time = 0
    while len(passengers) > 0:
    #for time in range(simulation_time+1):
        #print(len(passengers))
        if total_time <= time:
            for p in passengers:
                if p.active and p.arrival_time <= time:
                    if p.current_bus == "-1":
                        w_time += 1
                    else:
                        inv_time += 1
        for route in bus_routes:
            for bus in route:
                if bus.starting_time <= time and bus.state == "on_station":
                    for p in passengers:
                        alight_passengers(bus, p, time)
                    passengers = list(filter(lambda x: x.active, passengers))
                    for p in passengers:
                        board_passengers(bus, p, time)   
                bus.move()
                assert(bus.capacity >= 0 and bus.capacity <= 50)
        #inv_time += on_bus
        time += 1
    print(time)
    print(inactives)
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

""" network_routes = [[0,1,2,5,7,9,10,12],[4,3,5,7,14,6],[11,3,5,14,8],[9,13,12]]
network_frequencies = [68.2, 19.900000000000002, 15.35930618219989, 5.93956326268465] 
simulation_time = 5580 """

network_routes = [[0,1,2,5,7,9,10,12]]
network_frequencies = [10] 
simulation_time = 5580

simulate(coordinates, network_frequencies, network_routes, simulation_time, CAP)
