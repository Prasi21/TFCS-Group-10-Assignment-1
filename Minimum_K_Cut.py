import networkx as nx
import matplotlib.pyplot as plt 
from itertools import combinations, chain


# Number of target partitions
TARGET_PARTITIONS = 3

# Function to create the graph
def create_graph():
    g = nx.Graph()
    nodes = ["a", "b", "c", "d", "e", "f", "g"]
    
    for node in nodes:
        g.add_node(node, visited=False)
    
    edges = [
        ("a", "b", 1), ("a", "c", 4),
        ("b", "d", 3), ("b", "e", 6),
        ("c", "d", 2), ("c", "f", 5),
        ("d", "e", 2), ("d", "f", 4),
        ("e", "f", 2), ("e", "g", 7),
        ("f", "g", 6)
    ]
    
    for edge in edges:
        v1, v2, weight = edge
        g.add_edge(v1, v2, weight=weight)
    
    return g

# Function to get all possible edge combinations
def get_edge_combinations(g):
    return powerset(g.edges.data("weight", default=1))

# Function to find the best partition
def find_best_partition(g, all_edge_combinations):
    current_best_sum = float('inf')
    current_best_combo = None
    combo_count = 0
    
    for combo in all_edge_combinations:
        combo_count += 1
        g_copy = g.copy()
        
        # Calculate the sum of weights and remove edges
        sum_weights = 0
        for edge in combo:
            v1, v2, weight = edge
            sum_weights += weight
            g_copy.remove_edge(v1, v2)
        
        # If there is already a better one, don't bother checking this one
        if sum_weights > current_best_sum:
            continue
        
        # Check the number of partitions
        count = count_partitions(g_copy)
        
        if count == TARGET_PARTITIONS:
            current_best_combo = combo
            current_best_sum = sum_weights
    
    return current_best_combo, current_best_sum, combo_count

# Function to count partitions using DFS
def count_partitions(g):
    count = 0
    while unvisited_nodes_exist(g):
        start_node = get_first_unvisited_node(g)
        for node in nx.algorithms.dfs_preorder_nodes(g, start_node):
            nx.set_node_attributes(g, {node: {"visited": True}})
        count += 1
    return count

# Function to check if unvisited nodes exist
def unvisited_nodes_exist(g):
    return any(not visited for _, visited in g.nodes.data("visited", default=False))

# Function to get the first unvisited node
def get_first_unvisited_node(g):
    for node, visited in g.nodes.data("visited", default=False):
        if not visited:
            return node
    return None

# Function to generate the powerset of iterable
def powerset(iterable):
    return chain.from_iterable(combinations(iterable, r) for r in range(len(iterable) + 1))

# Function to remove edges from the graph and set their weight to -1
def remove_edges_from_graph(g, edges_to_remove):
    for edge in edges_to_remove:
        v1, v2, _ = edge
        if g.has_edge(v1, v2):
            nx.set_edge_attributes(g, {(v1, v2): {"weight": -1}})

# Function to visualize the graph
def visualize_graph(g):
    # Adjust the k value to control the spacing between nodes
    random_pos = nx.random_layout(g, seed=42)
    pos = nx.spring_layout(g, pos=random_pos, k=0.5)
    
    labels = {node: node for node in g.nodes()}
    
    edge_colors = []  # To store edge colors
    
    for edge in g.edges(data=True):
        v1, v2, data = edge
        weight = data.get("weight", 1)
        
        if weight == -1:
            edge_colors.append("red")
        else:
            edge_colors.append("black")
    
    nx.draw(g, pos, with_labels=True, labels=labels, node_size=500, edge_color=edge_colors)
    
    edge_labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    
    plt.show()

# Main function
def main():
    g = create_graph()
    
    # Visualize the graph
    visualize_graph(g)
    
    all_edge_combinations = get_edge_combinations(g)
    
    best_combo, best_sum, combo_count = find_best_partition(g, all_edge_combinations)
    print("BEST:", best_combo, "=", best_sum)
    print("There were", combo_count, "combinations to check! Yay exponentiation!")
    
    # Remove the best_combo edges from the original graph and set their weight to -1
    remove_edges_from_graph(g, best_combo)
    print("Graph after removing best_combo edges:")
    visualize_graph(g)
    
if __name__ == "__main__":
    main()
