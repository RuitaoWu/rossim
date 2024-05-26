
from ast import Raise
import numpy as np
# from torch import _test_autograd_multiple_dispatch
from util import Master, Node,Worker, WorkerNode
from indep import Parent, Child
from orchestrator import Orchestrator
from taskgen import TaskGen
import rospy,random,os
# from hector_uav_msgs.msg import Task
# import threading
import configparser
from mpi4py import MPI
# from read_dag import read_dag

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
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created.")
    except:
        print(f"Folder '{folder_path}' already exists.")

# Example usage:
# folder_path = '/home/jxie/rossim/src/ros_mpi/data'
# task_succ_path = '/home/jxie/rossim/src/ros_mpi/task_succ'
folder_path = '../data'
task_succ_path = '../task_succ'

create_folder_if_not_exists(folder_path)
create_folder_if_not_exists(task_succ_path)
# if not os.path('/home/jxie/rossim/src/ros_mpi/data_indep'):
#     os.mkdir('/home/jxie/rossim/src/ros_mpi/data_indep')
# else:
#     print(f"Folder '{'/home/jxie/rossim/src/ros_mpi/data_indep'}' already exists.")
config = configparser.ConfigParser()
# config.read('/rossim/src/ros_mpi/scripts/property.properties')
config.read('property.properties')
max_cpu = int(config.get('UAV','max_cpu'))
min_cpu = int(config.get('UAV','min_cpu'))
sleep_time = float(config.get('UAV','sleep_time'))
numberOfTask = int(config.get('Task','numberOfTask'))
numberOfComputingNode = int(config.get('Task','computing'))
density = float(config.get('Task','density'))
taskType = config.get('Task','task_type')
master_node = int(config.get('Task','master_uav'))
max_iter = int(config.get('Task','maxiter'))
# taskgenerator = TaskGen(numberOfTask,numberOfComputingNode)
task_size_min = int(config.get('Task','task_size_min'))
task_size_max = int(config.get('Task','task_size_max'))
ipsMax = int(config.get('Task','ips_max'))
ipsMin = int(config.get('Task','ips_min'))
# taskgenerator = TaskGen(numberOfTask,numberOfComputingNode,task_size_min,task_size_max,ipsMin,ipsMax)
# comm = taskgenerator.generate_random_dag(density)
# print(f'task list {testOchestrator.mes}')
comm = MPI.COMM_WORLD
num_node = comm.Get_size()
node_id = comm.Get_rank()
node_name = MPI.Get_processor_name()
if taskType == 'Independent':

    try:
        if node_id == 0:
            node_verify = "Master"
            nodeMaster = Node(node_id+1,node_verify,[],int(random.randrange(int(min_cpu),int(max_cpu))),0,[])
            nodeMaster.run()
        else:
            node_verify = "Worker%d"%(node_id+1)
            nodeWorker = WorkerNode(node_id+1,node_verify,int(random.randrange(int(min_cpu),int(max_cpu))),0,[])
            nodeWorker.run()
    except rospy.ROSInterruptException:
        print('ROS shutdown, key interruptted')

elif taskType == 'Dependent':

    if node_id == 0:
        taskgenerator = TaskGen(numberOfTask,numberOfComputingNode,task_size_min,task_size_max,ipsMin,ipsMax)
        # comp = [[14,16,9],
        #                 [13,19,18],
        #                 [11,13,19],
        #                 [13,8,17],
        #                 [12,13,10],
        #                 [13,16,9],
        #                 [7,15,11],
        #                 [5,11,4],
        #                 [18,12,20],
        #                 [21,7,16]]

        # comm = [[0,18,12,9,11,14,0,0,0,0],
        #         [0,0,0,0,0,0,0,19,16,0],
        #         [0,0,0,0,0,0,23,0,0,0],
        #         [0,0,0,0,0,0,0,27,23,0],
        #         [0,0,0,0,0,0,0,0,13,0],
        #         [0,0,0,0,0,0,0,15,0,0],
        #         [0,0,0,0,0,0,0,0,0,17],
        #         [0,0,0,0,0,0,0,0,0,11],
        #         [0,0,0,0,0,0,0,0,0,13],
        #         [0,0,0,0,0,0,0,0,0,0]]
        comp = [[0.0, 0.0, 0.0], [92.0, 83.0, 72.0], [73.0, 63.0, 72.0], [26.0, 24.0, 28.0], [95.0, 84.0, 95.0], [58.0, 63.0, 78.0], [34.0, 33.0, 31.0], [86.0, 93.0, 95.0], [48.0, 42.0, 31.0], [75.0, 63.0, 70.0], [28.0, 23.0, 22.0], [24.0, 36.0, 26.0], [37.0, 54.0, 50.0], [97.0, 103.0, 101.0], [113.0, 87.0, 103.0], [83.0, 62.0, 58.0], [54.0, 55.0, 41.0], [38.0, 29.0, 39.0], [97.0, 81.0, 90.0], [98.0, 111.0, 160.0], [49.0, 77.0, 64.0], [0.0, 0.0, 0.0]]
        comm =[[-1, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, 46, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, 55, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, 42, 41, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, 40, -1, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 36, -1, 48, -1, -1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 20, -1, 45, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 49, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 61, -1, 27, 50, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 38, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 41, -1], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0], [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
    
        testOchestrator = Orchestrator(comm,comp,task_size_min,task_size_max)
        # testOchestrator.heft()
        testOchestrator.orch_ipef()
        print('list: ', testOchestrator.task_schedule_list)
        master = Master(node_id+1,int(random.randrange(min_cpu,max_cpu)),sleep_time)
        print('waiting....')
        master.run(testOchestrator.mes)

    else:
        worker = Worker(node_id+1,int(random.randrange(int(min_cpu),int(max_cpu))),sleep_time)
        print('worker ',node_id+1,' waiting....')
        worker.run()
else:
    if node_id == 0:
        parent = Parent((node_id+1))
        parent.run()
    else:
        child = Child((node_id+1))
        child.run()

print('All parallel tasks are done!')

MPI.Finalize()
