
from concurrent.futures import thread
from turtle import pos
from collections import defaultdict
from hector_uav_msgs.msg import Task, FinishTime
from orchestrator import Orchestrator
import rospy,threading
from geometry_msgs.msg import PoseStamped



task_ast = defaultdict(list)
task_aft = defaultdict(list)

class Master:
    def __init__(self) -> None:
        print('construcing master node')
        self.topic = '/uav1/task'
        self.loc = '/uav1/ground_truth_to_tf/pose'
        self.worker_to_uav = '/worker/task'
        rospy.init_node('Master', anonymous=True)
        self.pub = rospy.Publisher(self.topic,Task,queue_size=10)
        self.rate = rospy.Rate(1) # 10hz
        self.master_task = []
        self.task_received = []
        # self.sch_list = sch
        print('master node is completed')
    def pred_aft(self,t):
        temp =[0]
        for pre in t.dependency:
            if task_aft[pre]:
                temp.append(task_aft[pre])
        return max(temp)
    def sub_callback(self,data):
        if data:
            print('subscriber call back function...')
            self.task_received.append(data)
        else:
            print('nothing...')
    # def received_call_back(self):
    #     print('call receive threading...')
    #     rospy.Subscriber(self.worker_to_uav,Task,self.sub_callback)
    def run(self,dt):
        print(f'publishing...')
        # thread = threading.Thread(target= self.received_call_back)
        # thread.start()
        rospy.Subscriber(self.worker_to_uav,Task,self.sub_callback)
        for x in dt:
            print(f'publishing task {x.task_idx}')
            if x.processor_id == 0:
                x.st = self.master_task[-1].et if self.master_task else 0
                x.et = x.st + (x.size/1000000)
                self.master_task.append(x)
                # if self.master_task[-1] and task_ast[self.master_task[-1].task_idx]:
                #     task_ast[x.task_idx] = max(self.pred_aft(x),task_ast[self.master_task[-1].task_idx])
                # else:
                #     task_ast[x.task_idx] = self.pred_aft(x)
                # task_aft[x.task_idx] = task_ast[x.task_idx] + 10
            print(f'x start {x.st} and x end {x.et}')
            self.pub.publish(x)
            print(f'completed task {x.task_idx}')
            rospy.sleep(1)
        #all tasks
        with open('/home/jxie/rossim/src/ros_mpi/data/task_ast_master.txt','w') as file:
            # for key, values in task_ast.items():
            #     file.write(f"{key}: {values}\n")
            for ele in self.task_received :
                file.write(f"{ele}\n\n")
        #task on master
        with open('/home/jxie/rossim/src/ros_mpi/data/task_on_master.txt','w') as file:
            # for key, values in task_ast.items():
            #     file.write(f"{key}: {values}\n")
            for ele in self.master_task :
                file.write(f"{ele}\n\n")




class Worker:
    def __init__(self,worker_id) -> None:
        print('constructing worker node ',worker_id)
        self.worker_id = worker_id
        self.topic = '/uav1/task'
        self.worker_to_uav = '/worker/task'
        self.loc = '/uav%d/ground_truth_to_tf/pose'%self.worker_id
        rospy.init_node('Worker%d'%self.worker_id , anonymous=True)
        self.pub = rospy.Publisher(self.worker_to_uav,Task,queue_size=20)
        self.worker_task = []
    
    def pred_aft(self,t):
        temp =[0]
        for pre in t.dependency:
            if task_aft[pre]:
                temp.append(task_aft[pre])
        return max(temp)
    def callback_func(self,data):
        if data.processor_id == self.worker_id:
            print(f'task time at line 90 {data.st}')
            # if self.worker_task[-1] and task_ast[self.worker_task[-1].task_idx]:
            #     # task_ast[data.task_idx] = max(self.pred_aft(data),task_ast[self.worker_task[-1].task_idx])
            #     data.st = max(self.pred_aft(data),task_ast[self.worker_task[-1].task_idx])
            # else:
            #     # task_ast[data.task_idx] = self.pred_aft(data)
            #     # task_aft[data.task_idx] = task_ast[data.task_idx] + 10
            #     data.st = max(self.pred_aft(data),task_ast[self.worker_task[-1].task_idx])
            #     data.et = data.st + 10
            print('dependency',data.dependency)
            data.st = 10
            self.pub.publish(data)
            rospy.sleep(1)
            print(f'task time at line 103: {data.st}')
            print('**********************************************************')
            self.worker_task.append(data)
            with open('/home/jxie/rossim/src/ros_mpi/data/task_ast_worker%d.txt'%self.worker_id,'w') as file:
                # for key, values in task_ast.items():
                #     file.write(f"{key}: {values}\n")
                for ele in self.worker_task:
                    file.write(f"{ele}\n")
        else:
            print('empty')
    #sub location information
    def location_thread(self):
        pos = rospy.wait_for_message(self.loc, PoseStamped)
        print(f'current worker location : ({pos.pose.position.x},{pos.pose.position.y})')
    def sub_thread(self):
        rospy.Subscriber(self.topic, Task, self.callback_func)
    def run(self):
        print('call worker%d'%self.worker_id )
        rospy.Subscriber(self.topic, Task, self.callback_func)
        # pos = rospy.wait_for_message(self.loc, PoseStamped)
        # print(f'current worker location : ({pos.pose.position.x},{pos.pose.position.y})')
        # thread_sub = threading.Thread(target=self.sub_thread)
        # thread_loc = threading.Thread(target=self.location_thread)
        # thread_sub.start()
        # thread_loc.start()
        print(f'worker {self.worker_id} done')
        rospy.spin()