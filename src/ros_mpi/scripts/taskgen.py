import random
class TaskGen():

    def __init__(self,num_nodes,computing_node):
        self.computing_node = computing_node
        self.num_nodes = num_nodes
    def gen_comp_matrix(self):
        return [[random.randint(20,40) for _ in range(self.computing_node)] for _ in range(self.num_nodes)]
    def generate_random_dag(self,density):
        # Initialize an empty adjacency matrix
        adjacency_matrix = [[0] * self.num_nodes for _ in range(self.num_nodes)]

        # Ensure the graph is acyclic
        for i in range(self.num_nodes - 1):
            for j in range(i + 1, self.num_nodes):
                if random.random() < density:
                    # Add an edge from node i to node j
                    adjacency_matrix[i][j] = 1

                    # Ensure the graph remains acyclic
                    if self.is_cyclic(adjacency_matrix):
                        # If adding the edge creates a cycle, remove the edge
                        adjacency_matrix[i][j] = 0

        return adjacency_matrix

    def is_cyclic_util(self,graph, visited, rec_stack, node):
        visited[node] = True
        rec_stack[node] = True

        for neighbor in range(len(graph)):
            if graph[node][neighbor] == 1:
                if not visited[neighbor]:
                    if self.is_cyclic_util(graph, visited, rec_stack, neighbor):
                        return True
                elif rec_stack[neighbor]:
                    return True

        rec_stack[node] = False
        return False

    def is_cyclic(self,graph):
        num_nodes = len(graph)
        visited = [False] * num_nodes
        rec_stack = [False] * num_nodes

        for node in range(num_nodes):
            if not visited[node]:
                if self.is_cyclic_util(graph, visited, rec_stack, node):
                    return True

        return False
    
    
if __name__ == '__main__':
# Example usage:
    num_nodes = 5 #number of tasks
    density = 0.8
    random_dag = TaskGen(num_nodes,3)
    print(random_dag.gen_comp_matrix())
    test_dag = random_dag.generate_random_dag(density)

    print(test_dag)


