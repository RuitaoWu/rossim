from cgi import test
from tracemalloc import take_snapshot

import numpy as np
from util import Master, Node,Worker, WorkerNode
from orchestrator import Orchestrator
from taskgen import TaskGen
import rospy,random,os
from hector_uav_msgs.msg import Task
import threading
import configparser
from mpi4py import MPI

from dataplot import PlotGraph

# comp = [[14, 16, 9],
#         [13, 19, 18],
#         [11, 13, 19],
#         [13, 8, 17],
#         [12, 13, 10],
#         [13, 16, 9],
#         [7, 15, 11],
#         [5, 11, 4],
#         [18, 12, 20],
#         [21, 7, 16]]

# # UAV communication matrix
# comm = [[0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
#                  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

# Example usage:
folder_path = '/home/jxie/rossim/src/ros_mpi/data_indep'

create_folder_if_not_exists(folder_path)
# if not os.path('/home/jxie/rossim/src/ros_mpi/data_indep'):
#     os.mkdir('/home/jxie/rossim/src/ros_mpi/data_indep')
# else:
#     print(f"Folder '{'/home/jxie/rossim/src/ros_mpi/data_indep'}' already exists.")
config = configparser.ConfigParser()
config.read('/home/jxie/rossim/src/ros_mpi/scripts/property.properties')
max_cpu = int(config.get('UAV','max_cpu'))
min_cpu = int(config.get('UAV','min_cpu'))
sleep_time = float(config.get('UAV','sleep_time'))
numberOfTask = int(config.get('Task','numberOfTask'))
numberOfComputingNode = int(config.get('Task','computing'))
density = float(config.get('Task','density'))
taskType = config.get('Task','task_type')
master_node = int(config.get('Task','master_uav'))
max_iter = int(config.get('Task','maxiter'))
taskgenerator = TaskGen(numberOfTask,numberOfComputingNode)
task_size_min = int(config.get('Task','task_size_min'))
task_size_max = int(config.get('Task','task_size_max'))
comp = taskgenerator.gen_comp_matrix()
comm = taskgenerator.generate_random_dag(density)


testOchestrator = Orchestrator(comm,comp,task_size_min,task_size_max)
# line 64: representing the task priorities 
rank_up_values = [testOchestrator.calculate_rank_up_recursive(testOchestrator.comp,testOchestrator.comm,i) for i in range(len(testOchestrator.comp))]
# print("at line 93: ", np.argsort(rank_up_values)[::-1])
testOchestrator.heft()
# heft_list = testOchestrator.task_schedule_list

comm = MPI.COMM_WORLD
num_node = comm.Get_size()
node_id = comm.Get_rank()
node_name = MPI.Get_processor_name()
if taskType == 'Independent':
    #at begnining of each iteration it will define new empty task queue
    for x in range(0,1):
        print(f'current iteration {x}')
        if node_id  == master_node:
            node_verify = "Master"
            nodeMaster = Node(node_id+1,node_verify,testOchestrator.mes,int(random.randrange(int(min_cpu),int(max_cpu))),x,[])
            nodeMaster.run()
        else:
            node_verify = "Worker%d"%(node_id+1)
            nodeWorker = WorkerNode(node_id+1,node_verify,int(random.randrange(int(min_cpu),int(max_cpu))),x,[])
            nodeWorker.run()
        print(f'finished iteration {x}')
    
    # if node_id  == master_node:
    #     node_verify = "Master"
    #     nodeMaster = Node(node_id+1,node_verify,testOchestrator.mes,int(random.randrange(int(min_cpu),int(max_cpu))))
    #     nodeMaster.run()
    # else:
    #     node_verify = "Worker%d"%(node_id+1)
    #     nodeWorker = WorkerNode(node_id+1,node_verify,int(random.randrange(int(min_cpu),int(max_cpu))))
    #     nodeWorker.run()
elif taskType == 'Dependant':

    if node_id == 0:
        master = Master(node_id+1,int(random.randrange(min_cpu,max_cpu)),sleep_time)
        # print(f'all tasks {testOchestrator.mes}')
        master.run(testOchestrator.mes)
        # savegraph = PlotGraph(node_id+1)
        # savegraph.run()
    else:
        worker = Worker(node_id+1,int(random.randrange(int(min_cpu),int(max_cpu))),sleep_time)
        worker.run()
        # savegraph = PlotGraph(node_id+1)
        # savegraph.run()
else:
    print(f'The input task type {taskType} is invalid, either Dependant or Independent')

print('All parallel tasks are done!')

MPI.Finalize()
