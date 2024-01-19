import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualizer:
    def __init__(self, network, solution, objective_function):
        self.network = network
        self.solution = solution
        self.objective_function = objective_function
        self.G = nx.Graph()

        # Add nodes and edges
        nodes = [i for i in range(len(network))]
        arcset = [(p[0], v[0]) for p in enumerate(network) for v in p[1]]
        self.G.add_nodes_from(nodes)
        self.G.add_edges_from(arcset)

        # Layout
        seed = 30
        self.pos = nx.spring_layout(self.G, seed=seed)
        self.pos = {node: (-x, y) for node, (x, y) in self.pos.items()}

    def draw_graph(self):
        # Draw the graph using spring layout
        nx.draw(self.G, self.pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=10, font_color='black', edge_color='gray')

        # Draw each route with a different color
        for i, route in enumerate(self.solution):
            route_edges = [(route[0][j], route[0][j + 1]) for j in range(len(route[0]) - 1)]
            nx.draw_networkx_edges(self.G, self.pos, edgelist=route_edges, edge_color=f'C{i}', width=2.5, label=f'Ruta {i + 1}, Buses: {route[1]}.0')

        # Add legend to the bottom-left
        plt.legend(loc='lower left')

        # Add annotation label
        annotation_label = f"Función objetivo: {self.objective_function}\nTotal buses: {sum(route[1] for route in self.solution)}"
        plt.annotate(annotation_label, xy=(0.5, -0.1), xycoords="axes fraction", ha='center', va='center', fontsize=12, bbox=dict(boxstyle="round,pad=0.3", edgecolor="none", facecolor="white"))

    def save_plot(self, filename, dpi=600):
        # Save the plot to a file (e.g., PNG format)
        plt.savefig(filename, bbox_inches='tight', dpi=dpi)

    def show_plot(self):
        # Show the plot
        plt.show()