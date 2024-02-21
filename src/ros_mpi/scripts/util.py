
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
    def __init__(self,node_id,nodeVerify,allTasks,cpu) -> None:
        self.node_id = node_id
        self.taskQueue = []
        self.nodeVerify = nodeVerify
        self.pubTopic = 'pub/task'
        self.recTopic = 'rec/task'
        self.allTasks = allTasks
        self.cpu = cpu
        rospy.init_node(self.nodeVerify, anonymous=True)
        self.pub = rospy.Publisher(self.pubTopic,Task,queue_size=10)
        self.rate = rospy.Rate(1) # 10hz
        print(f'all tasks {self.allTasks}')
        print(f'Master construction completed node id {self.nodeVerify}')
    def run(self):
        print(f'publishing...')
        for t in self.allTasks:
            if t.processor_id == self.node_id:
                t.st = self.taskQueue [-1].et if self.taskQueue else 0
                t.et = t.st + float(t.size / self.cpu) 
                self.taskQueue.append(t)
            else: 
                print(f'publish task {t.task_idx}')
                self.pub.publish(t)
                rospy.sleep(1) 
        #task on master
        with open('/home/jxie/rossim/src/ros_mpi/data_indep/master%d.txt'%self.node_id,'w') as file:
            for ele in self.taskQueue :
                file.write(f"{ele}\n\n")
class WorkerNode:
        def __init__(self,node_id,nodeVerify,cpu) -> None:
            self.node_id = node_id
            self.taskQueue = []
            self.nodeVerify = nodeVerify
            self.pubTopic = 'pub/task'
            self.cpu = cpu
            # self.recTopic = 'rec/task'
            rospy.init_node(self.nodeVerify, anonymous=True)
            # self.pub = rospy.Publisher(self.pubTopic,Task,queue_size=10)
            # self.rate = rospy.Rate(1) # 10hz
            print(f'Worker node construction completed node id {self.nodeVerify}')
        def sub_callback(self,data):
            if data.processor_id == self.node_id:
                data.st = self.taskQueue [-1].et if self.taskQueue else 0
                data.et = data.st + float(data.size / self.cpu) 
                self.taskQueue.append(data)
                
                with open('/home/jxie/rossim/src/ros_mpi/data_indep/uav%d%s.txt'%(self.node_id,time.strftime("%Y%m%d-%H%M%S")),'w') as file:
                    for ele in self.taskQueue :
                        file.write(f"{ele}\n\n")
            else:
                print('nothing...')
        def run(self):
            print('call worker%d'%self.node_id )
            rospy.Subscriber(self.pubTopic, Task, self.sub_callback)
            rospy.spin()


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

    def run(self,dt):
        print(f'publishing...')
        thread = threading.Thread(target= self.received_call_back)
        thread.start()
        # rospy.Subscriber(self.worker_to_uav,Task,self.sub_callback)
        
        for x in dt:
            
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
    def pred_aft(self,t):
        temp =[0]
        for pre in t.dependency:
            for x in self.all_task:
                if pre == x.task_idx:
                    temp.append(x.et)
        return max(temp)

        #sub location information
    def location_thread(self):
        pos = rospy.wait_for_message(self.loc, PoseStamped)
        print(f'current worker location : ({pos.pose.position.x},{pos.pose.position.y})')
    def callback_func(self,data):
        self.all_task.append(data)
        print(f'at line 124 received task  {data.task_idx} start {data.st}')
        if data.processor_id == self.worker_id:
            data.st = max(self.worker_task[-1].et, self.pred_aft(data),data.st) if self.worker_task else max(self.pred_aft(data),data.st)
            data.et = data.st +(data.size / self.cpu)
            self.pub.publish(data)
            rospy.sleep(self.sleepTime)
            self.worker_task.append(data)
            with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.pkl'%self.worker_id,'wb') as file:
                pickle.dump(self.worker_task,file)
        else:
            print('empty')

    def sub_thread(self):
        rospy.Subscriber(self.topic, Task, self.callback_func)
    def run(self):
        print('call worker%d'%self.worker_id )
        rospy.Subscriber(self.topic, Task, self.callback_func)
        
        print(f'worker {self.worker_id} done')
        rospy.spin()