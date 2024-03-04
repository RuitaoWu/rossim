import math
import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from geometry_msgs.msg import PoseStamped
class Datarate:
    def __init__(self,noise=0.0000000001,band_width=5000000 , transmission_power=0.05,alpha=4.0) -> None:
        self.noise=noise
        self.band_width=band_width
        self.transmission_power=transmission_power
        self.alpha=alpha
        # self.v=distance
    def __str__(self) -> str:
        return 'datarate object information noise {} bandwidth {} transmission power {} and alpha {}'.format(self.noise,self.band_width,self.transmission_power,self.alpha)

    def data_rate(self,distance):
        return self.band_width * math.log2(1 + (self.transmission_power* (distance ** (-self.alpha))))/self.noise
if __name__ == '__main__':
    test = Datarate()
    print(test.data_rate(400))