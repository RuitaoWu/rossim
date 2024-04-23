
from ast import Raise
import numpy as np
# from torch import _test_autograd_multiple_dispatch
from util import UAV, Master, Node,Worker, WorkerNode
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
    #at begnining of each iteration it will define new empty task queue
    # for x in range(0,1):
    #     print(f'current iteration {x}')
    #     try:
    #         if node_id  == master_node:
    #         # if node_id  == random.randint(0,numberOfComputingNode):
    #             node_verify = "Master"
    #             nodeMaster = Node(node_id+1,node_verify,[],int(random.randrange(int(min_cpu),int(max_cpu))),x,[])
    #             nodeMaster.run()
    #         else:
    #             node_verify = "Worker%d"%(node_id+1)
    #             nodeWorker = WorkerNode(node_id+1,node_verify,int(random.randrange(int(min_cpu),int(max_cpu))),x,[])
    #             nodeWorker.run()
    #     except:
    #         print('an error has occurred')
    #     print(f'finished iteration {x}')



    # taskgenerator = TaskGen(random.randint(numberOfTask // 2, numberOfTask),numberOfComputingNode,task_size_min,task_size_max,ipsMin,ipsMax)
    # testorchest = Orchestrator([],taskgenerator.gen_comp_matrix(),100,200)
    # testorchest.indep_sch(taskgenerator.gen_indep())
    # tempTask = taskgenerator.gen_indep()
    
    
    # for i in range(3):
    #     masterID = random.randint(1,3)
    #     print('generating tasks')
    #     taskgenerator = TaskGen(random.randint(numberOfTask // 2, numberOfTask),numberOfComputingNode,task_size_min,task_size_max,ipsMin,ipsMax)
    #     testorchest = Orchestrator([],taskgenerator.gen_comp_matrix(),100,200)
    #     tempTask = taskgenerator.gen_indep()
    #     if masterID == (node_id+1):
    #         uav = UAV((node_id+1),masterID,i,alltasks=testorchest.indep_sch(tempTask))
    #         uav.run()
    #     else:
    #         uav = UAV((node_id+1),masterID,i)
    #         uav.run()
        

    #     print(f'finished iteration {i} on master {node_id +1}')


elif taskType == 'Dependent':

    if node_id == 0:
        taskgenerator = TaskGen(numberOfTask,numberOfComputingNode,task_size_min,task_size_max,ipsMin,ipsMax)
        # comp = taskgenerator.gen_comp_matrix()
        # comm = taskgenerator.generate_random_dag(density)
        # comp = [[14, 16, 9],
        # [13, 19, 18],
        # [11, 13, 19],
        # [13, 8, 17],
        # [12, 13, 10],
        # [13, 16, 9],
        # [7, 15, 11],
        # [5, 11, 4],
        # [18, 12, 20],
        # [21, 7, 16]]
        # comp = [[12.164249102442461, 10.19234567082301, 19.35626155644548], [12.96963026584221, 17.397969055797574, 10.800366001337327], [13.308863130493055, 17.040360967433337, 13.96074696446106], [17.84351120297285, 18.820787153130347, 19.87440797081596], [11.566646484550262, 10.7740196841573, 19.178230996092097], [14.54309190422558, 18.569895504037333, 10.016734942195923], [19.589215299721335, 16.645700862654294, 14.318789302909622], [16.75996013189734, 11.097542423516382, 12.249537043195904], [14.177388247724856, 13.100957659695569, 19.529151517659663], [16.369214130739547, 17.054433482423704, 18.49604129275724], [13.001894030246003, 18.38240328697433, 16.37728842149799], [17.12881222286068, 12.120916216726918, 12.769953950274564], [11.377317047301645, 16.257311331583786, 11.419337670664682], [13.481182137184916, 19.615976261702208, 19.322822111181097], [10.2020883698409, 18.70725715404938, 16.4654729289784], [11.369355305192553, 12.973714321308229, 12.125334058996827], [13.35029603331369, 14.353637087223763, 12.516991869836236], [10.112792921728833, 16.9685729732629, 10.307279273449193], [13.125875771610502, 13.435090362953119, 13.574738690462537], [12.72582765872258, 11.946915722734635, 12.514383389218455]]


        # UAV communication matrix
        # comm = [[0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        #                 [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        #                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        #                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        # comm = [[0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1], [0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        comp = [[14,16,9],
                        [13,19,18],
                        [11,13,19],
                        [13,8,17],
                        [12,13,10],
                        [13,16,9],
                        [7,15,11],
                        [5,11,4],
                        [18,12,20],
                        [21,7,16]]

        comm = [[0,18,12,9,11,14,0,0,0,0],
                [0,0,0,0,0,0,0,19,16,0],
                [0,0,0,0,0,0,23,0,0,0],
                [0,0,0,0,0,0,0,27,23,0],
                [0,0,0,0,0,0,0,0,13,0],
                [0,0,0,0,0,0,0,15,0,0],
                [0,0,0,0,0,0,0,0,0,17],
                [0,0,0,0,0,0,0,0,0,11],
                [0,0,0,0,0,0,0,0,0,13],
                [0,0,0,0,0,0,0,0,0,0]]
        # comm = np.where(read_dag('test.dot')[-1] >= 0, 1, 0).tolist()
        # print(comm)
        # print(comp)
        # print(f'communication matrix {comm}')
        testOchestrator = Orchestrator(comm,comp,task_size_min,task_size_max)
        # line 64: representing the task priorities 
        # rank_up_values = [testOchestrator.calculate_rank_up_recursive(testOchestrator.comp,testOchestrator.comm,i) for i in range(len(testOchestrator.comp))]
        # print("at line 93: ", np.argsort(rank_up_values)[::-1])
        testOchestrator.heft()
        print('list: ', testOchestrator.task_schedule_list)
        # testOchestrator.orch_ipef()
        # heft_list = testOchestrator.task_schedule_list
        # print('scheduleing list:   ',testOchestrator.task_schedule_list)
        master = Master(node_id+1,int(random.randrange(min_cpu,max_cpu)),sleep_time)
        print('waiting....')
        master.run(testOchestrator.mes)

    else:
        worker = Worker(node_id+1,int(random.randrange(int(min_cpu),int(max_cpu))),sleep_time)
        print('worker ',node_id+1,' waiting....')
        worker.run()
else:
    print(f'The input task type {taskType} is invalid, either Dependant or Independent')

print('All parallel tasks are done!')

MPI.Finalize()
