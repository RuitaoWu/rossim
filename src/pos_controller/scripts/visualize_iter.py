#! /usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import argparse
from matplotlib.ticker import MaxNLocator
import pickle
from scipy.interpolate import interp1d

num_uavs = 3


def comm_bandwidth(rssi_value):
    S = 10 ** ((rssi_value - 30) / 10)
    b = 1 + S / (1.1 * 10 ** (-35))
    bandwidth = 1.2 * 10 ** 6  * np.log2(b)
    #print(bandwidth)
    return bandwidth


rssi_file_name = '../data/rssi_data.pkl'
with open(rssi_file_name, 'rb') as fp:
    rssi_data = pickle.load(fp)

# print(rssi_data[0])
time = [value[0] for value in rssi_data]
for i in range(num_uavs):
    rssi = [comm_bandwidth(value[i+1])*10**(-6) for value in rssi_data]
    plt.plot(time, rssi, label = 'UAV 1 and UAV %d' %(i+2))

font_size = 15
plt.xlabel('Time (s)', fontsize=font_size)
plt.ylabel('Bandwidth (Mbits/s)', fontsize=font_size)
plt.xlim([2, 100])
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.legend(fontsize=font_size)
plt.savefig('time_bandwidth')
plt.show()
