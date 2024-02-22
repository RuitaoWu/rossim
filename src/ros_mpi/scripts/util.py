
from concurrent.futures import thread
import pickle

import time
from turtle import pos
from collections import defaultdict
from hector_uav_msgs.msg import Task, FinishTime
from orchestrator import Orchestrator
import rospy,threading
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32MultiArray



task_ast = defaultdict(list)
task_aft = defaultdict(list)

class Node:
    def __init__(self,node_id,nodeVerify,allTasks,cpu,iteration,taskqueue) -> None:
        self.node_id = node_id
        self.taskQueue = taskqueue
        self.nodeVerify = nodeVerify
        self.pubTopic = 'pub/task'
        self.recTopic = 'rec/task'
        self.allTasks = allTasks
        self.cpu = cpu
        self.iteration = iteration
        rospy.init_node(self.nodeVerify, anonymous=True)
        self.pub = rospy.Publisher(self.pubTopic,Task,queue_size=10)
        self.rate = rospy.Rate(1) # 10hz
        # rospy.Subscriber(self.pubTopic, Task, self.sub_callback)
        # self.pos = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose' %self.node_id, PoseStamped)
        print(f'Master construction completed node id {self.node_id}')

    def run(self):
        print(f'publishing...')

        for t in self.allTasks:
            pos = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose' %self.node_id, PoseStamped)
            print(f'current master {self.node_id} position {(pos.pose.position.x,pos.pose.position.y,pos.pose.position.z)}')
            if t.processor_id == self.node_id -1:
                t.st = self.taskQueue [-1].et if self.taskQueue else 0
                t.et = t.st + float(t.size / self.cpu) 
                self.taskQueue.append(t)
            else: 
                print(f'publish task {t.task_idx} to worker {t.processor_id}')
                self.pub.publish(t)
                rospy.sleep(1) 
        #task on master
        print(f'all tasks on master node {len(self.taskQueue)}')
        with open('/home/jxie/rossim/src/ros_mpi/data_indep/iter_%d_master%d.txt'%(self.iteration,self.node_id),'w') as file:
            for ele in self.taskQueue :
                file.write(f"{ele}\n\n")
class WorkerNode:
        def __init__(self,node_id,nodeVerify,cpu,iteration,taskqueue) -> None:
            self.node_id = node_id
            self.taskQueue = taskqueue
            self.nodeVerify = nodeVerify
            self.pubTopic = 'pub/task'
            self.loc = '/uav%d/ground_truth_to_tf/pose'%self.node_id
            self.cpu = cpu
            self.iteration = iteration
            rospy.init_node(self.nodeVerify, anonymous=True)
            rospy.Subscriber(self.pubTopic, Task, self.sub_callback)
            # self.pos = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose' %self.node_id, PoseStamped)
 
        def sub_callback(self,data):
            # print(f'current worker {self.node_id} location {self.pos}')
            pos = rospy.wait_for_message(self.loc,PoseStamped)
            print(f'current worker {self.node_id} position {(pos.pose.position.x,pos.pose.position.y,pos.pose.position.z)}')
            if data.processor_id == self.node_id -1 :
                data.st = self.taskQueue [-1].et if self.taskQueue else 0
                data.et = data.st + float(data.size / self.cpu) 
                self.taskQueue.append(data)

                print(f'worker {self.node_id} received task {self.taskQueue[-1].task_idx} ')
                # with open('/home/jxie/rossim/src/ros_mpi/data_indep/uav%d.txt'%self.node_id,'w') as file:
                #     for ele in self.taskQueue :
                #         file.write(f"{ele}\n\n")
                # with open('/home/jxie/rossim/src/ros_mpi/data_indep/uav%d%s.txt'%(self.node_id,time.strftime("%Y%m%d-%H%M%S")),'w') as file:
                #     for ele in self.taskQueue :
                #         file.write(f"{ele}\n\n")
            else:
                print('nothing...')

        
        def run(self):
            print('call worker%d'%self.node_id )
            # omd = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose' %self.node_id, PoseStamped)
            # print(f'omd current worker {self.node_id} at {omd.pose.position}')
            # rospy.Subscriber(self.pubTopic, Task, self.sub_callback)
            
            rospy.spin()
            print(f'saveing task queue to file..')
            with open('/home/jxie/rossim/src/ros_mpi/data_indep/iter_%d_uav%d.txt'%(self.iteration,self.node_id),'w') as file:
                for ele in self.taskQueue :
                    file.write(f"{ele}\n\n")
            
            print('saved')

######################################################################################################
####                                     dependent task                                           ####
####                                                                                              ####
####                                                                                              ####
######################################################################################################
class Master:
    def __init__(self,cpu,sleepTime) -> None:
        print('construcing master node')
        self.topic = '/uav1/task'
        self.loc = '/uav1/ground_truth_to_tf/pose'
        self.worker_to_uav = '/worker/task'
        rospy.init_node('Master', anonymous=True)
        self.pub = rospy.Publisher(self.topic,Task,queue_size=10)
        self.rate = rospy.Rate(1) # 10hz
        self.master_task = []
        self.task_received = []
        self.cpu = cpu
        self.sleepTime = sleepTime
        # self.pos = rospy.wait_for_message(self.loc, PoseStamped)

    # def pred_aft(self,t):
    #     temp =[0]
    #     for pre in t.dependency:
    #         if task_aft[pre]:
    #             temp.append(task_aft[pre])
    #     return max(temp)
    def pred_aft(self,t):
        temp =[0]
        
        for pre in t.dependency:
            for x in self.task_received:
                if pre == x.task_idx:
                    temp.append(x.et)
        print(f'max finished time for task {t.task_idx} is {temp}')
        return max(temp)

    def update_time(self):
        for x in self.task_received:
            x.st = max(self.pred_aft(x),x.st)
            x.et = x.st + (x.size/self.cpu)


    def sub_callback(self,data):
        if data:
            self.task_received.append(data)
            # self.update_time()
        else:
            print('nothing...')

    def received_call_back(self):
        print('call receive threading...')
        rospy.Subscriber(self.worker_to_uav,Task,self.sub_callback)
    
    def location_call_back(self,data):
        if data:
            print(f'current master location {(data.pose.position.x,data.pose.position.y,data.pose.position.z)}')
    def location(self):
        print('threading location...')
        pos = rospy.wait_for_message(self.loc, PoseStamped)
        # rospy.Subscriber(self.loc,PoseStamped,self.location_call_back)
        print(f'current master location {(pos.pose.position.x,pos.pose.position.y,pos.pose.position.z)}')

    def run(self,dt):
        print(f'publishing...')
        thread = threading.Thread(target= self.received_call_back)
        # thread_loc = threading.Thread(target=self.location)
        # thread_loc.start()
        thread.start()

        # rospy.Subscriber(self.worker_to_uav,Task,self.sub_callback)
        for x in dt:
            pos = rospy.wait_for_message(self.loc,PoseStamped)
            print(f'current master {1} position {(pos.pose.position.x,pos.pose.position.y,pos.pose.position.z)}')
            if x.processor_id == 0:

                x.st = max(self.master_task[-1].et, self.pred_aft(x)) if self.master_task else self.pred_aft(x)
                print(f'current task {x.task_idx} start {x.st}')
                x.et = x.st + (x.size/self.cpu)
                self.master_task.append(x)
            else:
                x.st = self.pred_aft(x)
            self.pub.publish(x)

            rospy.sleep(self.sleepTime)  
        
        #all tasks
        # with open('/home/jxie/rossim/src/ros_mpi/data/task_ast_master.pkl','w') as file:
            # for ele in self.task_received :
            #     file.write(f"{ele}\n\n")
        with open('/home/jxie/rossim/src/ros_mpi/data/uav0.pkl','wb') as file:
            pickle.dump(self.master_task,file)
        #task on master
        # with open('/home/jxie/rossim/src/ros_mpi/data/task_on_master.txt','w') as file:
        #     for ele in self.master_task :
        #         file.write(f"{ele}\n\n")
        





class Worker:
    def __init__(self,worker_id,cpu,sleepTime) -> None:
        print('constructing worker node ',worker_id)
        self.worker_id = worker_id
        self.topic = '/uav1/task'
        self.worker_to_uav = '/worker/task'
        self.loc = '/uav%d/ground_truth_to_tf/pose'%self.worker_id
        rospy.init_node('Worker%d'%self.worker_id , anonymous=True)
        self.pub = rospy.Publisher(self.worker_to_uav,Task,queue_size=20)
        self.worker_task = []
        self.all_task = []
        self.cpu = cpu
        self.sleepTime = sleepTime
        rospy.Subscriber(self.topic, Task, self.callback_func)
        # self.pos = rospy.wait_for_message(self.loc,PoseStamped)
    def pred_aft(self,t):
        temp =[0]
        for pre in t.dependency:
            for x in self.all_task:
                if pre == x.task_idx:
                    temp.append(x.et)
        return max(temp)

        #sub location information
    # def location_thread(self):
    #     pos = rospy.wait_for_message(self.loc, PoseStamped)
    #     print(f'current worker location : ({pos.pose.position.x},{pos.pose.position.y})')
    def callback_func(self,data):
        pos = rospy.wait_for_message(self.loc,PoseStamped)
        print(f'current worker {self.worker_id} position {(pos.pose.position.x,pos.pose.position.y,pos.pose.position.z)}')
        self.all_task.append(data)
        # print(f'at line 124 received task  {data.task_idx} start {data.st}')
        if data.processor_id == self.worker_id -1 :
            data.st = max(self.worker_task[-1].et, self.pred_aft(data),data.st) if self.worker_task else max(self.pred_aft(data),data.st)
            data.et = data.st +(data.size / self.cpu)
            self.pub.publish(data)
            rospy.sleep(self.sleepTime)
            self.worker_task.append(data)
            # with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.pkl'%self.worker_id,'wb') as file:
            #     pickle.dump(self.worker_task,file)
        else:
            print('empty')

    def sub_thread(self):
        rospy.Subscriber(self.topic, Task, self.callback_func)
    def run(self):
        print('call worker%d'%self.worker_id )
        # rospy.Subscriber(self.topic, Task, self.callback_func)
        
        print(f'worker {self.worker_id} done')
        rospy.spin()
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.txt'%self.worker_id,'w') as file:
                for ele in self.worker_task :
                    file.write(f"{ele}\n\n")