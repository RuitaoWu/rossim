#!/usr/bin/env python3
PKG = 'pos_controller'

import roslib; roslib.load_manifest(PKG)

import rospy
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
import pickle,os

ns = rospy.get_namespace()
# index = int(ns[-2])
if ns[-3:-1].isnumeric():
    index = int(ns[-3:-1])
else:
    index = int(ns[-2])

    
time = []
pos_x = []
pos_y = []
pos_z = []
#/home/jxie/rossim/src/pos_controller/data
# folder_path = "/home/jxie/rossim/src/pos_controller/data"
folder_path = '/home/ad/rossim/src/pos_controller/data'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print("Folder created.")
else:
    print("Folder already exists. Skipping.")
    
# time_file_name = '/home/jxie/rossim/src/pos_controller/data/path_time%d.pkl' %index
# path_x_name = '/home/jxie/rossim/src/pos_controller/data/path_x%d.pkl' %index
# path_y_name = '/home/jxie/rossim/src/pos_controller/data/path_y%d.pkl' %index
# path_z_name = '/home/jxie/rossim/src/pos_controller/data/path_z%d.pkl' %index

time_file_name = '/home/ad/rossim/src/pos_controller/data/path_time%d.pkl' %index
path_x_name = '/home/ad/rossim/src/pos_controller/data/path_x%d.pkl' %index
path_y_name = '/home/ad/rossim/src/pos_controller/data/path_y%d.pkl' %index
path_z_name = '/home/ad/rossim/src/pos_controller/data/path_z%d.pkl' %index


def path_cb(data):
    # print('pose data', data)
    time.append(rospy.get_time())
    pos_x.append(data.pose.position.x)
    pos_y.append(data.pose.position.y)
    pos_z.append(data.pose.position.z)
    #print('simulation time', rospy.get_time(), rospy.Time.now(), data.pose.position.z)
    with open(time_file_name, 'wb') as fp1:
        pickle.dump(time, fp1)

    with open(path_x_name, 'wb') as fp2:
        pickle.dump(pos_x, fp2)

    with open(path_y_name, 'wb') as fp3:
        pickle.dump(pos_y, fp3)

    with open(path_z_name, 'wb') as fp4:
        pickle.dump(pos_z, fp4)



rospy.init_node('path_recording_node%d' %index)

odom_sub = rospy.Subscriber('/uav%d/ground_truth_to_tf/pose' %index, PoseStamped, path_cb)



if __name__ == '__main__':
    rospy.spin()
