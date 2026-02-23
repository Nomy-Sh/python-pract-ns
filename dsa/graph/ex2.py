import networkx as nx
import matplotlib.pyplot as plt

# 1. Initialize an empty undirected graph
G = nx.Graph()

# 2. Add edges (this automatically creates the nodes if they don't exist)
G.add_edges_from([
    ('A', 'B'), ('B', 'C'), ('C', 'A'), 
    ('C', 'D'), ('D', 'E'), ('E', 'C')
])

# 3. Choose a layout (positioning of nodes)
# spring_layout is the default but defining it explicitly allows for more control
pos = nx.spring_layout(G)

# 4. Draw the graph components
nx.draw(G, pos, with_labels=True, 
        node_color='purple', 
        node_size=800, 
        edge_color='gray', 
        font_size=15, 
        font_color='white',
        font_weight='bold')

# 5. Display the result
plt.title("Simple NetworkX Graph")
plt.show()