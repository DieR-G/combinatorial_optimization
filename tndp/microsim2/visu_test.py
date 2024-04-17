import matplotlib.pyplot as plt
import numpy as np

# Sample data for nodes and edges
nodes = [[-46.449444, -25.874734],
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
edges = [(0,1),(1,2),(1,3),(1,4),(2,5),
         (3,4),(3,5),(3,11),(5,7),(5,14),
         (14,8),(7,14),(14,6),(7,9),(6,9),
         (11,10),(10,9),(9,12),(9,13),
         (10,12), (13,12)]

# Function to draw graph network
def draw_graph(nodes, edges, node_radius=0.1):
    fig, ax = plt.subplots()
    
    # Draw edges
    for edge in edges:
        x_values = [nodes[edge[0]][0], nodes[edge[1]][0]]
        y_values = [nodes[edge[0]][1], nodes[edge[1]][1]]
        ax.plot(x_values, y_values, color='black')
    
    # Draw nodes
    for node in nodes:
        ax.add_patch(plt.Circle((node[0], node[1]), radius=node_radius, color='blue', zorder=10))

    ax.set_aspect('equal', 'box')
    ax.autoscale()
    plt.show()

# Call the function to draw the graph
draw_graph(nodes, edges, node_radius=0.011)
