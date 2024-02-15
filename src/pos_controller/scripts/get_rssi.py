#!/usr/bin/env python3
PKG = 'pos_controller'
from time import sleep
import roslib; roslib.load_manifest(PKG)
sleep(2)
import rospy
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32MultiArray
import pickle


rssi_data = []
rssi_file_name = '/home/jxie/Workspace/hzhang3986/nac_sim/src/pos_controller/data/rssi_data.pkl'

def rssi_cb(data):
    rssi_data.append(data.data)
    #with open(rssi_file_name, 'wb') as fp:
        #print('saving file...........')
        #pickle.dump(rssi_data, fp)
    #print('data*****************************')

rospy.init_node('rssi_data_recording')

rssi_sub = rospy.Subscriber('/recv_Signal', Float32MultiArray, rssi_cb)


if __name__ == '__main__':
    rospy.spin()
