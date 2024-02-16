from cgi import test
from re import T
import numpy as np
from hector_uav_msgs.msg import Task
from taskgen import TaskGen
class Orchestrator:
    def __init__(self,comm,comp):
        self.rank_up_values=[]
        self.comm = comm
        self.comp = comp
        self.AST = [float('-inf')]*len(comp)
        self.AFT = [float('-inf')]*len(comp)
        self.task_schedule_list=  [[] for _ in range(len(comp[0]))]
        self.mes = []
    def calculate_rank_up_recursive(self,comp, comm, i):
        successors = [j for j in range(len(comp)) if comm[i][j] > 0]
        
        if not successors:
            return np.mean(comp[i])
        
        max_rank_j = max([comm[i][j] + self.calculate_rank_up_recursive(comp, comm, j) for j in successors])
        return np.mean(comp[i]) + max_rank_j


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

    def heft(self):
        TASK_FLAG=[False]*len(self.comp)
        self.rank_up_values = [self.calculate_rank_up_recursive(self.comp,self.comm,i) for i in range(len(self.comp))]
        for task in np.argsort(self.rank_up_values)[::-1]:
            est =[]
            eft = []
            for s in range(0,len(self.comp[0])):
                est.append(self.earliest_start_time(task,s))
                eft.append(self.earliest_finish_time(task,s,est[s]))
                self.update_aft(eft,est,task)
            if TASK_FLAG[task] == False:
                self.task_schedule_list[np.argmin(eft)].append(task) # append task to the processor with earliest finish time
                TASK_FLAG[task] = True
        for row in self.task_schedule_list:
            for col in row:
                task = Task()
                task.task_idx = col
                task.processor_id = self.task_schedule_list.index(row)
                task.dependency=self.predecessor_task(col)
                task.size = 1000000
                self.mes.append(task)
        


    
    def heft2(self,task,server):
        est=[]
        eft=[]
        #update communication information
        for s in server:
            est.append(self.earliest_start_time(task,s))
            eft.append(self.earliest_finish_time(task,s,est[s]))
            self.update_aft(eft,est,task)
        self.task_schedule_list[np.argmin(eft)].append(task) 
        print(f'ast {self.AST}')
        print(f'aft {self.AFT}')
        return np.argmin(eft)

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
#     comm = [[0, 18, 12, 9, 11, 14, 0, 0, 0, 0],
#                     [0, 0, 0, 0, 0, 0, 0, 19, 16, 0],
#                     [0, 0, 0, 0, 0, 0, 23, 0, 0, 0],
#                     [0, 0, 0, 0, 0, 0, 0, 27, 23, 0],
#                     [0, 0, 0, 0, 0, 0, 0, 0, 13, 0],
#                     [0, 0, 0, 0, 0, 0, 0, 15, 0, 0],
#                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 17],
#                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
#                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
#                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#     # taskgen = TaskGen(5,3)
#     # comm = taskgen.generate_random_dag()
#     # comp = taskgen.gen_comp_matrix()
#     # print(comm)
#     # print(comp)

#     testobj = Orchestrator(comm,comp)
#     testobj.heft()
#     # print(comm)
#     # print(comp)
#     print(testobj.task_schedule_list)
#     print(testobj.mes)
