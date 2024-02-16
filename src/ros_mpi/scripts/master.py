from cgi import test
from tracemalloc import take_snapshot

import numpy as np
from util import Master,Worker
from orchestrator import Orchestrator
from taskgen import TaskGen
import rospy,random
from hector_uav_msgs.msg import Task
import threading
import configparser
from mpi4py import MPI


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

config = configparser.ConfigParser()
config.read('/home/jxie/rossim/src/ros_mpi/scripts/property.properties')
max_cpu = int(config.get('UAV','max_cpu'))
min_cpu = int(config.get('UAV','min_cpu'))

numberOfTask = int(config.get('Task','numberOfTask'))
numberOfComputingNode = int(config.get('Task','computing'))
density = float(config.get('Task','density'))


taskgenerator = TaskGen(numberOfTask,numberOfComputingNode)

comp = taskgenerator.gen_comp_matrix()
comm = taskgenerator.generate_random_dag(density)
print(comm)
print(comp)

testOchestrator = Orchestrator(comm,comp)
# line 64: representing the task priorities 
rank_up_values = [testOchestrator.calculate_rank_up_recursive(testOchestrator.comp,testOchestrator.comm,i) for i in range(len(testOchestrator.comp))]
# print("at line 93: ", np.argsort(rank_up_values)[::-1])
testOchestrator.heft()
# heft_list = testOchestrator.task_schedule_list

comm = MPI.COMM_WORLD
num_node = comm.Get_size()
node_id = comm.Get_rank()
node_name = MPI.Get_processor_name()



if node_id == 0:
    master = Master(int(random.randrange(min_cpu,max_cpu)))
    master.run(testOchestrator.mes)
else:
    worker = Worker(node_id,int(random.randrange(int(min_cpu),int(max_cpu))))
    worker.run()

print('All parallel tasks are done!')

MPI.Finalize()