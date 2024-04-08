import random
from hector_uav_msgs.msg import Task
from orchestrator import Orchestrator
import string
class TaskGen():

    def __init__(self,num_nodes,computing_node,taskMin,taskMax,ciMin,ciMax):
        self.computing_node = computing_node
        self.num_nodes = num_nodes
        self.taskMin = taskMin
        self.taskMax = taskMax
        self.ciMin = ciMin
        self.ciMax = ciMax
    def gen_comp_matrix(self):
        #time units: seconds
        return [[random.uniform(10,20) for _ in range(self.computing_node)] for _ in range(self.num_nodes)]
    def generate_random_dag(self,density):
        # Initialize an empty adjacency matrix
        adjacency_matrix = [[0] * self.num_nodes for _ in range(self.num_nodes)]
        print(f'genereating random DAG.......')
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
    
    def gen_indep(self):
        temp_task=[]
        app_name = "".join(random.choices(string.ascii_lowercase,k=5))
        for i in range(0,self.num_nodes):
            task = Task()
            task.task_idx = i
            task.processor_id = -1
            task.dependency=[]
            task.size = random.randint(self.taskMin,self.taskMax) #number of instructions
            # task.size = random.randint(self.taskMin,self.taskMax) 
            task.st = 0
            task.et = 0
            task.app_name = app_name
            task.ci = random.randint(self.ciMin, self.ciMax) #instruction per second
            task.delta = 0.05 #Watt
            temp_task.append(task)
        temp_task.sort(key=lambda x: x.size)
        return temp_task
if __name__ == '__main__':
# Example usage:
    num_nodes = 20 #number of tasks
    density = 0.8
    random_dag = TaskGen(num_nodes,3,40000,50000,60000,80000)
    test = random_dag.gen_indep()
    for i in range(5):
        print([x.app_name for x in test])
    # comp = random_dag.gen_comp_matrix()
    # testorchest = Orchestrator([],comp,100,200,40000,50000,60000,80000)
    # for i in testorchest.indep_sch(random_dag.gen_indep()):
    #     print(i.processor_id)
    # print(random_dag.gen_comp_matrix())
    # test_dag = random_dag.generate_random_dag(density)

    # print(test_dag)


