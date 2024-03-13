
# minmin algorithm 
# import numpy as np
# def main():
#     nM, nT = 3,10

#     # minMin = np.random.uniform(1, 10, size=(nM, nT))
#     minMin = np.random.randint(1, 5, size=(nM, nT))
#     done = np.full(nT, -1, dtype=int)  # -1 -> not completed, 0 -> completed

#     ptr = np.zeros(nT, dtype=int)      # Holds the index of the smaller execution time for every task
#     min_time = np.zeros(nT, dtype=int)  # Holds the value of the smaller execution time for every task
#     print(minMin)
#     print(done)
#     result_task = np.zeros(nT, dtype=int)
#     result_machine = np.zeros(nT, dtype=int)
#     result_time = np.zeros(nT, dtype=int)

#     for k in range(nT):
#         for i in range(nT):
#             if done[i] == 0:
#                 continue
#             min_time[i] = minMin[0][i]

#         for j in range(nT):
#             if done[j] == 0:
#                 continue
#             for i in range(nM):
#                 if minMin[i][j] <= min_time[j]:
#                     min_time[j] = minMin[i][j]
#                     ptr[j] = i

#         p = 99999  # Points to the min task time in the task array
#         p1 = 0     # Stores the index
#         for i in range(nT):
#             if done[i] == 0:
#                 continue
#             if min_time[i] <= p:
#                 p = min_time[i]
#                 p1 = i
#         result_task[k] = p1
#         result_machine[k] = ptr[p1]
#         result_time[k] = minMin[ptr[p1]][p1]
#         done[p1] = 0
#         for j in range(nT):
#             if done[j] == -1:
#                 minMin[ptr[p1]][j] += p

#     # Printing answer
#     print("\nScheduled Tasks are:")
#     for i in range(nT):
#         print(f"Task {result_task[i]+1} Runs on Machine {result_machine[i]+1} with Time {result_time[i]} units")
#     print(f"Makespan = {np.max(result_time)}")

# if __name__ == "__main__":
#     main()
#     print('finished...')




####################################################################
####################################################################
####################################################################

###graph partition algorithm
import networkx as nx
import matplotlib.pyplot as plt
import random


#convert to maximum spanning tree

# Generate a random DAG with n nodes
def generate_dag(n):
    G = nx.DiGraph()
    nodes = list(range(1, n + 1))
    G.add_nodes_from(nodes)

    for i in range(2, n + 1):
        # Randomly select parent nodes for node i
        parents = random.sample(nodes[:i-1], random.randint(0, i-1))
        # Add edges from parents to node i
        for parent in parents:
            G.add_edge(parent, i,weight=round(random.uniform(5,10), 2))
    
    return G

# Generate a random DAG with 10 nodes
G = generate_dag(6)

# def group_nodes_topological(dag, k):
#     # Perform topological sort
#     topological_order = list(nx.topological_sort(dag))
    
#     # Calculate the size of each group
#     group_size = len(topological_order) // k
    
#     # Group nodes based on topological ordering
#     communities = []
#     for i in range(k):
#         start = i * group_size
#         end = (i + 1) * group_size if i < k - 1 else len(topological_order)
#         communities.append(topological_order[start:end])

#     return communities

# communities = group_nodes_topological(G, 6)

# # Print communities
# for i, community in enumerate(communities):
#     print(f"Community {i + 1}: {community}")


# Create a directed acyclic graph (DAG)


# Perform topological sort
topological_order = list(nx.topological_sort(G))

# Group nodes based on topological ordering
def group_nodes(topological_order, k):
    groups = []
    for i in range(0, len(topological_order), k):
        groups.append(topological_order[i:i+k])
    return groups

k = 2  # Number of nodes per group
node_groups = group_nodes(topological_order, k)

# Assign colors to each group
colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'yellow']

# Create a dictionary to store the color of each node
node_colors = {}
for i, group in enumerate(node_groups):
    for node in group:
        node_colors[node] = colors[i]

# Plot the DAG with different colors for different communities
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color=[node_colors[node] for node in G.nodes()], node_size=1000)
plt.show()









# print(nx.is_directed_acyclic_graph(G))

# bc = nx.betweenness_centrality(G)
# bc = nx.edge_betweenness_centrality(G)
# print(bc)
# Draw the DAG (optional)

# pos = nx.spring_layout(G)  # Positions for all nodes
# nx.draw(G, pos,with_labels=True, arrows=True)
# edge_labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red',alpha=0.5,verticalalignment
# ='top')
# comm = nx.community.girvan_newman(G)
# for c in comm:
#     print(c)
# pos = nx.spring_layout(G)  # Positions for all nodes
# nx.draw(G, pos,with_labels=True, arrows=True)

# plt.draw()
# plt.show()


# import pandas as pd

# # Load karate graph and find communities using Girvan-Newman
# # G = nx.karate_club_graph()
# communities = list(nx.community.girvan_newman(G))
# # print(f'communities at line 120: {communities}')

# # function to create node colour list
# def create_community_node_colors(graph, communities):
#     number_of_colors = len(communities)
#     print(f'num: {number_of_colors}')
#     colors = ["#D4FCB1", "#CDC5FC", "#FFC2C4", "#F2D140", "#BCC6C8","#D5FCB7", "#CDC3FC", "#FFC1C6", "#FAD140", "#BDC7C8"][:number_of_colors]
#     node_colors = []
#     for node in graph:
#         current_community_index = 0
#         for community in communities:
#             if node in community:
#                 node_colors.append(colors[current_community_index])
#                 break
#             print(f'current community index {current_community_index}')
#             current_community_index += 1
#     return node_colors


# # function to plot graph with node colouring based on communities
# def visualize_communities(graph, communities, i):
#     node_colors = create_community_node_colors(graph, communities)
#     modularity = round(nx.community.modularity(graph, communities), 6)
#     title = f"Community Visualization of {len(communities)} communities with modularity of {modularity}"
#     pos = nx.spring_layout(graph, k=0.3, iterations=50, seed=2)
#     plt.subplot(2, 1, i)
#     plt.title(title)
#     nx.draw(
#         graph,
#         pos=pos,
#         node_size=1000,
#         node_color=node_colors,
#         with_labels=True,
#         font_size=20,
#         font_color="black",
#     )


# fig, ax = plt.subplots(3, figsize=(15, 20))

# # Plot graph with colouring based on communities
# visualize_communities(G, communities[0], 1)
# visualize_communities(G, communities[2], 2)

# plt.show()







# # Compute betweenness centrality for edges
# edge_betweenness = nx.edge_betweenness_centrality(G)

# # Find the edge(s) with the greatest betweenness centrality
# max_betweenness = max(edge_betweenness.values())
# edges_with_max_betweenness = [edge for edge, centrality in edge_betweenness.items() if centrality == max_betweenness]

# # Remove the first edge with the greatest betweenness centrality
# if edges_with_max_betweenness:
#     edge_to_remove = edges_with_max_betweenness[0]
#     G.remove_edge(*edge_to_remove)
#     print(f"Removed edge with the greatest betweenness centrality: {edge_to_remove}")
# else:
#     print("No edges found with non-zero betweenness centrality")


# nx.draw(G, with_labels=True, arrows=True)
# plt.draw()
# plt.show()