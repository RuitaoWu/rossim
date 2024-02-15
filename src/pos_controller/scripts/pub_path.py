#!/usr/bin/env python
PKG = 'pos_controller'

import roslib; roslib.load_manifest(PKG)

import rospy
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

path = Path()
ns = rospy.get_namespace()
index = int(ns[-2])

def odom_cb(data):
    global path
    path.header = data.header
    path.header.frame_id = "world"
    pose = PoseStamped()
    print('data*****************************')
    
    pose.header = data.header
    pose.pose = data.pose.pose
    path.poses.append(pose)
    path_pub.publish(path)

rospy.init_node('path_node%d' %index)

odom_sub = rospy.Subscriber('/uav%d/ground_truth/state' %index, Odometry, odom_cb)
path_pub = rospy.Publisher('/path%d' %index, Path, queue_size=10)

if __name__ == '__main__':
    rospy.spin()
