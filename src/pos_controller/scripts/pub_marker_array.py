#! /usr/bin/env python
from fileinput import filename
import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import json
PKG = 'pos_controller'
from time import sleep

import roslib; roslib.load_manifest(PKG)
sleep(2)
ns = rospy.get_namespace()
#print(ns)
index = int(ns[-2])


rospy.init_node('rviz_marker_array%d' %index)
# /home/jxie/Workspace/hzhang3986/nac_sim/src/pos_controller/scripts/path.txt
# filename = '/home/smile/nac_sim/src/pos_controller/scripts/path.txt'
# filename ='/home/jxie/Workspace/hzhang3986/nac_sim/src/pos_controller/scripts/path.txt'
#/home/jxie/rossim/src/pos_controller/scripts
filename ='/home/jxie/rossim/src/pos_controller/scripts/path.txt'
with open(filename, 'r') as fd:
    path = json.load(fd)

path = path['uav%d'%index]


marker_pub = rospy.Publisher("/visualization_marker_array%d" %index, MarkerArray, queue_size = 2)
markerArray = MarkerArray()
i = 0
# Three agents
color = [[255, 255, 0], [0, 255, 255], [255, 0, 255], [255, 125, 255]]
for x, y, z in zip(path['x'], path['y'], path['z']):
    marker = Marker()
    marker.header.frame_id = "world"
    marker.header.stamp = rospy.Time.now()

    # set shape, Arrow: 0; Cube: 1 ; Sphere: 2 ; Cylinder: 3
    marker.type = 1
    marker.id = i

    # Set the scale of the marker
    marker.scale.x = 0.32
    marker.scale.y = 0.32
    marker.scale.z = 0.32

    # Set the color
    marker.color.r = color[index-1][0]
    marker.color.g = color[index-1][1]
    marker.color.b = color[index-1][2]
    marker.color.a = 1.0

    # Set the pose of the marker
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = z
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0

    markerArray.markers.append(marker)
    i += 1


while not rospy.is_shutdown():
  marker_pub.publish(markerArray)
  rospy.rostime.wallsleep(1.0)
