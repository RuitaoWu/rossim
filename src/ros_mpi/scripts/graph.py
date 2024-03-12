
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
# Generate a random DAG with n nodes
def generate_random_dag(n):
    G = nx.DiGraph()
    nodes = list(range(1, n + 1))
    G.add_nodes_from(nodes)

    for i in range(2, n + 1):
        # Randomly select parent nodes for node i
        parents = random.sample(nodes[:i-1], random.randint(0, i-1))
        # Add edges from parents to node i
        for parent in parents:
            G.add_edge(parent, i)
    
    return G

# Generate a random DAG with 10 nodes
random_dag = generate_random_dag(6)
print(nx.is_directed_acyclic_graph(random_dag))
# bc = nx.betweenness_centrality(random_dag)
bc=nx.edge_betweenness_centrality(random_dag)
# print(bc)
# Draw the DAG (optional)
nx.draw(random_dag, with_labels=True, arrows=True)
plt.draw()
plt.show()


# Compute betweenness centrality for edges
edge_betweenness = nx.edge_betweenness_centrality(random_dag)

# Find the edge(s) with the greatest betweenness centrality
max_betweenness = max(edge_betweenness.values())
edges_with_max_betweenness = [edge for edge, centrality in edge_betweenness.items() if centrality == max_betweenness]

# Remove the first edge with the greatest betweenness centrality
if edges_with_max_betweenness:
    edge_to_remove = edges_with_max_betweenness[0]
    random_dag.remove_edge(*edge_to_remove)
    print(f"Removed edge with the greatest betweenness centrality: {edge_to_remove}")
else:
    print("No edges found with non-zero betweenness centrality")


nx.draw(random_dag, with_labels=True, arrows=True)
plt.draw()
plt.show()