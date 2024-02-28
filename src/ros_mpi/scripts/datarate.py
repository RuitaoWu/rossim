import math
import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from geometry_msgs.msg import PoseStamped
class Datarate:
    def __init__(self) -> None:
        # self.uavlist = uavlist
        pass
    #transmission power is 500 mW converted to watts  0.5 
    #noise power is -100dBm converted to watts 0.0000000000001
    #band width is 5MHz 5000000 # 5MHz
    def channel_gain(self,distance, alpha=4.0):
        return distance ** (-alpha)
    def data_rate(self,channel_gain, noise=0.000001,band_width=5000000 , transmission_power=0.5):
        return band_width * math.log2(1 + (transmission_power* channel_gain))/noise
if __name__ == '__main__':
    # test = Datarate([0,1,2])
    test = Datarate()
    print(test.data_rate(test.channel_gain(400)))