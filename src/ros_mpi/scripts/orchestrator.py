# Author: Ruitao Wu
# Date: 2024-03-01 12:32:53
from cgi import test
from math import ceil
from re import T
import numpy as np
from hector_uav_msgs.msg import Task
# from taskgen import TaskGen
import random
from read_dag import read_dag
from ipef import IPEFT
class Orchestrator:
    def __init__(self,comm,comp,taskMin,taskMax):
        self.rank_up_values=[]
        # Memoization cache
        self.memo = {}
        self.comm = comm
        self.comp = comp
        self.taskMin = taskMin
        self.taskMax = taskMax
        self.AST = [float('-inf')]*len(comp)
        self.AFT = [float('-inf')]*len(comp)
        self.task_schedule_list=  [[] for _ in range(len(comp[0]))]
        self.mes = []

    def calculate_rank_up_recursive(self,comp, comm, i):
        """
        The function calculates the rank of a node recursively based on its communication with other
        nodes in a network.
        
        :param comp: It seems like you were about to provide some information about the `comp` parameter,
        but the message got cut off. Could you please provide more details about the `comp` parameter so
        that I can assist you further with the `calculate_rank_up_recursive` function?
        :param comm: It seems like you were about to provide some information about the `comm` parameter,
        but the message got cut off. Could you please provide more details about the `comm` parameter so
        that I can assist you further with the `calculate_rank_up_recursive` function?
        :param i: The parameter `i` in the `calculate_rank_up_recursive` function represents the index of
        the current node for which we are calculating the rank. It is used to access the corresponding
        row in the `comp` and `comm` matrices to determine the successors of the current node
        :return: The function `calculate_rank_up_recursive` returns the calculated rank value for a given
        index `i` based on the input arrays `comp` and `comm`.
        """
        # print(f'calculating rank up value for {i}')
        # successors = [j for j in range(len(comp)) if comm[i][j] > 0]
        # print('successors: ', successors)
        # if not successors:
        #     print('returned at line 45')
        #     return np.mean(comp[i])
        
        # max_rank_j = max([comm[i][j] + self.calculate_rank_up_recursive(comp, comm, j) for j in successors])
        # print('max rank j: ', max_rank_j, 'returned')
        # return np.mean(comp[i]) + max_rank_j
    

        if i in self.memo:
            # Return cached result if available
            return self.memo[i]

        successors = [j for j in range(len(comp)) if comm[i][j] > 0]

        if not successors:
            # Base case: If no successors, return the mean computational cost
            result = np.mean(comp[i])
        else:
            # Recursive case: Calculate the rank for each successor and find the maximum
            max_rank_j = max([comm[i][j] + self.calculate_rank_up_recursive(comp, comm, j) for j in successors])
            # Store the result in the memoization cache
            result = np.mean(comp[i]) + max_rank_j

        # Cache the result before returning
        self.memo[i] = result
        return result


    #find the predecessor of current task
    def predecessor_task(self,task):
        """
        The function `predecessor_task` takes a task as input and returns a list of its predecessor tasks.
        
        :param task: The parameter "task" represents the index of a task in a list or array
        :return: a list of predecessor tasks for the given task.
        """

        pre_decessor = []
        for i in range(0, len(self.comm)):
            if self.comm[i][task] > 0:
                pre_decessor.append(i)
        return pre_decessor

    def successor(self,task):
        """
        The function "successor" takes a task as input and returns a list of its successors based on the
        values in the "comm" matrix.
        
        :param task: The parameter "task" represents current task
        :return: The function `successor` returns a list of successors for a given task.
        """
        suc_cessor = []
        for i in range(0, len(self.comm)):
            if self.comm[task][i] > 0:
                suc_cessor.append(i)
        return suc_cessor
    #find earliest idel time of current processor
    def earliest_avilable_time(self,idx):
        if self.task_schedule_list[idx] is None or len(self.task_schedule_list[idx]) == 0:
            return 0
        else:
            return max([self.AFT[x] for x in self.task_schedule_list[idx]])
    # calculate the earliest start time for current task on each processor
    def earliest_start_time(self,idx,s):
        predecessor_list = self.predecessor_task(idx)
        start_time = []
        if predecessor_list is None or len(predecessor_list) == 0:
            return 0
        else:    
            
            for p in predecessor_list:
                if p in self.task_schedule_list[s]:
                    start_time.append(self.AFT[p])
                else:
                    start_time.append(self.AFT[p]+self.comm[p][idx])
            return max(self.earliest_avilable_time(s),max(start_time))
        # calculate the earliest finish time for current task on each processor
    def earliest_finish_time(self,idx,s,est):
        return est + self.comp[idx][s]
    def update_aft(self,eft,est,task):
        self.AFT[task] = min(eft)
        self.AST[task] = est[np.argmin(eft)]
    def locate_task(self,t):
        for row in self.task_schedule_list:
                if t in row: return self.task_schedule_list.index(row)

    def heft(self):
        print('scheduling DAG based tasks......')
        # print(self.comm)
        # print(self.comp)
        TASK_FLAG=[False]*len(self.comp)
        self.rank_up_values = [self.calculate_rank_up_recursive(self.comp,self.comm,i) for i in range(len(self.comp))]
        for task in np.argsort(self.rank_up_values)[::-1]:
            # print(f'scheduling {task}')
            est =[]
            eft = []
            for s in range(0,len(self.comp[0])):
                est.append(self.earliest_start_time(task,s))
                eft.append(self.earliest_finish_time(task,s,est[s]))
                self.update_aft(eft,est,task)
            if TASK_FLAG[task] == False:
                self.task_schedule_list[np.argmin(eft)].append(task) # append task to the processor with earliest finish time
                TASK_FLAG[task] = True
                print(f'scheduled {task} on {np.argmin(eft)}')
        # print('formatting tasks......')
        task = Task()
        task.task_idx = -1
        task.processor_id = -1
        task.dependency=[]
        task.size = 0
        task.st = 0.1
        task.et = 0.1
        task.ci = 0.01 #cpu cycle for executing the task
        task.delta = 0.1 #mj per sec
        self.mes.append(task)
        for t in np.argsort(self.rank_up_values)[::-1]:
                task = Task()
                task.task_idx = t
                task.processor_id = self.locate_task(t)
                task.dependency=self.predecessor_task(t)
                task.size = random.randint(self.taskMin,self.taskMax) #number of instructions
                task.st = 0
                task.et = 0
                task.ci = random.randint(4000000, 8000000) #instruction per second
                task.delta = 0.05 #Watt
                self.mes.append(task)
         
    def indep_sch(self,tasklist):
        computing_nodes = [[] for _ in range(len(self.comp[0]))]
        print(f'scheduling tasks...')
        for task in tasklist:
            # print(f'current task {task}')
            node_idx = 0
            min_eft = float('inf')
            # Find the computing node with the earliest finish time
            for i, node_tasks in enumerate(computing_nodes):
                last_task = node_tasks[-1] if node_tasks else None
                eft = last_task.et if last_task else 0
                if eft < min_eft:
                    min_eft = eft
                    node_idx = i
            # print(f'current processor id {node_idx}')
            task.processor_id = node_idx
            task.st = min_eft
            task.et = min_eft + task.size / task.ci  # EFT calculation
            computing_nodes[node_idx].append(task)
            # print(f'current task {task} is done')
        return tasklist
        
    def orch_ipef(self):
        # self.comm = np.where(read_dag('test.dot')[-1] >= 0, 1, 0).tolist()
        self.task_schedule_list = IPEFT(file='test.dot', verbose=True, p=3, b=0.1, ccr=0.1).outcome()
        task = Task()
        task.task_idx = -1
        task.processor_id = -1
        task.dependency=[]
        task.size = 0
        task.st = 0.1
        task.et = 0.1
        task.ci = 0.01 #cpu cycle for executing the task
        task.delta = 0.1 #mj per sec
        self.mes.append(task)
        for row in IPEFT(file='test.dot', verbose=True, p=3, b=0.1, ccr=0.1).outcome():
            for t in row:
                task = Task()
                task.task_idx = t
                task.processor_id = self.locate_task(t)
                task.dependency=self.predecessor_task(t)
                task.size = random.randint(self.taskMin,self.taskMax) #number of instructions
                task.st = 0
                task.et = 0
                task.ci = random.randint(4000000, 8000000) #instruction per second
                task.delta = 50 #mW
                self.mes.append(task)
# if __name__ == '__main__':

#     comp = [[14, 16, 9],
#                     [13, 19, 18],
#                     [11, 13, 19],
#                     [13, 8, 17],
#                     [12, 13, 10],
#                     [13, 16, 9],
#                     [7, 15, 11],
#                     [5, 11, 4],
#                     [18, 12, 20],
#                     [21, 7, 16]]
#     # comm = [[0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
#     #              [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
#     #              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     #              [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
#     #              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#     #              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#     #              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     #              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     #              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     #              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#     # comm = [[0, 18, 12, 9, 11, 14, 0, 0, 0, 0],
#     #                 [0, 0, 0, 0, 0, 0, 0, 19, 16, 0],
#     #                 [0, 0, 0, 0, 0, 0, 23, 0, 0, 0],
#     #                 [0, 0, 0, 0, 0, 0, 0, 27, 23, 0],
#     #                 [0, 0, 0, 0, 0, 0, 0, 0, 13, 0],
#     #                 [0, 0, 0, 0, 0, 0, 0, 15, 0, 0],
#     #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 17],
#     #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
#     #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
#     #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#     comm = np.where(read_dag('test.dot')[-1] >= 0, 1, 0).tolist()
#     # taskgen = TaskGen(5,3)
#     # comm = taskgen.generate_random_dag()
#     # comp = taskgen.gen_comp_matrix()
#     # print(comm)
#     # print(comp)

#     testobj = Orchestrator(comm,comp,100,200)
#     testobj.orch_ipef()
#     print(testobj.comm)
#     print(testobj.mes)
#     print(testobj.locate_task(2))
