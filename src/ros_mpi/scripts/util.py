
from concurrent.futures import thread
import pickle
import random

import time,math
from traceback import print_tb
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
config = configparser.ConfigParser()
config.read('/home/jxie/rossim/src/ros_mpi/scripts/property.properties')

class Node:
    def __init__(self,node_id,nodeVerify,allTasks,cpu,iteration,taskqueue,energy=50) -> None:
        print(f'constructing master node UAV on {node_id}')
        self.datarate = Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))
        print(self.datarate)
        numberOfTask = int(config.get('Task','numberOfTask'))
        numberOfComputingNode = int(config.get('Task','computing'))
        task_size_min = int(config.get('Task','task_size_min'))
        task_size_max = int(config.get('Task','task_size_max'))
        ipsMax = int(config.get('Task','ips_max'))
        ipsMin = int(config.get('Task','ips_min'))
        taskgenerator = TaskGen(random.randint(numberOfTask // 10, numberOfTask),numberOfComputingNode,task_size_min,task_size_max,ipsMin,ipsMax)
        testorchest = Orchestrator([],taskgenerator.gen_comp_matrix(),100,200)
        # testorchest.indep_sch(taskgenerator.gen_indep())
        tempTask = taskgenerator.gen_indep()
        print('generating tasks')
        self.allTasks = testorchest.indep_sch(tempTask)
        # for i in self.allTasks:
        #     print(f'task {i.task_idx} on processor {i.processor_id}')
        self.node_id = node_id
        self.taskQueue = taskqueue
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
        while True:
            if rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%self.node_id, PoseStamped).pose.position.z + 0.1 > 0:
                break
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

            pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
            pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
            return math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                                [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])

            
    def run(self):

        for t in self.allTasks:
            self.fly_energy.append([self.energy * (t.size / t.ci),t.task_idx])
            if t.processor_id == self.node_id -1:
                t.st = self.taskQueue [-1].et if self.taskQueue else 0
                t.et = t.st + float(t.size / t.ci) 
                self.taskQueue.append(t)
                self.comp_energy.append([t.delta * (t.size/t.ci),t.task_idx])
                self.comp_time.append([(t.size/t.ci),t.task_idx])
                self.completed.append([t.task_idx,rospy.get_time()])
                rospy.sleep(t.size/t.ci)
            else: 
                if self.range(self.node_id,t.processor_id+1) > 200:
                    self.incompleted.append([t.task_idx,rospy.get_time()])
                    print('Disconnected......')
                    continue
                else:
                    print(f'publish task {t.task_idx} to worker {t.processor_id}')
                    temp = self.comm_time(self.node_id,t.processor_id+1) if t.processor_id+1 > 0 else 1
                    self.comm_energy.append([(t.size / temp)*self.energy,t.task_idx])
                    self.communication_time.append(t.size / temp)
                    print(f'energy cost at line 70 {self.comm_energy}')
                    self.completed.append([t.task_idx,rospy.get_time()])
                    self.pub.publish(t)
                    rospy.sleep(0.25) 
        #task on master
        # print(f'all tasks on master node {len(self.taskQueue)}')
        print(f'total task {len(self.completed) + len(self.incompleted)}')
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
        self.comm_range = float(config.get('UAV','comm_range'))
        # noise=0.0000000000001,band_width=5000000 , transmission_power=0.5,alpha=4.0
        # density = float(config.get('Task','density'))
        self.datarate = Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))
        while True:
            if rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%self.nodeid, PoseStamped).pose.position.z + 0.1 > 0:
                break
        print('master node is on position...')
    #locate sucessor location
    def locate_pred(self,t):
        temp =[0]
        processor = [0]
        for pre in t.dependency:
            for x in self.task_received :
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
                    processor.append(x.processor_id )
        # print(f'at line 142 max finished time process location for task {t.task_idx} is {processor[temp.index(max(temp))]}')
        return processor[temp.index(max(temp))]

    #
    def pred_aft(self,t):
        temp =[-1]
        print(f'predecessor list of task {t.task_idx} is {t.dependency} at line 237')
        for pre in t.dependency:
            for x in self.task_received :
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
        # print(f'at line 241 max finished time for task {t.task_idx} is {temp}')
        return max(temp)
    
    def sub_callback(self,data):
        if data not in self.task_received:
            self.task_received.append(data)
            temp = self.comm_time(self.nodeid,data.processor_id+1) if data.processor_id+1 > 0 else 1
            self.comm_energy.append([(data.size / temp)*self.energy,data.task_idx]) 
            self.communication_time_rec.append([data.size / temp,data.task_idx])
            print(f'at line 246 current task  received {data.task_idx} from {data.processor_id+1} with communication time {self.communication_time_offload[-1]}')
        elif data:
            print('at lint 248 received: ',data.task_idx)
        else:
            print('empty...')

    def received_call_back(self):
        print('call receive threading...')
        rospy.Subscriber(self.worker_to_uav,Task,self.sub_callback)
        
    def comm_time(self,u1,u2):
        # print(f'uav {u1} and uav {u2}')
        pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
        pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
        d = math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                             [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
        # dr = Datarate()
        return self.datarate.data_rate(d)
    def distance_between_nodes(self,u1,u2):
        pos_1= rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u1, PoseStamped)
        pos_2 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%u2, PoseStamped)
        return math.dist([pos_1.pose.position.x,pos_1.pose.position.y,pos_1.pose.position.z],
                             [pos_2.pose.position.x,pos_2.pose.position.y,pos_2.pose.position.z])
    def run(self,dt):
        print(f'publishing...')
        thread = threading.Thread(target= self.received_call_back)
        thread.start()
        for x in dt:
            self.fly_energy.append([self.energy * (x.size / self.cpu),x.task_idx])
            if self.distance_between_nodes(self.nodeid,x.processor_id+1) > self.comm_range:
                print('**'*20)
                print('Communication Failed......')
                print('**'*20)
            else:
                if x.processor_id == 0:
                    if self.distance_between_nodes(self.nodeid,self.locate_pred(x)+1) > self.comm_range:
                        print('**'*20)
                        print('at line 291 Communication Failed......')
                        print('**'*20)
                        continue
                    else:
                        location_predecessor = self.locate_pred(x)
                        trans_time = x.size / self.comm_time(self.nodeid,location_predecessor+1) if location_predecessor != 0 else 0
                        x.st = max(self.master_task[-1].et, self.pred_aft(x)+trans_time) if self.master_task else self.pred_aft(x)+trans_time
                        x.et = x.st + ((x.size/x.ci)*10)
                        self.comp_energy.append([x.delta * (x.size/x.ci),x.task_idx])
                        self.comp_time.append([(x.size/x.ci),x.task_idx])
                        self.master_task.append(x)
                        if self.master_task[-1].st < 0:
                            continue
                        rospy.sleep(x.size/x.ci) #simulate computation time
                        self.pub.publish(x)
                        rospy.sleep(self.sleepTime) #communication delay
                else:
                    #plus communication time
                    temp = self.comm_time(self.nodeid,x.processor_id+1)
                    x.st = self.pred_aft(x) + (x.size / temp)
                    self.communication_time_offload.append([x.size / temp,x.task_idx])
                    # print(f'at line 261 current task {x.task_idx} not on master with communication time {self.communication_time_offload[-1]}')
                    self.comm_energy.append([(x.size / temp)*self.energy,x.task_idx]) #units: mj
                    # rospy.sleep(x.size/x.ci) #simulate computation time
                    self.pub.publish(x)
                    print(f'after pub task {x.task_idx} st is {x.st}')
                    rospy.sleep(self.sleepTime) #communication delay
        print(f'at line 268 total task{len(dt)}, and {len(self.communication_time_offload)}')
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
        while True: 
            if rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%self.worker_id, PoseStamped).pose.position.z + 0.1 > 0:
                break
        rospy.Subscriber(self.topic, Task, self.callback_func)

    def pred_aft(self,t):
        temp =[0]
        for pre in t.dependency:
            for x in self.all_task:
                if pre == x.task_idx and x.processor_id != t.processor_id:
                    temp.append(x.et)
        return max(temp)
    def callback_func(self,data):

        print(f'at line 379 {data.task_idx}')
        self.fly_energy.append([self.energy * (data.size / self.cpu),data.task_idx])
        self.all_task.append(data)
        if data.processor_id == self.worker_id - 1 :
            # print('/uav%d/ground_truth_to_tf/pose'%(data.processor_id+1))
            worker_1 = rospy.wait_for_message('/uav%d/ground_truth_to_tf/pose'%(data.processor_id+1),PoseStamped)
            worker_2 = rospy.wait_for_message(self.loc,PoseStamped)

            distance = math.dist([worker_1.pose.position.x,worker_1.pose.position.y,worker_1.pose.position.z],
                                [worker_2.pose.position.x,worker_2.pose.position.y,worker_2.pose.position.z])
            current_datarate = self.datarate.data_rate(distance)
            print(f'task {data.task_idx} on {data.processor_id}')
            data.st = max(self.worker_task[-1].et, self.pred_aft(data),data.st) if self.worker_task else max(self.pred_aft(data),data.st)
            data.et = data.st +((data.size / data.ci)*10) #add more computation time
            self.comp_energy.append([data.delta *(data.size/data.ci),data.task_idx]) #units: mj
            self.comp_time.append([(data.size / data.ci),data.task_idx] )
            self.comm_energy.append([(data.size / current_datarate) * self.energy,data.task_idx]) #units: j
            self.communication_time.append(data.size / current_datarate)
            rospy.sleep((data.size / data.ci)) #simulate computation time
            self.pub.publish(data)
            rospy.sleep(self.sleepTime) #communication delay
            self.worker_task.append(data)
        else:
            print('empty')

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
