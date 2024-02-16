from cgi import test

import numpy as np
from util import Master,Worker
from orchestrator import Orchestrator
import rospy
from hector_uav_msgs.msg import Task
import threading

from mpi4py import MPI


comp = [[14, 16, 9],
        [13, 19, 18],
        [11, 13, 19],
        [13, 8, 17],
        [12, 13, 10],
        [13, 16, 9],
        [7, 15, 11],
        [5, 11, 4],
        [18, 12, 20],
        [21, 7, 16]]

# UAV communication matrix
comm = [[0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

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
    master = Master()
    master.run(testOchestrator.mes)
else:
    worker = Worker(node_id)
    worker.run()
# if node_id == 1:
#     worker = Worker(node_id)
#     worker.run()

# if node_id == 2:
#     worker = Worker(node_id)
#     worker.run()



# master = Master()

# worker_threads = []
# for i in range(0,3):
#     if i == 0:
#         worker_threads.append(threading.Thread(target=Master().run(testTasks))) #Master().run(testTask)
#     else:
#         worker_threads.append(threading.Thread(target=Worker(i+1).run())) #Worker(i+1)

# for t in worker_threads:
#     t.start()

# for t in worker_threads:
#     t.join()

# uavs = []
# for i in range(0,2):
#     uavs.append(Worker(i+1))


# my_node = MyNode(uavs)

# # Create a thread for the publisher
# publisher_thread = threading.Thread(target=my_node.publish_data)

# # Start the threads
# publisher_thread.start()

# # Run the ROS event loop
# rospy.spin()

# # Wait for threads to finish
# publisher_thread.join()


print("done")