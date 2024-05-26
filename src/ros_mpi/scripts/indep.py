
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
from std_msgs.msg import String
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

'''
def dist(array,n):
    ele_per_pie = len(array) // n
    remainder = len(array)%n
    res = []
    st = 0
    for i in range(n):
        et = st +ele_per_pie +(1 if i > remainder else 0)
        res.append(array[st:et])
        st=et
    return res
'''
class Parent:
    def __init__(self,node_id) -> None:
        numberOfTask = int(config.get('Task','numberOfTask'))
        self.numberOfComputingNode = int(config.get('Task','computing'))
        task_size_min = int(config.get('Task','task_size_min'))
        task_size_max = int(config.get('Task','task_size_max'))
        ipsMax = int(config.get('Task','ips_max'))
        ipsMin = int(config.get('Task','ips_min'))
        taskgenerator = TaskGen(random.randint(numberOfTask // 2, numberOfTask),self.numberOfComputingNode,task_size_min,task_size_max,ipsMin,ipsMax)
        self.cpu = random.randint(100000000,200000000)
        self.task = taskgenerator.gen_indep()
        self.pubTopic = 'pub/task'
        self.taskQ = []
        self.node_id = node_id
        rospy.init_node('uav%d'%(node_id), anonymous=True)
        self.pub = rospy.Publisher(self.pubTopic,Task,queue_size=10)
        # self.pub = rospy.Publisher("chatter",String,queue_size=10)
        self.rate = rospy.Rate(1) # 10hz
    #distribution system
    def dist(self,array,n):
        ele_per_pie = len(array) // n
        remainder = len(array)%n
        res = []
        st = 0
        for i in range(n):
            et = st +ele_per_pie +(1 if i > remainder else 0)
            res.append(array[st:et])
            st=et
        return res
    def run(self):
        task = self.dist(self.task,self.numberOfComputingNode)
        for i in task:
            for t in i:
                t.processor_id = (task.index(i)+1)
                if t.processor_id == self.node_id:
                    if self.taskQ:
                        t.st = self.taskQ[-1].et
                        t.et = t.st + t.ci/self.cpu
                        self.taskQ.append(t)
                    else:
                        t.st = 0
                        t.et = t.st + t.ci/self.cpu
                        self.taskQ.append(t)
                self.pub.publish(t)
                rospy.sleep(0.2)
        print(f'done')
        for x in self.taskQ:
            # print(f'task id {x.task_idx} st {x.st} and et {x.et} and ci {x.ci/self.cpu}')
            print(f'task id {x.task_idx} st {x.st} and et {x.et}')
class Child:
    def __init__(self,node_id) -> None:
        self.pubTopic = 'pub/task'
        self.node_id = node_id
        rospy.init_node('uav%d'%self.node_id, anonymous=True)
        self.taskQ = []
        self.cpu = random.randint(100000000,200000000)
    def sub_callback(self,data):
        if data.processor_id == self.node_id:
            if self.taskQ:
                data.st = self.taskQ[-1].et
                data.et = data.st + data.ci/self.cpu
                self.taskQ.append(data)
            else:
                data.st = 0
                data.et = data.st + data.ci/self.cpu
                self.taskQ.append(data)
            # print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    def run(self):
        rospy.Subscriber(self.pubTopic, Task, self.sub_callback)
        # rospy.Subscriber("chatter", String, self.sub_callback)
        
        rospy.spin()
        print(f'current uav is: {self.node_id}')
        # print(f'at line 97 {self.taskQ}')
        for x in self.taskQ:
            # print(f'task id {x.task_idx} st {x.st} and et {x.et} and ci {x.ci/self.cpu}')
            print(f'task id {x.task_idx} st {x.st} and et {x.et}')
    