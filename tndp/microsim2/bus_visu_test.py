import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap
from bus_generator import generate_buses, generate_bus_test

# Function to initialize the plot
def setup_plot():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.grid(True)
    ax.set_xlim(-46.6, -45.8)  # Set plot limits to the GPS coordinates range
    ax.set_ylim(-26.6, -25.8)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title('Bus Positions in Space')
    return fig, ax

# Function to update the plot
def update(frame_number, buses, scatter_plots):
    for scatter, bus_list in zip(scatter_plots, buses):
        positions = [(bus.pos.x, bus.pos.y) for bus in bus_list]
        scatter.set_offsets(positions)  # Update positions for each route
        for bus in bus_list:
            bus.move()  # Move each bus to the next position
    return scatter_plots

# Setup data for the animation
coordinates = [
    [-46.449444, -25.874734], [-46.350297, -25.973882], [-46.216734, -25.977159],
    [-46.349477, -26.083682], [-46.506802, -26.083682], [-46.217553, -26.08614],
    [-45.884057, -26.218064], [-46.09956, -26.218883], [-45.836531, -26.08532],
    [-45.978288, -26.376208], [-46.04466, -26.461426], [-46.38635, -26.331961],
    [-45.936499, -26.504035], [-45.855378, -26.439302], [-45.9873, -26.084501]
]
network_routes = [[0, 1, 2, 5, 7, 9, 10, 12], [4, 3, 5, 7, 14, 6], [11, 3, 5, 14, 8], [9, 13, 12]]
network_frequencies = [68.2, 19.9, 15.21, 5.446]
network_coordinates = [
    list(map(lambda x: tuple(coordinates[x]), r)) for r in network_routes
]
buses = generate_buses(network_routes, network_frequencies, network_coordinates, 50)

fig, ax = setup_plot()
cmap = get_cmap('viridis', len(buses))  # Get a colormap with as many colors as there are routes

# Create a scatter plot for each bus route with a different color
scatter_plots = [ax.scatter([], [], s=15, color=cmap(i)) for i in range(len(buses))]

ani = FuncAnimation(fig, update, fargs=(buses, scatter_plots), interval=50, blit=True)

plt.show()
