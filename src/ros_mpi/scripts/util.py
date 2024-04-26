
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
class UAV:
    def __init__(self,uav_id,master_id,iter,alltasks=[]) -> None:
        self.pub_suc_topic = '/uav1/tasks'
        self.uavId = uav_id
        self.masterId = master_id
        self.alltasks = alltasks
        self.taskqueue=[]
        self.taskqueueLocal=[]
        self.iteration=iter
        rospy.init_node('uav%d'%self.uavId, anonymous=True)
        self.pub = rospy.Publisher(self.pub_suc_topic,Task,queue_size=10)
        # print(f'constructed uav {self.uavId} received task {self.alltasks}')
        print(f'constructed uav {self.uavId}')
        # print(f'current master is {self.masterId}')
        # self.rate = rospy.Rate(1) # 10hz
    def sub_callback(self,data):
        print(f'currrent task id {data.task_idx} on {data.processor_id+1} current uav {self.uavId}')
        # if data not in self.taskqueue:
        if data.processor_id +1 == self.uavId and data not in self.taskqueue:
            self.taskqueue.append(data)
        # with open('/home/jxie/rossim/src/ros_mpi/task_succ/tasks_REC%d_iter_%d.pkl'%(self.uavId,self.iteration),'wb') as file:
        #     pickle.dump(self.taskqueue,file)
    def thread_callback(self):
        print('\nthread call back subscriber')
        rospy.Subscriber(self.pub_suc_topic,Task,self.sub_callback)
        # with open('/home/jxie/rossim/src/ros_mpi/task_succ/tasks%d_iter_%d.pkl'%(self.uavId,self.iteration),'wb') as file:
        #     pickle.dump(self.taskqueue,file)
        rospy.spin()
        # print(f'current uav-{self.uavId} finished......')

    def run(self):
        print(f'call the run method......')
        thread = threading.Thread(target=self.thread_callback)
        # thread_pub = threading.Thread(target=self.thread_pub)
        thread.start()
        # thread_pub.start()
        if self.alltasks:
            for i in self.alltasks:
                self.pub.publish(i)
                print(f'task {i.task_idx} is on {i.processor_id}')
                if (i.processor_id +1)== self.uavId:
                    self.taskqueueLocal.append(i)
                rospy.sleep(0.25)
            print(f'finished publish all tasks..')
        else:
            print(f'current uav {len(self.alltasks)} is empty')
        with open('/home/jxie/rossim/src/ros_mpi/task_succ/tasks_local_REC%d_iter_%d.pkl'%(self.uavId,self.iteration),'wb') as file:
            pickle.dump(self.taskqueueLocal,file)
        with open('/home/jxie/rossim/src/ros_mpi/task_succ/tasks_REC%d_iter_%d.pkl'%(self.uavId,self.iteration),'wb') as file:
            pickle.dump(self.taskqueue,file)








#################################################################################




class Node:
    def __init__(self,node_id,nodeVerify,allTasks,cpu,iteration,taskqueue,energy=50) -> None:
        print(f'constructing master node UAV on {node_id}')
        self.datarate = Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))
        print(self.datarate)
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
        # testorchest.indep_sch(taskgenerator.gen_indep())
        tempTask = taskgenerator.gen_indep()
        print('generating tasks')
        self.allTasks = self.testorchest.indep_sch(tempTask)
        # for i in self.allTasks:
        #     print(f'task {i.task_idx} on processor {i.processor_id}')
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
        rospy.init_node(self.nodeVerify, anonymous=True)
        self.pub = rospy.Publisher(self.pubTopic,Task,queue_size=10)
        self.rate = rospy.Rate(1) # 10hz
        # while True:
        #     if rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%self.node_id, PoseStamped).pose.position.z + 0.1 > 0:
        #         break
            # else:
            #     print(f'master {self.node_id} not on position')
        print(f'Master construction completed node id {self.node_id}')
    def comm_time(self,u1,u2):
            # print(f'uav {u1} and uav {u2}')
            pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
            pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
            distance = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                                [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])

            return self.datarate .data_rate(distance)
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

    def run(self):
        task_status_flag = [False]*len(self.comm)
        # temp_task = defaultdict(list)
        # while incomplete_task and task_status_flag:
        print('****'*20)
        timeslot =0
        print(f'comm matrix {self.comm}')
        while True:
            incomplete_task =np.argsort([self.testorchest.calculate_rank_up_recursive(self.comp,self.comm,i) for i in range(len(self.comp))]).tolist()[::-1]
            # print(f'incomplete_task{incomplete_task}')
            #call dynamic heft             
            # print(f'currrent time slot {timeslot}')
            self.testorchest.dy_heft(incomplete_task,timeslot)
            self.testorchest.update_comm(0.1)
            # self.testorchest.update_comm(np.mean([self.comm_time(self.node_id,u) for u in range(2,self.numberOfComputingNode+1)]))
            # for u in range(2,self.numberOfComputingNode+1):
            #     print(f'data rate between {self.node_id} and worker {u} is {self.comm_time(self.node_id,u)}')
            # temp_task = [x for x in incomplete_task if testobj.task_flag[x]]
            # print(f'at line 344 { testobj.task_flag}')
            
            timeslot += 1
            # print(f'complete list: {complete_list}')
            # for i in complete_list:
            #     task_status_flag[i] = True
            print(f'self.testorchest.get_items() {self.testorchest.get_items()}')
            for x in self.testorchest.get_items():
                if self.testorchest.task_flag[x]:
                    print(f'current task {x} is already scheduled {self.testorchest.task_flag[x]}')
                    continue
                if self.testorchest.tasks[x].processor_id == self.node_id - 1:
                    self.taskQueue.append(x)
                    self.completed.append([self.testorchest.tasks[x].task_idx,rospy.get_time()])
                    rospy.sleep(self.testorchest.tasks[x].size / self.testorchest.tasks[x].ci)
                else:
                    self.pub.publish(self.testorchest.tasks[x])
                    rospy.sleep(0.25)
            print(f'task flag {self.testorchest.task_flag}')
            if not False in self.testorchest.task_flag:
                print(f'task scheduling {self.testorchest.task_schedule_list}')
                print(f'ast {self.testorchest.AST}')
                print(f'aft {self.testorchest.AFT}')
                break
        print('finished')
        print('*'*20)


    # def run(self):

    #     for t in self.allTasks:
    #         self.fly_energy.append([self.energy * (t.size / t.ci),t.task_idx])
    #         if t.processor_id == self.node_id -1:
    #             t.st = self.taskQueue [-1].et if self.taskQueue else 0
    #             t.et = t.st + float(t.size / t.ci) 
    #             self.taskQueue.append(t)
    #             self.capc_usage(t)
    #             self.comp_energy.append([t.delta * (t.size/t.ci),t.task_idx])
    #             self.comp_time.append([(t.size/t.ci),t.task_idx])
    #             self.completed.append([t.task_idx,rospy.get_time()])
    #             rospy.sleep(t.size/t.ci)
                
    #         else: 
    #             if self.range(self.node_id,t.processor_id+1) > 200:
    #                 self.incompleted.append([t.task_idx,rospy.get_time()])
    #                 print('Disconnected......')
    #                 continue
    #             else:
    #                 print(f'publish task {t.task_idx} to worker {t.processor_id}')
    #                 temp = self.comm_time(self.node_id,t.processor_id+1) if t.processor_id+1 > 0 else 1
    #                 self.comm_energy.append([(t.size / temp)*self.energy,t.task_idx])
    #                 self.communication_time.append(t.size / temp)
    #                 print(f'energy cost at line 70 {self.comm_energy}')
    #                 self.completed.append([t.task_idx,rospy.get_time()])
    #                 self.pub.publish(t)
    #                 rospy.sleep(0.25) 
        #task on master
        # print(f'all tasks on master node {len(self.taskQueue)}')
        # print(f'total task {len(self.completed) + len(self.incompleted)}')
        # print(f'uav capacity usage {len(self.capacity)}')
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.taskQueue,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_time_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.communication_time,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_energy_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.comm_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_energy_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.comp_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_fly_energy_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.fly_energy,file)
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_time_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.comp_time,file)
        with open('/home/jxie/rossim/src/ros_mpi/task_succ/completed_%d_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.completed,file)
        with open('/home/jxie/rossim/src/ros_mpi/task_succ/incompleted_%d_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.incompleted,file)
        with open('/home/jxie/rossim/src/ros_mpi/task_succ/capacity%d_iter_%d.pkl'%(self.node_id,self.iteration),'wb') as file:
            pickle.dump(self.capacity,file)

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
            self.communication_time=[]
            self.comp_energy = []
            self.fly_energy = []
            self.comp_time = []
            self.datarate = Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))

            print(f'constructing worker node on {self.node_id}')
            rospy.init_node(self.nodeVerify, anonymous=True)
            while True:
                if rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%self.node_id, PoseStamped).pose.position.z + 0.1 > 0:
                    break
                # else:
                #     print(f'worker {self.node_id} not on position')
            rospy.Subscriber(self.pubTopic, Task, self.sub_callback)
        def comm_time(self,u1,u2):
            # print(f'uav {u1} and uav {u2}')
            pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
            pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
            distance = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                                [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
            return self.datarate.data_rate(distance)
        def sub_callback(self,data):
            self.fly_energy.append([self.energy * (data.size / data.ci),data.task_idx])

            self.comm_energy.append([(data.size / self.comm_time(2,self.node_id))*self.energy,data.task_idx])
            self.communication_time.append(data.size / self.comm_time(2,self.node_id))
            
            if data.processor_id == self.node_id -1 :
                print(f'task {data.task_idx} on worker { self.node_id}')
                data.st = self.taskQueue [-1].et if self.taskQueue else 0
                data.et = data.st + float(data.size / data.ci) 
                if data not in self.taskQueue:self.taskQueue.append(data) 
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
            with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_time.pkl'%self.node_id,'wb') as file:
                pickle.dump(self.communication_time,file)
            print('saved')

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
                trans_time = 0.1
                x.st = max(self.master_task[-1].et, self.pred_aft(x)+trans_time) if self.master_task else self.pred_aft(x)+trans_time
                x.et = x.st + self.comp[x.task_idx][x.processor_id]
                self.comp_energy.append([x.delta * (x.size/x.ci),x.task_idx])
                self.comp_time.append([self.comp[x.task_idx][x.processor_id],x.task_idx]) #computatin time
                self.master_task.append(x)
            else:
                #plus communication time
                temp = self.comm_time(self.nodeid,x.processor_id+1)
                x.st = self.pred_aft(x) + 0.1
                print(f'at line  483 current task {x.task_idx} st {x.st}')
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
        # while True: 
        #     if rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%self.worker_id, PoseStamped).pose.position.z + 0.1 > 0:
        #         break
        # rospy.Subscriber(self.topic, Task, self.callback_func)

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
