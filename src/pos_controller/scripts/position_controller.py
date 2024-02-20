#!/usr/bin/env python
import rospy, tf
import geometry_msgs.msg, nav_msgs.msg
from geometry_msgs.msg import PoseStamped,TwistStamped
from math import *
from time import sleep


def control_callback(message, cargs):
    # Implementation of proportional position control

    # Callback arguments
    pub, msg, goal = cargs

    # Tunable parameters
    kdx = 0.1
    kdy = 0.1
    kdz = 0.1

    curr_x, curr_y, curr_z = message.pose.position.x, message.pose.position.y, message.pose.position.z

    distThresh = 0.2 # Distance treshold [m]


    #Euclidean distance
    dist = sqrt((curr_x-goal[0])**2 + (curr_y-goal[1])**2 + (curr_z-goal[2])**2)


    if (dist > distThresh):
        vx, vy, vz = kdx * (goal[0] - curr_x), kdy * (goal[1]- curr_y), kdz * (goal[2]- curr_z)

        # Publish
        msg.linear.x = vx
        msg.linear.y = vy
        msg.linear.z = vz
        pub.publish(msg)

        # Reporting
        print('control_callback: x = %4.1f, y = %4.1f, z = %4.1f, dist = %4.2f, vx = %4.2f, vy = %4.2f, vz = %4.2f' %(curr_x, curr_y, curr_z, dist, vx, vy, vz))

########################################
# Main Script
# Initialize our node
rospy.init_node('UAV position controller',anonymous=True)

# Set waypoint for Husky to drive to
goal = [-6,-6, 5]  # Goal

# Setup publisher

cmdmsg = geometry_msgs.msg.Twist()
print("msg#######################################################")
print(cmdmsg)
cmdpub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)

# Setup subscription - which implemets our controller.
# We pass the publisher, the message to publish and the goal as
# additional parameters to the callback function.
rospy.Subscriber('/ground_truth_to_tf/pose', PoseStamped, control_callback,
                 (cmdpub, cmdmsg, goal))
# spin() simply keeps python from exiting until this node is stopped
rospy.spin()
