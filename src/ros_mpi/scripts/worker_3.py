#!/usr/bin/env python

from hmac import new
from platform import node
import rospy,time,os,pickle,math,threading
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped
from hector_uav_msgs.msg import Task,FinishTime
from orchestrator import Orchestrator
from datarate import Datarate
# PKG = 'ros_mpi'
# import roslib; roslib.load_manifest(PKG)
task = Task()
task.task_idx = -1
task.size = -1
task.processor_id = -1
task.dependency =[-1]
global_data = []
topic_two = '/uav1/task/worker3'
topic_fromworker = '/uav2/task/worker3'

topic_master = '/uav3/task/master'
topic_worker = '/uav3/task/worker2'

master_pos='/uav1/ground_truth_to_tf/pose'
worker_one = '/uav2/ground_truth_to_tf/pose'
worker_two = '/uav3/ground_truth_to_tf/pose'

finish_time_worker_3 = '/uav1/finish/worker3'

# pub1 = rospy.Publisher(topic_master, Fi, queue_size=10)
pub1 = rospy.Publisher(topic_master, FinishTime, queue_size=10)
pub2 = rospy.Publisher(topic_worker, FinishTime, queue_size=10)

task_info=[]
task_received,data_rate_one,data_rate_two = [],[1004830000],[1004830000]
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

""" comm = [[0, 18, 12, 9, 11, 14, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 19, 16, 0],
                 [0, 0, 0, 0, 0, 0, 23, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 27, 23, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 13, 0],
                 [0, 0, 0, 0, 0, 0, 0, 15, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 17],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] """
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
# rank_up_values = [testOchestrator.calculate_rank_up_recursive(testOchestrator.comp,testOchestrator.comm,i) for i in range(len(testOchestrator.comp))]
# print("at line 93: ", np.argsort(rank_up_values)[::-1])

testOchestrator.heft()
heft_list = testOchestrator.task_schedule_list
print(heft_list)
comm_time_one,comm_time_two = [],[]

datarate_module = Datarate()
def locatetask(schedulist,task):
    for x in schedulist:
        if task in x:return schedulist.index(x)

last_message_time=[0]

def pred_time(t):
    pred_list = testOchestrator.predecessor_task(t)
    temp_time =[0]
    if len(task_received) != 0:
        for i in pred_list:
            for j in task_received:
                if i == j.task_id:
                    temp_time.append(j.actual_finish_time)
    return max(temp_time)
# def from_master(data):
#     # task_info.append({'task_id':data.task_idx,'start_time':rospy.get_time(),'end_time':rospy.get_time()+comp[data.task_idx][2]/1000,'duration':comp[data.task_idx][2]/1000})
#     print('receivded task',data)
#     ros_cost = rospy.get_time() - last_message_time[-1]
#     trans_cost = data.size/ data_rate_two[-1]
#     last_message_time.append(rospy.get_time())
#     temp_start = last_message_time[-1] +(max(ros_cost,trans_cost))
#     if len(task_info) == 0:
#         task_info.append({'task_id':data.task_idx,'start_time':temp_start,
#                         'end_time':temp_start+comp[data.task_idx][2],
#                         'duration':comp[data.task_idx][2]})
#     else:
#         s_time = max(task_info[-1]['end_time'],pred_time(data.task_idx))
#         e_time = s_time+comp[data.task_idx][2]
#         task_info.append({'task_id':data.task_idx,'start_time':s_time,
#                         'end_time':e_time,
#                         'duration':comp[data.task_idx][2]})
#     print('at line 114 ',task_info[-1]['start_time'])
#     # global_data.append(data)
#     # rospy.sleep(comp[data.task_idx][2])
#     for x in data.dependency:
#         if locatetask(heft_list,x) == 0:
#             print('publishing task ', data.task_idx,' to master')
#             ft = FinishTime()
#             ft.task_id = data.task_idx
#             # ft.actual_finish_time = rospy.get_time() +comp[data.task_idx][2]
#             ft.actual_finish_time = task_info[-1]['end_time']
#             pub1.publish(ft)
#         elif locatetask(heft_list,x) == 1:
#             print('publishing task ', data.task_idx,' to worker 2') 
#             ft2 = FinishTime()
#             ft2.task_id = data.task_idx
#             # ft2.actual_finish_time = rospy.get_time() +comp[data.task_idx][2] 
#             ft2.actual_finish_time = task_info[-1]['end_time']   
#             pub2.publish(ft2)
#         else:
#             print(f'process task {x} on worker 3')
def from_master(data):
    print('receivded task',data)
    start = rospy.get_time()
    rospy.sleep(comp[data.task_idx][1])
    end = rospy.get_time()
    # ros_cost = rospy.get_time() - last_message_time[-1]
    trans_cost = data.size/ data_rate_two[-1]
    last_message_time.append(rospy.get_time())
    # temp_start = last_message_time[-1] +(max(ros_cost,trans_cost))
    if len(task_info) == 0:
        task_info.append({'task_id':data.task_idx,'start_time':max(start,pred_time(data.task_idx))+ trans_cost,
                        'end_time':max(start,pred_time(data.task_idx))+comp[data.task_idx][2]+ trans_cost,
                        'duration':+comp[data.task_idx][1]})
    else:
        s_time = max(task_info[-1]['end_time'],pred_time(data.task_idx))
        e_time = s_time+comp[data.task_idx][2]
        task_info.append({'task_id':data.task_idx,'start_time':s_time,
                        'end_time':e_time,
                        'duration':comp[data.task_idx][2]})

    for x in data.dependency:
        if locatetask(heft_list,x) == 0:
            print('publishing task ', data.task_idx,' to master')
            ft = FinishTime()
            ft.task_id = data.task_idx
            # ft.actual_finish_time = rospy.get_time() +comp[data.task_idx][2]
            ft.actual_finish_time = task_info[-1]['end_time']
            pub1.publish(ft)
        elif locatetask(heft_list,x) == 1:
            print('publishing task ', data.task_idx,' to worker 2') 
            ft2 = FinishTime()
            ft2.task_id = data.task_idx
            ft2.actual_finish_time = task_info[-1]['end_time']   
            pub2.publish(ft2)
        else:
            print(f'process task {x} on worker 3')
def from_worker(data,rec_time):
    print(f'cost time from master { rospy.get_time() - last_message_time[-1]}')
    last_message_time.append(rospy.get_time())
    print(f'last message time {last_message_time[-1]}')
    # global_data.append(data)
    if data not in task_received:
        task_received.append(data)
    print('I heard from worker 2', data)

position_uav = []   
def callback_position(data):
    x,y,z = data.pose.position.x,data.pose.position.y,data.pose.position.z
    if [x,y,z] not in position_uav:
        position_uav.append([x,y,z])

def subc_thread_1(): #hear from master
    rospy.Subscriber(topic_two, Task, from_master)

def subc_thread_2():
    rospy.Subscriber(topic_fromworker,FinishTime,from_worker,rospy.get_time())

def subc_thread_3():
    rospy.Subscriber(finish_time_worker_3,FinishTime,from_worker,rospy.get_time())
def position():
    subposition = '/uav2/ground_truth_to_tf/pose'
    # pos = rospy.wait_for_message(subposition,PoseStamped)
    rospy.Subscriber(subposition,PoseStamped,callback_position)

def listener():
    print('call listener...')
    rospy.init_node('Worker3', anonymous=True)
    # pos_master = rospy.wait_for_message(master_pos, PoseStamped)
    # pos_worker_one = rospy.wait_for_message(worker_one, PoseStamped)
    # pos_worker_two = rospy.wait_for_message(worker_two, PoseStamped)
    # data_rate_one.append(datarate_module.data_rate(datarate_module.channel_gain(math.dist([pos_master.pose.position.x,pos_master.pose.position.y],[pos_worker_one.pose.position.x,pos_worker_one.pose.position.y]))))
    # data_rate_two.append(datarate_module.data_rate(datarate_module.channel_gain(math.dist([pos_master.pose.position.x,pos_master.pose.position.y],[pos_worker_two.pose.position.x,pos_worker_two.pose.position.y]))))
    thread1 = threading.Thread(target=subc_thread_1)
    thread2 = threading.Thread(target=subc_thread_2)
    thread3 = threading.Thread(target=subc_thread_3)
    thread4 = threading.Thread(target=position)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    # rospy.Subscriber(topic_two, Task, from_master)
    # rospy.Subscriber(topic_fromworker,FinishTime,from_worker,rospy.get_time())
    # rospy.Subscriber(finish_time_worker_3,FinishTime,from_worker,rospy.get_time())
    rospy.spin()

    if not os.path.exists('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/scripts/commtime'):
        os.makedirs('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/scripts/commtime')

    with open('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/scripts/commtime/worker_three_one.pkl','wb') as file:
        pickle.dump(comm_time_two,file)
    with open('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/scripts/commtime/worker_three_two.pkl','wb') as file:
        pickle.dump(comm_time_two,file)

if __name__ == '__main__':
    print('Worker 3 listening...')
    listener()
    print(f'task receivded from worker 2: {task_received}')
    print(task_info)
    print(f'last message time {last_message_time}')
    print('worker 3 complete')
    # for x in global_data:
    #     print(x)
    #     print('\n')
