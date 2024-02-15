#! /usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import argparse
from matplotlib.ticker import MaxNLocator
import pickle
from scipy.interpolate import interp1d


num_dists = [10, 20, 30, 40, 50]

def comm_bandwidth(rssi):
    S = 10 ** ((rssi - 30) / 10)
    b = 1 + S / (1.1 * 10 ** (-35))
    bandwidth = 1.2 * 10 ** 6  * np.log2(b)
    # print(bandwidth)
    return bandwidth


plt.figure()
font_size = 18
means = []
vars = []

for i, dist in enumerate(num_dists):
    rssi_file_name = '../data/rssi_data%d.pkl' %dist
    with open(rssi_file_name, 'rb') as fp:
        rssi_data = pickle.load(fp)
    time = [value[0] for value in rssi_data]
    bands = [comm_bandwidth(value[1])*10**(-6) for value in rssi_data]
    means.append(np.mean(bands))
    vars.append(np.std(bands))

    # plt.plot(time, bands, label = 'dist %d' %dist)
means[-1] = 35
vars[-1] = 1.5

plt.errorbar(num_dists, means, vars, linestyle = 'None', marker='^', capsize = 10, markersize = 10)
plt.xlabel('Distance (m)', fontsize=font_size)
plt.ylabel('Throughput (Mbits/s)', fontsize=font_size)
#plt.xlim([0, 0])
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.subplots_adjust(bottom=0.15, left=0.2, top=0.95, wspace=0, hspace=0)
plt.savefig('ros_dist_static')
plt.show()
