#!/usr/bin/env python3
'''
Author: BaoqianWang
Date Created: 03/16/2022
Description: Waypoint follower

Modified by: Ruitao Wu
Date modified: 02/21/2024
Description: added random walk
'''
import configparser
# from mobility import random_direction
from operator import index
import rospy, tf
import geometry_msgs.msg, nav_msgs.msg
from math import *
import numpy as np
from time import sleep
import time
import json
import roslib
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import PoseStamped
PKG = 'pos_controller'
roslib.load_manifest(PKG)

ns = rospy.get_namespace()

# index = int(ns[-2])
'''
Modified by: Ruitao Wu
the ns will return: /uav1/
detect if the third last to second last two char in a string is numerical data or not
if it is numerical data then convert it to int
else
convert the second last to int
'''
if ns[-3:-1].isnumeric():
    index = int(ns[-3:-1])
else:
    index = int(ns[-2])

class WaypoingFollower:
    '''
    waypoint following implementation
    '''
    def __init__(self, pos0, node_name="waypointfollower%d" %index):
        rospy.init_node(node_name)
        self.pose = [pos0[0], pos0[1], pos0[2]]
        # self.ini_pos = initial_pos
        #default gain val
        # self.kdx = 0.15
        # self.kdy = 0.15
        # self.kdz = 0.15
        self.kdx = 2
        self.kdy = 2
        self.kdz = 2

        #mobility configuration
        self.config = configparser.ConfigParser()
        # self.config.read('/home/jxie/rossim/src/ros_mpi/scripts/property.properties')
        self.config.read('/home/ad/rossim/src/ros_mpi/scripts/property.properties')
        self.xMax = float(self.config.get('Mobile','xMax'))
        self.xMin = float(self.config.get('Mobile','xMin'))
        self.yMax = float(self.config.get('Mobile','yMax'))
        self.yMin = float(self.config.get('Mobile','yMin'))
        self.zMax = float(self.config.get('Mobile','zMax'))
        self.zMin = float(self.config.get('Mobile','zMin'))
        self.numberOfPoints = int(self.config.get('Mobile','numberOfPoints'))
        

        self.sub_topic = '/uav%d/ground_truth_to_tf/pose' %index
        self.pub_topic = '/uav%d/cmd_vel' %index
        self.distThresh = 0.3

    #position generation function
    def random_waypoint(self,num_nodes, area_size, max_speed, max_time):
        """
        Simulate the Random Waypoint model with random direction in (x, y, z) space.

        Parameters:
        - num_nodes: Number of nodes in the simulation.
        - area_size: Size of the simulation area (x_max, y_max, z_max).
        - max_speed: Maximum speed of nodes.
        - max_time: Maximum simulation time.

        Returns:
        - positions: Final positions of nodes after simulation.
        """

        # Initialize positions and velocities
        positions = np.random.rand(num_nodes, 3) * area_size
        velocities = np.zeros((num_nodes, 3))

        # Simulate movement
        current_time = 0
        while current_time < max_time:
            # Choose a random node
            node_index = np.random.randint(num_nodes)

            # Generate a random destination within the area
            destination = np.random.rand(3) * area_size

            # Calculate direction and normalize
            direction = destination - positions[node_index]
            direction /= np.linalg.norm(direction)

            # Calculate a random speed within the specified range
            speed = np.random.uniform(0, max_speed)

            # Update velocity towards the destination
            velocities[node_index] = direction * speed

            # Update position based on velocity
            positions += velocities

            # Increment time
            current_time += 1

        return positions.tolist()

        return positions
    def get_pos(self, message):
        # Implementation of proportional position control
        self.pose = [message.pose.position.x, message.pose.position.y, message.pose.position.z]



    def run(self):
        msg = geometry_msgs.msg.Twist()
        pub = rospy.Publisher(self.pub_topic, geometry_msgs.msg.Twist, queue_size=10)
        rospy.Subscriber(self.sub_topic, PoseStamped, self.get_pos)
        print("at line 96 waypoint followerpy namespace: ",ns)
        #src/pos_controller/scripts/path.txt
        filename = '/home/jxie/rossim/src/pos_controller/scripts/path.txt'
        with open(filename, 'r') as fd:
            path=json.load(fd)
        path = path['uav%d'%index]
 
        #generate random position within ceratin aera in 3D space
        # allPositions = self.random_waypoint(10,100,2,100)
        px,py,pz = [],[],[]
        for p in self.random_waypoint(50,400,5,200):
            px.append(p[0])
            py.append(p[1])
            pz.append(abs(p[2]))
        for goal_x, goal_y, goal_z in zip(path['x'], path['y'], path['z']):
        # for goal_x, goal_y, goal_z in zip(px,py, pz):
            print('Goal is', goal_x, goal_y, goal_z)
            print('Current position: x=%4.1f, y=%4.1f, z=%4.1f'%(self.pose[0], self.pose[1], self.pose[2]))
            distance = sqrt((self.pose[0]-goal_x)**2 + (self.pose[1]-goal_y)**2 + (self.pose[2]-goal_z)**2)
            while distance > self.distThresh:
                distance = sqrt((self.pose[0]-goal_x)**2 + (self.pose[1]-goal_y)**2 + (self.pose[2]-goal_z)**2)

                vx, vy, vz = self.kdx * (goal_x- self.pose[0]), self.kdy * (goal_y- self.pose[1]), self.kdz * (goal_z- self.pose[2])

                # Publish
                msg.linear.x = vx
                msg.linear.y = vy
                msg.linear.z = vz
                pub.publish(msg) # control frequency
                print('control_callback: x = %4.1f, y = %4.1f, z = %4.1f, dist = %4.2f, vx = %4.2f, vy = %4.2f, vz = %4.2f' %(self.pose[0], self.pose[1], self.pose[2], distance, vx, vy, vz))

        while not rospy.is_shutdown():
            # distance = sqrt((self.pose[0]-goal_x)**2 + (self.pose[1]-goal_y)**2 + (self.pose[2]-goal_z)**2)
            # while distance > self.distThresh:
            distance = sqrt((self.pose[0]-goal_x)**2 + (self.pose[1]-goal_y)**2 + (self.pose[2]-goal_z)**2)

            vx, vy, vz = self.kdx * (goal_x- self.pose[0]), self.kdy * (goal_y- self.pose[1]), self.kdz * (goal_z- self.pose[2])

            # Publish
            msg.linear.x = vx
            msg.linear.y = vy
            msg.linear.z = vz
            pub.publish(msg) # control frequency


# if __name__ == "__main__":
#     sleep(10)
#     print("namespace: ")
#     print(ns)
#     waypoint_follower = WaypoingFollower([0, 0, 0.3])
#     waypoint_follower.run()
#     rospy.spin()
