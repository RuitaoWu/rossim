
from concurrent.futures import thread
import pickle
import random
import numpy as np
# from re import T
import time,math
# from traceback import print_tb
# from turtle import pos
from collections import defaultdict
# from cupshelpers import Printer
# from networkx import node_attribute_xy
from numpy import save

# from torch import _euclidean_dist
from hector_uav_msgs.msg import Task
from orchestrator import Orchestrator
from datarate import Datarate
import rospy,threading
from geometry_msgs.msg import PoseStamped
# from std_msgs.msg import Float32MultiArray
from dataplot import PlotGraph
import configparser
from orchestrator import Orchestrator
from taskgen import TaskGen
config = configparser.ConfigParser()
config.read('property.properties')

#################################################################################
#indepedent
#dy heft
#################################################################################

class Node:
    def __init__(self,node_id,nodeVerify,allTasks,cpu,iteration,taskqueue,energy=50) -> None:
        print(f'constructing master node UAV on {node_id}')
        self.datarate = Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))
        # print(self.datarate)
        numberOfTask = int(config.get('Task','numberOfTask'))
        self.numberOfComputingNode = int(config.get('Task','computing'))
        task_size_min = int(config.get('Task','task_size_min'))
        task_size_max = int(config.get('Task','task_size_max'))
        ipsMax = int(config.get('Task','ips_max'))
        ipsMin = int(config.get('Task','ips_min'))
        taskgenerator = TaskGen(random.randint(numberOfTask // 2, numberOfTask),self.numberOfComputingNode,task_size_min,task_size_max,ipsMin,ipsMax)
        # self.comp,self.comm = taskgenerator.gen_comp_matrix(),taskgenerator.generate_random_dag(density=0.5)
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
        self.comp,self.comm = comp,comm
        self.testorchest = Orchestrator(self.comm,self.comp,100,200)
        self.uav_capa = 1000000
        self.node_id = node_id
        self.taskQueue = taskqueue
        self.capacity,self.temp_capa = [],[]
        self.nodeVerify = nodeVerify
        self.pubTopic = 'pub/task'
        self.recTopic = 'rec/task'
        self.incompleted,self.completed =[],[]
        self.cpu = cpu
        self.iteration = iteration
        self.energy = energy
        self.comm_energy = []
        self.communication_time = []
        self.comp_energy = []
        self.fly_energy = []
        self.comp_time = []
        self.task_received=[]
        rospy.init_node(self.nodeVerify, anonymous=True)
        self.pub = rospy.Publisher(self.pubTopic,Task,queue_size=10)
        self.rate = rospy.Rate(1) # 10hz
        # while True:
        #     if rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%self.node_id, PoseStamped).pose.position.z + 0.1 > 0:
        #         break
            # else:
            #     print(f'master {self.node_id} not on position')
        print(f'Master construction completed node id {self.node_id}')
    
     #find the predecessor of current task
    def predecessor_task(self,task):
        """
        The function `predecessor_task` takes a task as input and returns a list of its predecessor tasks.
        
        :param task: The parameter "task" represents the index of a task in a list or array
        :return: a list of predecessor tasks for the given task.
        """

        pre_decessor = []
        for i in range(0, len(self.comm)):
            if self.comm[i][task] > 0:
                pre_decessor.append(i)
        return pre_decessor

    
    def comm_time(self,u1,u2):
            # print(f'uav {u1} and uav {u2}')
            # pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
            # pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
            # distance = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
            #                     [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])

            return self.datarate .data_rate(400)
    def range(self,u1,u2):
        try:
            pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
            pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
            return math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                                [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
        except:
            return float('inf')

    def capc_usage(self,t):
        self.temp_capa.append(t.size)
        while sum(self.temp_capa) > self.uav_capa:
            self.temp_capa.pop(0)
        self.capacity.append(sum(self.temp_capa))
    #locate sucessor location
    def locate_pred(self,t):
        temp =[0]
        processor = [0]
        for pre in t.dependency:
            for x in self.task_received:
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
                    processor.append(x.processor_id )
        return processor[temp.index(max(temp))]

    #predecessor actual finish time
    def pred_aft(self,t):
        temp =[0]
        # print(f'dependency {t.dependency}')
        for pre in t.dependency:
            for x in self.task_received :
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
        # print(f'at line 157 task id {t.task_idx} and temp {temp}')
        return max(temp)
    
    def sub_callback(self,data):
        # print(f'receive tasks......')
        id_list = [x.task_idx for x in self.task_received]
        #update task time after received back from worker
        if data.task_idx not in id_list:            
            self.task_received.append(data)
        else:
            print(f'at line 163 task index {self.task_received[self.task_received.index(data)].st}\
                 {self.task_received[self.task_received.index(data)].et}')

            # temp = self.comm_time(self.node_id,data.processor_id+1) if data.processor_id+1 > 0 else 1
            # self.comm_energy.append([(data.size / temp)*self.energy,data.task_idx]) 
            # self.communication_time_rec.append([data.size / temp,data.task_idx])

    def received_call_back(self):
        print('call receive threading...')
        rospy.Subscriber(self.recTopic,Task,self.sub_callback)
    
    
    def run(self):
        thread = threading.Thread(target= self.received_call_back)
        thread.start()
        print('****'*20)
        timeslot =60
        print(f'comm matrix {self.comm}')
        rospy.sleep(0.25)
        while True:
            incomplete_task =np.argsort([self.testorchest.calculate_rank_up_recursive(self.comp,self.comm,i) for i in range(len(self.comp))]).tolist()[::-1]
            self.testorchest.dy_heft(incomplete_task,timeslot)
            self.testorchest.update_comm(self.comm_time(0,0))
            
            timeslot += 5
            # print(f'self.testorchest.get_items(): {self.testorchest.get_items()[::-1]}')
            for x in self.testorchest.get_items()[::-1]:
                if self.testorchest.task_flag[x]:
                    # print(f'at line 187 {self.testorchest.task_flag[x]}')
                    if self.testorchest.tasks[x].processor_id == self.node_id - 1:
                        # if self.testorchest.tasks[x].task_idx not in [x.task_idx for x in self.taskQueue]:
                        trans_time = 100000
                        if self.taskQueue:
                            self.testorchest.tasks[x].st=max(self.taskQueue[-1].et, self.pred_aft(self.testorchest.tasks[x])+(self.testorchest.tasks[x].size / trans_time)) 
                            self.testorchest.tasks[x].et = self.testorchest.tasks[x].st+self.comp[self.testorchest.tasks[x].task_idx][self.testorchest.tasks[x].processor_id ]
                        else:
                            self.testorchest.tasks[x].st=self.pred_aft(self.testorchest.tasks[x])+(self.testorchest.tasks[x].size/ trans_time)
                            self.testorchest.tasks[x].et=self.testorchest.tasks[x].st+self.comp[self.testorchest.tasks[x].task_idx][self.testorchest.tasks[x].processor_id ]
                        # print(f'at line 223 self.testorchest.tasks[x].et: {self.testorchest.tasks[x].et}')
                        self.taskQueue.append(self.testorchest.tasks[x])
                        self.completed.append([self.testorchest.tasks[x].task_idx,rospy.get_time()])
                        # rospy.sleep(0.25)
                    else:
                        self.testorchest.tasks[x].st = self.pred_aft(self.testorchest.tasks[x]) + 0.1 
                    self.pub.publish(self.testorchest.tasks[x])
                    print(f'at line 207 self.testorchest.tasks[x] {self.testorchest.tasks[x].task_idx} st {self.testorchest.tasks[x].st}and et {self.testorchest.tasks[x].et}')
                    rospy.sleep(0.25)
            if not False in self.testorchest.task_flag:
                for x in self.task_received:
                    print(f'x id {x.task_idx} with {x.st} and {x.et}')
                break
        print('finished')
        print('*'*20)

        with open('../data/uav%d.pkl'%(self.node_id),'wb') as file:
            pickle.dump(self.taskQueue,file)
        with open('../data/uav%d_comm_time_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.communication_time,file)
        with open('../data/uav%d_comm_energy_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.comm_energy,file)
        with open('../data/uav%d_comp_energy_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.comp_energy,file)
        with open('../data/uav%d_fly_energy_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.fly_energy,file)
        with open('../data/uav%d_comp_time_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.comp_time,file)
        with open('../task_succ/completed_%d_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.completed,file)
        with open('../task_succ/incompleted_%d_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.incompleted,file)
        with open('../task_succ/capacity%d_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.capacity,file)

class WorkerNode:
        def __init__(self,node_id,nodeVerify,cpu,iteration,taskqueue,energy=50) -> None:
            self.node_id = node_id
            self.taskQueue = taskqueue
            self.nodeVerify = nodeVerify
            self.pubTopic = 'pub/task'
            self.recTopic = 'rec/task'
            self.workerpub = rospy.Publisher(self.recTopic,Task,queue_size=20)
            self.loc = '/uav%d/ground_truth_to_tf/pose'%self.node_id
            self.cpu = cpu
            self.iteration = iteration
            self.energy = energy
            self.comm_energy = []
            self.communication_time=[]
            self.comp_energy = []
            self.fly_energy = []
            self.comp_time = []
            self.allTask=[]
            self.datarate = Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))

            print(f'constructing worker node on {self.node_id}')
            self.comp = [[14,16,9],
                    [13,19,18],
                    [11,13,19],
                    [13,8,17],
                    [12,13,10],
                    [13,16,9],
                    [7,15,11],
                    [5,11,4],
                    [18,12,20],
                    [21,7,16]]

            self.comm = [[0,18,12,9,11,14,0,0,0,0],
                        [0,0,0,0,0,0,0,19,16,0],
                        [0,0,0,0,0,0,23,0,0,0],
                        [0,0,0,0,0,0,0,27,23,0],
                        [0,0,0,0,0,0,0,0,13,0],
                        [0,0,0,0,0,0,0,15,0,0],
                        [0,0,0,0,0,0,0,0,0,17],
                        [0,0,0,0,0,0,0,0,0,11],
                        [0,0,0,0,0,0,0,0,0,13],
                        [0,0,0,0,0,0,0,0,0,0]]
            rospy.init_node(self.nodeVerify, anonymous=True)
            rospy.Subscriber(self.pubTopic, Task, self.sub_callback)
        #predecessor actual finish time
        def pred_aft(self,t):
            temp =[-1]

            for pre in t.dependency:
                for x in self.allTask :
                    if pre == x.task_idx and x.processor_id != t.processor_id:
                        # print(f'at line 285 the et time is {x.et}')
                        temp.append(x.et)
            # print(f'at line 289 task id {t.task_idx} with temp {temp} ')
            return max(temp)
        def comm_time(self,u1,u2):
            # print(f'uav {u1} and uav {u2}')
            # pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
            # pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
            # distance = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
            #                     [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
            return self.datarate.data_rate(400)
        def sub_callback(self,data):
            self.fly_energy.append([self.energy * (data.size / data.ci),data.task_idx])
            self.comm_energy.append([(data.size / self.comm_time(2,self.node_id))*self.energy,data.task_idx])
            self.communication_time.append(data.size / self.comm_time(2,self.node_id))
            self.allTask.append(data)
            if data.processor_id == self.node_id -1 :
                if data.task_idx not in self.taskQueue:
                    if self.taskQueue:
                        data.st = max(self.taskQueue [-1].et, self.pred_aft(data)+(data.size / 100000))
                        data.et = data.st + self.comp[data.task_idx][data.processor_id]
                    else:
                        data.st = self.pred_aft(data)+(data.size / 100000)
                        data.et = data.st + self.comp[data.task_idx][data.processor_id]
                    self.comp_energy.append([data.delta * (data.size/data.ci),data.task_idx])
                    self.comp_time.append([(data.size/data.ci),data.task_idx])
                    self.taskQueue.append(data) 
            self.workerpub.publish(data)
            rospy.sleep(0.25)

        def run(self):
            print('call worker%d'%self.node_id )
            
            rospy.spin()
            print(f'saveing task queue to file..')
            print(f'at line 325 task queue {len(self.taskQueue)}')
            with open('../data/uav%d.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.taskQueue,file)
            with open('../data/uav%d_comm_energy.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.comm_energy,file)
            with open('../data/uav%d_comp_energy.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.comp_energy,file)
            with open('../data/uav%d_fly_energy.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.fly_energy,file)
            with open('../data/uav%d_comp_time.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.comp_time,file)
            with open('../data/uav%d_comm_time.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.communication_time,file)
            print('saved')
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
####                                     dependent task                                           ####
####                                                                                              ####
####                                                                                              ####
######################################################################################################
class Master:
    def __init__(self,node_id,cpu,sleepTime,energy=0.05) -> None:
        print('construcing master node on ',node_id)
        self.topic = '/uav%d/task'%node_id
        self.loc = '/uav%d/ground_truth_to_tf/pose'%node_id
        self.worker_to_uav = '/worker/task'
        rospy.init_node('uav%d'%(node_id), anonymous=True)
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
        config.read('property.properties')
        self.comm_range = float(config.get('UAV','comm_range'))
        # noise=0.0000000000001,band_width=5000000 , transmission_power=0.5,alpha=4.0
        # density = float(config.get('Task','density'))
        self.datarate = Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))
        self.comp = [[14,16,9],
                    [13,19,18],
                    [11,13,19],
                    [13,8,17],
                    [12,13,10],
                    [13,16,9],
                    [7,15,11],
                    [5,11,4],
                    [18,12,20],
                    [21,7,16]]

        self.comm = [[0,18,12,9,11,14,0,0,0,0],
                    [0,0,0,0,0,0,0,19,16,0],
                    [0,0,0,0,0,0,23,0,0,0],
                    [0,0,0,0,0,0,0,27,23,0],
                    [0,0,0,0,0,0,0,0,13,0],
                    [0,0,0,0,0,0,0,15,0,0],
                    [0,0,0,0,0,0,0,0,0,17],
                    [0,0,0,0,0,0,0,0,0,11],
                    [0,0,0,0,0,0,0,0,0,13],
                    [0,0,0,0,0,0,0,0,0,0]]
        # while True:
        #     if rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%self.nodeid, PoseStamped).pose.position.z + 0.1 > 0:
        #         break
        print('master node is on position...')
    #locate sucessor location
    def locate_pred(self,t):
        temp =[0]
        processor = [0]
        for pre in t.dependency:
            for x in self.task_received:
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
                    processor.append(x.processor_id )
        return processor[temp.index(max(temp))]



    #predecessor actual finish time
    def pred_aft(self,t):
        temp =[]
        print(f'dependency {t.dependency}')
        for pre in t.dependency:
            for x in self.task_received :
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
        return max(temp) if temp else 0
    
    def sub_callback(self,data):
        if data not in self.task_received:
            self.task_received.append(data)
            temp = self.comm_time(self.nodeid,data.processor_id+1) if data.processor_id+1 > 0 else 1
            self.comm_energy.append([(data.size / temp)*self.energy,data.task_idx]) 
            self.communication_time_rec.append([data.size / temp,data.task_idx])

    def received_call_back(self):
        print('call receive threading...')
        rospy.Subscriber(self.worker_to_uav,Task,self.sub_callback)
        
    def comm_time(self,u1,u2):
        # print(f'uav {u1} and uav {u2}')
        # pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
        # pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
        # d = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
        #                      [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
        # dr = Datarate()
        # return self.datarate.data_rate(d)
        return self.datarate.data_rate(400)
    def distance_between_nodes(self,u1,u2):
        pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
        pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
        return math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                             [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
    def run(self,dt):
        print(f'publishing...')
        thread = threading.Thread(target= self.received_call_back)
        thread.start()
        self.pub.publish(Task())
        rospy.sleep(self.sleepTime) 
        for x in dt:
            self.fly_energy.append([self.energy * (x.size / self.cpu),x.task_idx])
            if x.processor_id == 0:
                trans_time = self.comm_time(0,0)
                print(f'data rate {x.size / trans_time}')
                x.st = max(self.master_task[-1].et, self.pred_aft(x)+(x.size / trans_time)) if self.master_task else self.pred_aft(x)+(x.size / trans_time)
                x.et = x.st + self.comp[x.task_idx][x.processor_id]
                print(f'at line  431 current task {x.task_idx} st {x.st} with comp {self.comp[x.task_idx][x.processor_id]}')
                self.comp_energy.append([x.delta * (x.size/x.ci),x.task_idx])
                self.comp_time.append([self.comp[x.task_idx][x.processor_id],x.task_idx]) #computatin time
                self.master_task.append(x)
            else:
                #plus communication time
                # temp = self.comm_time(self.nodeid,x.processor_id+1)
                temp = self.comm_time(self.nodeid,x.processor_id+1)
                x.st = self.pred_aft(x) + (x.size / temp)              
                self.communication_time_offload.append([x.size / temp,x.task_idx])
                self.comm_energy.append([(x.size / temp)*self.energy,x.task_idx]) #units: mj
                # rospy.sleep(x.size/x.ci) #simulate computation time
            self.pub.publish(x)
            rospy.sleep(self.sleepTime) #communication delay

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
        rospy.init_node('uav%d'%self.worker_id , anonymous=True)
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
        self.comp = [[14,16,9],
                    [13,19,18],
                    [11,13,19],
                    [13,8,17],
                    [12,13,10],
                    [13,16,9],
                    [7,15,11],
                    [5,11,4],
                    [18,12,20],
                    [21,7,16]]

        self.comm = [[0,18,12,9,11,14,0,0,0,0],
                    [0,0,0,0,0,0,0,19,16,0],
                    [0,0,0,0,0,0,23,0,0,0],
                    [0,0,0,0,0,0,0,27,23,0],
                    [0,0,0,0,0,0,0,0,13,0],
                    [0,0,0,0,0,0,0,15,0,0],
                    [0,0,0,0,0,0,0,0,0,17],
                    [0,0,0,0,0,0,0,0,0,11],
                    [0,0,0,0,0,0,0,0,0,13],
                    [0,0,0,0,0,0,0,0,0,0]]

    def pred_aft(self,t):
        temp =[0]
        # print(f'at line 580 {t.dependency}')
        for pre in t.dependency:
            for x in self.all_task:
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
        return max(temp)
    def callback_func(self,data):

        self.fly_energy.append([self.energy * (data.size / self.cpu),data.task_idx])
        self.all_task.append(data)
        if data.processor_id == self.worker_id - 1 :
            # print('/uav%d/ground_truth_to_tf/pose'%(data.processor_id+1))
            # worker_1 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%(data.processor_id+1),PoseStamped)
            # worker_2 = rospy.wait_for_message(self.loc,PoseStamped)
 
            # distance = math.dist([worker_1.pose.position.x,worker_1.pose.position.y,worker_1.pose.position.z],
            #                     [worker_2.pose.position.x,worker_2.pose.position.y,worker_2.pose.position.z])
            current_datarate = self.datarate.data_rate(400)

            data.st = max(self.worker_task[-1].et, self.pred_aft(data),data.st) if self.worker_task else max(self.pred_aft(data),data.st)
            data.et = data.st + self.comp[data.task_idx][data.processor_id] #add more computation time
            print(f'data at line 589 current worker id {self.worker_id}:  task id {data.task_idx} start timee {data.st} and end time {data.et} with comp time {self.comp[data.task_idx][data.processor_id]}')
            self.comp_energy.append([data.delta *(data.size/data.ci),data.task_idx]) #units: mj
            self.comp_time.append([self.comp[data.task_idx][data.processor_id],data.task_idx])
            self.comm_energy.append([(data.size / current_datarate) * self.energy,data.task_idx]) #units: j
            self.communication_time.append(data.size / current_datarate)
            # rospy.sleep((data.size / data.ci)) #simulate computation time
            self.worker_task.append(data)
            self.pub.publish(data)
            rospy.sleep(self.sleepTime) #communication delay
            
        else:
            print(f'length of worker tasks {len(self.worker_task)}')

    def run(self):
        print('call worker%d'%self.worker_id )
        rospy.Subscriber(self.topic, Task, self.callback_func)
        
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
        #     print(f'at line 637 tasks: {self.comp_time}')

            print(f'node {self.worker_id} shutdown')
            # savegraph = PlotGraph(self.worker_id)
            # savegraph.run()
