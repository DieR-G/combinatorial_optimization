import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# Create graph
G = nx.Graph()

# Add nodes with coordinates
for i, coord in enumerate(coordinates):
    G.add_node(i, pos=(coord[0], coord[1]))

# Add edges
for node, neighbors in enumerate(network):
    for neighbor in neighbors:
        G.add_edge(node, neighbor[0], weight=neighbor[1])

# Initialize plot
fig, ax = plt.subplots()
# Function to update animation
def update(frame):
    ax.clear()
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=200, node_color='lightblue', font_size=8, edge_color='gray')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    ax.scatter(positions[frame][0], positions[frame][1], color='red', s=50, marker='o')

# Create animation
ani = FuncAnimation(fig, update, frames=len(positions), interval=1)

plt.show()