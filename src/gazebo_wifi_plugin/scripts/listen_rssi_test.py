#!/usr/bin/env python

PKG = 'ros_mpi'

import roslib; roslib.load_manifest(PKG)

import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import Float32MultiArray

def callback(data):
    print rospy.get_name(), "I heard %s" %str(data.data)

def listener():
    rospy.init_node('listener')
    rospy.Subscriber("recv_Signal", Float32MultiArray, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
