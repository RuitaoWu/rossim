
from concurrent.futures import thread
import pickle

import time,math
from turtle import pos
from collections import defaultdict
from networkx import node_attribute_xy
from numpy import save

from torch import _euclidean_dist
from hector_uav_msgs.msg import Task, FinishTime
from orchestrator import Orchestrator
from datarate import Datarate
import rospy,threading
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32MultiArray
from dataplot import PlotGraph


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
    def __init__(self,node_id,cpu,sleepTime,energy=50) -> None:
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
        self.energy = energy
        self.comm_energy = []
        self.comp_energy = []
        self.fly_energy = []
        self.comp_time = []
        self.nodeid = node_id
        print(f'at time {rospy.get_time()} created master node with energy {self.energy} mW')
    #locate sucessor location
    def locate_pred(self,t):
        temp =[0]
        processor = [0]
        for pre in t.dependency:
            for x in self.task_received :
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
                    processor.append(x.processor_id )
        print(f'at line 142 max finished time process location for task {t.task_idx} is {processor[temp.index(max(temp))]}')
        return processor[temp.index(max(temp))]

    #
    def pred_aft(self,t):
        temp =[0]
        for pre in t.dependency:
            for x in self.task_received :
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
        print(f'at line 152 max finished time for task {t.task_idx} is {temp}')
        return max(temp)
    
    def sub_callback(self,data):
        if data:
            self.task_received.append(data)
            temp = self.comm_time(1,data.processor_id+1) if data.processor_id+1 > 0 else 1
            self.comm_energy.append([(data.size / temp)*self.energy,data.task_idx]) 
            print(f'at line 139 received task {self.comm_energy[-1]}')
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
        print(f'current master location {(pos.pose.position.x,pos.pose.position.y,pos.pose.position.z)}')
    def comm_time(self,u1,u2):
        print(f'uav {u1} and uav {u2}')
        pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
        pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
        distance = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                             [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
        dr = Datarate()
        return dr.data_rate(dr.channel_gain(distance))
    def run(self,dt):
        self.energy -= 1
        print(f'at line 160 self energy remain: {self.energy}')
        print(f'publishing...')
        thread = threading.Thread(target= self.received_call_back)
        thread.start()

        # rospy.Subscriber(self.worker_to_uav,Task,self.sub_callback)
        for x in dt:           
            self.fly_energy.append([self.energy * (x.size / self.cpu),x.task_idx])
            if x.processor_id == 0:
                location_predecessor = self.locate_pred(x)
                trans_time = x.size / self.comm_time(self.nodeid,location_predecessor+1) if location_predecessor != 0 else 0
                print(f'at line 194 current trans_time {trans_time} for task {x.task_idx}')
                x.st = max(self.master_task[-1].et, self.pred_aft(x)+trans_time) if self.master_task else self.pred_aft(x)+trans_time
                print(f'current task {x.task_idx} start {x.st}')
                x.et = x.st + (x.size/x.ci)
                self.comp_energy.append([x.delta * (x.size/x.ci),x.task_idx])
                self.comp_time.append([(x.size/x.ci),x.task_idx])
                self.master_task.append(x)
            else:
                #plus communication time
                temp = self.comm_time(1,x.processor_id+1) if x.processor_id+1 > 0 else 1
                x.st = self.pred_aft(x) + (x.size / temp)
                self.comm_energy.append([(x.size / temp)*self.energy,x.task_idx]) #units: mj
            # print(f'at line 192 publishing task {x.task_idx} with start time {x.st} and end time {x.et}')
            self.pub.publish(x)

            rospy.sleep(self.sleepTime)  
        
        #all tasks
        # with open('/home/jxie/rossim/src/ros_mpi/data/task_ast_master.pkl','w') as file:
            # for ele in self.task_received :
            #     file.write(f"{ele}\n\n")
        print(f'master comm energy {self.comm_energy}')
        print(f'master comp energy {self.comp_energy}')
        print(f'master comp time {self.comp_time}')
        print(f'master fly energy {self.fly_energy}')
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1.pkl','wb') as file:
            pickle.dump(self.master_task,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1_comm_energy.pkl','wb') as file:
            pickle.dump(self.comm_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1_comp_energy.pkl','wb') as file:
            pickle.dump(self.comp_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1_fly_energy.pkl','wb') as file:
            pickle.dump(self.fly_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1_comp_time.pkl','wb') as file:
            pickle.dump(self.comp_time,file)
        # savegraph = PlotGraph(self.nodeid)
        # savegraph.run()
        # task on master
        # with open('/home/jxie/rossim/src/ros_mpi/data/uav1.txt','w') as file:
        #     for ele in self.master_task :
        #         file.write(f"{ele}\n\n")
        





class Worker:
    def __init__(self,worker_id,cpu,sleepTime,energy = 50) -> None:
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
        self.energy = energy
        self.comm_energy = []
        self.comp_energy = []
        self.fly_energy = []
        self.comp_time = []
        rospy.Subscriber(self.topic, Task, self.callback_func)
    def pred_aft(self,t):
        temp =[0]
        for pre in t.dependency:
            for x in self.all_task:
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
        # print(f'at line 232 the temp time list for task {t.task_idx} is {temp}')
        return max(temp)

        #sub location information
    # def location_thread(self):
    #     pos = rospy.wait_for_message(self.loc, PoseStamped)
    #     print(f'current worker location : ({pos.pose.position.x},{pos.pose.position.y}self.energy)')
    def callback_func(self,data):
        # loc_worker = '/uav%d/ground_truth_to_tf/pose'%data.processor_id +1
        # print('/uav%d/ground_truth_to_tf/pose'%(data.processor_id+1))
        print(f'at line 276 {data.task_idx}')
        self.fly_energy.append([self.energy * (data.size / self.cpu),data.task_idx])
        worker_1 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%(data.processor_id+1),PoseStamped)
        worker_2 = rospy.wait_for_message(self.loc,PoseStamped)
        # print([[worker_1.pose.position.x,worker_1.pose.position.y,worker_1.pose.position.z],
        #                      [worker_2.pose.position.x,worker_2.pose.position.y,worker_2.pose.position.z]])
        distance = math.dist([worker_1.pose.position.x,worker_1.pose.position.y,worker_1.pose.position.z],
                             [worker_2.pose.position.x,worker_2.pose.position.y,worker_2.pose.position.z])
        
        test = Datarate()
        current_datarate = test.data_rate(test.channel_gain(distance))

        self.comm_energy.append([(data.size / current_datarate) * self.energy,data.task_idx]) #units: mj
        self.all_task.append(data)
        print(f'at line 288 datarate between {self.worker_id} and  {data.processor_id+1} is {current_datarate} and the comm time is {(data.size / current_datarate) }')
        if data.processor_id == self.worker_id - 1 :
            data.st = max(self.worker_task[-1].et, self.pred_aft(data),data.st) if self.worker_task else max(self.pred_aft(data),data.st)
            data.et = data.st +(data.size / data.ci)
            self.comp_energy.append([data.delta *(data.size/data.ci),data.task_idx]) #units: mj
            self.comp_time.append([(data.size / data.ci),data.task_idx] )
            self.pub.publish(data)
            rospy.sleep(self.sleepTime)
            self.worker_task.append(data)
        else:
            print('empty')

    def sub_thread(self):
        rospy.Subscriber(self.topic, Task, self.callback_func)
    def run(self):
        print('call worker%d'%self.worker_id )
        # rospy.Subscriber(self.topic, Task, self.callback_func)
        
        print(f'worker {self.worker_id} done')
        rospy.spin()
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.pkl'%self.worker_id,'wb') as file:
            pickle.dump(self.worker_task,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_energy.pkl'%self.worker_id,'wb') as file:
            pickle.dump(self.comm_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_energy.pkl'%self.worker_id,'wb') as file:
            pickle.dump(self.comp_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_fly_energy.pkl'%self.worker_id,'wb') as file:
            pickle.dump(self.fly_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_time.pkl'%self.worker_id,'wb') as file:
            pickle.dump(self.comp_time,file)
        if rospy.is_shutdown():
            print(f'node {self.worker_id} shutdown')
            savegraph = PlotGraph(self.worker_id)
            savegraph.run()
        # with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.txt'%self.worker_id,'w') as file:
        #         for ele in self.worker_task :
        #             file.write(f"{ele}\n\n")