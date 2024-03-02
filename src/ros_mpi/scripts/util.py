
from concurrent.futures import thread
import pickle
import random

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
import configparser
from orchestrator import Orchestrator
from taskgen import TaskGen


class Node:
    def __init__(self,node_id,nodeVerify,allTasks,cpu,iteration,taskqueue,energy=50) -> None:
        config = configparser.ConfigParser()
        config.read('/home/jxie/rossim/src/ros_mpi/scripts/property.properties')

        numberOfTask = int(config.get('Task','numberOfTask'))
        numberOfComputingNode = int(config.get('Task','computing'))
        density = float(config.get('Task','density'))
        taskgenerator = TaskGen(numberOfTask,numberOfComputingNode)
        testorchest = Orchestrator([],taskgenerator.gen_comp_matrix(),100,200)
        testorchest.indep_sch(taskgenerator.gen_indep())

        self.allTasks = testorchest.indep_sch(taskgenerator.gen_indep())
        # for i in self.allTasks:
        #     print(f'task {i.task_idx} on processor {i.processor_id}')
        self.node_id = node_id
        self.taskQueue = taskqueue
        self.nodeVerify = nodeVerify
        self.pubTopic = 'pub/task'
        self.recTopic = 'rec/task'
        
        self.cpu = cpu
        self.iteration = iteration
        self.energy = energy
        self.comm_energy = []
        self.comp_energy = []
        self.fly_energy = []
        self.comp_time = []
        rospy.init_node(self.nodeVerify, anonymous=True)
        self.pub = rospy.Publisher(self.pubTopic,Task,queue_size=10)
        self.rate = rospy.Rate(1) # 10hz
        # rospy.Subscriber(self.pubTopic, Task, self.sub_callback)
        # self.pos = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose' %self.node_id, PoseStamped)
        print(f'Master construction completed node id {self.node_id}')
    def comm_time(self,u1,u2):
            print(f'uav {u1} and uav {u2}')
            pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
            pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
            distance = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                                [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
            dr = Datarate()
            return dr.data_rate(dr.channel_gain(distance))
    def run(self):
        print(f'publishing...')
        
        for t in self.allTasks:
            self.fly_energy.append([self.energy * (t.size / self.cpu),t.task_idx])
            # pos = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose' %self.node_id, PoseStamped)
            # print(f'current master {self.node_id} position {(pos.pose.position.x,pos.pose.position.y,pos.pose.position.z)}')
            if t.processor_id == self.node_id -1:
                t.st = self.taskQueue [-1].et if self.taskQueue else 0
                t.et = t.st + float(t.size / self.cpu) 
                self.taskQueue.append(t)
                self.comp_energy.append([t.delta * (t.size/t.ci),t.task_idx])
                self.comp_time.append([(t.size/t.ci),t.task_idx])
            else: 
                print(f'publish task {t.task_idx} to worker {t.processor_id}')
                temp = self.comm_time(self.node_id,t.processor_id+1) if t.processor_id+1 > 0 else 1
                
                self.comm_energy.append([(t.size / temp)*self.energy,t.task_idx])
                print(f'energy cost at line 70 {self.comm_energy}')
                self.pub.publish(t)
                rospy.sleep(1) 
        #task on master
        print(f'all tasks on master node {len(self.taskQueue)}')
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1.pkl','wb') as file:
            pickle.dump(self.taskQueue,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1_comm_energy.pkl','wb') as file:
            pickle.dump(self.comm_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1_comp_energy.pkl','wb') as file:
            pickle.dump(self.comp_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1_fly_energy.pkl','wb') as file:
            pickle.dump(self.fly_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav1_comp_time.pkl','wb') as file:
            pickle.dump(self.comp_time,file)

class WorkerNode:
        def __init__(self,node_id,nodeVerify,cpu,iteration,taskqueue,energy=50) -> None:
            self.node_id = node_id
            self.taskQueue = taskqueue
            self.nodeVerify = nodeVerify
            self.pubTopic = 'pub/task'
            self.loc = '/uav%d/ground_truth_to_tf/pose'%self.node_id
            self.cpu = cpu
            self.iteration = iteration
            self.energy = energy
            self.comm_energy = []
            self.comp_energy = []
            self.fly_energy = []
            self.comp_time = []
            rospy.init_node(self.nodeVerify, anonymous=True)
            rospy.Subscriber(self.pubTopic, Task, self.sub_callback)
            # self.pos = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose' %self.node_id, PoseStamped)
        def comm_time(self,u1,u2):
            print(f'uav {u1} and uav {u2}')
            pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
            pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
            distance = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                                [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
            dr = Datarate()
            return dr.data_rate(dr.channel_gain(distance))
        def sub_callback(self,data):
            self.fly_energy.append([self.energy * (data.size / self.cpu),data.task_idx])
            # print(f'current worker {self.node_id} location {self.pos}')
            pos = rospy.wait_for_message(self.loc,PoseStamped)
            self.comm_energy.append([(data.size / self.comm_time(2,self.node_id))*self.energy,data.task_idx])

            print(f'current worker {self.node_id} position {(pos.pose.position.x,pos.pose.position.y,pos.pose.position.z)}')
            if data.processor_id == self.node_id -1 :
                data.st = self.taskQueue [-1].et if self.taskQueue else 0
                data.et = data.st + float(data.size / self.cpu) 
                self.taskQueue.append(data)
                self.comp_energy.append([data.delta * (data.size/data.ci),data.task_idx])
                self.comp_time.append([(data.size/data.ci),data.task_idx])
            else:
                print('nothing...')

        
        def run(self):
            print('call worker%d'%self.node_id )

            
            rospy.spin()
            print(f'saveing task queue to file..')
            with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.taskQueue,file)
            with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_energy.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.comm_energy,file)
            with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_energy.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.comp_energy,file)
            with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_fly_energy.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.fly_energy,file)
            with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_time.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.comp_time,file)
            print('saved')

######################################################################################################
####                                     dependent task                                           ####
####                                                                                              ####
####                                                                                              ####
######################################################################################################
class Master:
    def __init__(self,node_id,cpu,sleepTime,energy=0.05) -> None:
        print('construcing master node')
        self.topic = '/uav%d/task'%node_id
        self.loc = '/uav%d/ground_truth_to_tf/pose'%node_id
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
        self.communication_time_offload=[]
        self.communication_time_rec=[]
        self.nodeid = node_id
        config = configparser.ConfigParser()
        config.read('/home/jxie/rossim/src/ros_mpi/scripts/property.properties')
        # noise=0.0000000000001,band_width=5000000 , transmission_power=0.5,alpha=4.0
        # density = float(config.get('Task','density'))
        self.datarate = Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))
        print(self.datarate)
        print(f'at time {rospy.get_time()} created master node with energy {self.energy} w')
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
        if data not in self.task_received:
            self.task_received.append(data)
            temp = self.comm_time(1,data.processor_id+1) if data.processor_id+1 > 0 else 1
            self.comm_energy.append([(data.size / temp)*self.energy,data.task_idx]) 
            self.communication_time_rec.append([data.size / temp,data.task_idx])
            # print(f'at line 217 current task  received {data.task_idx} from {data.processor_id+1} with communication time {self.communication_time_offload[-1]}')
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
        d = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                             [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
        # dr = Datarate()
        return self.datarate.data_rate(d)
    def run(self,dt):
        print(f'publishing...')
        thread = threading.Thread(target= self.received_call_back)
        thread.start()

        # rospy.Subscriber(self.worker_to_uav,Task,self.sub_callback)
        for x in dt:
            self.fly_energy.append([self.energy * (x.size / self.cpu),x.task_idx])
            if x.processor_id == 0:
                location_predecessor = self.locate_pred(x)
                trans_time = x.size / self.comm_time(self.nodeid,location_predecessor+1) if location_predecessor != 0 else 0
                x.st = max(self.master_task[-1].et, self.pred_aft(x)+trans_time) if self.master_task else self.pred_aft(x)+trans_time
                x.et = x.st + (x.size/x.ci)
                self.comp_energy.append([x.delta * (x.size/x.ci),x.task_idx])
                self.comp_time.append([(x.size/x.ci),x.task_idx])
                self.master_task.append(x)
            else:
                if x.processor_id > 0:
                    #plus communication time
                    print(f'current task {x.task_idx} not on master')
                    temp = self.comm_time(1,x.processor_id+1) if x.processor_id+1 > 0 else 1
                    x.st = self.pred_aft(x) + (x.size / temp)
                    self.communication_time_offload.append([x.size / temp,x.task_idx])
                    print(f'at line 261 current task {x.task_idx} not on master with communication time {self.communication_time_offload[-1]}')
                    self.comm_energy.append([(x.size / temp)*self.energy,x.task_idx]) #units: mj
            self.pub.publish(x)

            rospy.sleep(self.sleepTime)  
        print(f'at line 268 total task{len(dt)}, and {len(self.communication_time_offload),[x[1] for x in self.communication_time_offload]}')
        print(f'receied {[x.task_idx for x in self.task_received]}')
        #all tasks
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.pkl'%self.nodeid,'wb') as file:
            pickle.dump(self.master_task,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_energy.pkl'%self.nodeid,'wb') as file:
            pickle.dump(self.comm_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_energy.pkl'%self.nodeid,'wb') as file:
            pickle.dump(self.comp_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_fly_energy.pkl'%self.nodeid,'wb') as file:
            pickle.dump(self.fly_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_time.pkl'%self.nodeid,'wb') as file:
            pickle.dump(self.comp_time,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_time_offload.pkl'%self.nodeid,'wb') as file:
            pickle.dump(self.communication_time_offload,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_time_recived.pkl'%self.nodeid,'wb') as file:
            pickle.dump(self.communication_time_rec,file)
        





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
        self.communication_time=[]
        config = configparser.ConfigParser()
        config.read('/home/jxie/rossim/src/ros_mpi/scripts/property.properties')
        # noise=0.0000000000001,band_width=5000000 , transmission_power=0.5,alpha=4.0
        # density = float(config.get('Task','density'))
        self.datarate = Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))
        print(self.datarate)
        rospy.Subscriber(self.topic, Task, self.callback_func)
    def pred_aft(self,t):
        temp =[0]
        for pre in t.dependency:
            for x in self.all_task:
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
        # print(f'at line 232 the temp time list for task {t.task_idx} is {temp}')
        return max(temp)
    def callback_func(self,data):

        print(f'at line 276 {data.task_idx}')
        self.fly_energy.append([self.energy * (data.size / self.cpu),data.task_idx])
        worker_1 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%(data.processor_id+1),PoseStamped)
        worker_2 = rospy.wait_for_message(self.loc,PoseStamped)
        # print([[worker_1.pose.position.x,worker_1.pose.position.y,worker_1.pose.position.z],
        #                      [worker_2.pose.position.x,worker_2.pose.position.y,worker_2.pose.position.z]])
        distance = math.dist([worker_1.pose.position.x,worker_1.pose.position.y,worker_1.pose.position.z],
                             [worker_2.pose.position.x,worker_2.pose.position.y,worker_2.pose.position.z])
        
        # test = Datarate()
        current_datarate = self.datarate.data_rate(distance)

        
        self.all_task.append(data)
        print(f'at line 341 datarate between {self.worker_id} and  {data.processor_id+1} is {current_datarate} and the comm time is {(data.size / current_datarate) }')
        if data.processor_id == self.worker_id - 1 :
            data.st = max(self.worker_task[-1].et, self.pred_aft(data),data.st) if self.worker_task else max(self.pred_aft(data),data.st)
            data.et = data.st +(data.size / data.ci)
            self.comp_energy.append([data.delta *(data.size/data.ci),data.task_idx]) #units: mj
            self.comp_time.append([(data.size / data.ci),data.task_idx] )
            self.comm_energy.append([(data.size / current_datarate) * self.energy,data.task_idx]) #units: j
            self.communication_time.append(data.size / current_datarate)
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
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_time.pkl'%self.worker_id,'wb') as file:
            pickle.dump(self.communication_time,file)
        if rospy.is_shutdown():
            print(f'node {self.worker_id} shutdown')
            savegraph = PlotGraph(self.worker_id)
            savegraph.run()
        # with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.txt'%self.worker_id,'w') as file:
        #         for ele in self.worker_task :
        #             file.write(f"{ele}\n\n")