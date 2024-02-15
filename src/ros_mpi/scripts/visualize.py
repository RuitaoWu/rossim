#! /usr/bin/env python
from math import dist
import matplotlib
from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np
import argparse
from matplotlib.ticker import MaxNLocator
import pickle
from scipy.interpolate import interp1d

# from ros_mpi.scripts.node import comm_time


def comm_bandwidth(rssi):
    S = 10 ** ((rssi - 30) / 10)
    b = 1 + S / (1.1 * 10 ** (-35))
    bandwidth = 1.2 * 10 ** 6  * np.log2(b)
    # print(bandwidth)
    return bandwidth

plt.figure(figsize=(7,5))

linestyles = ['-', '-.', ':', '--','--','--','--','--','--','--','--','--']
#change the number workers
num_workers = 4
# rssi_file_name = '../data/comp_rssi.pkl'
# rssi_file_name='/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/data/comp_rssi.pkl'
# rssi_file_name='/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/exp-3/new-exp-3/10000rows/uncoded/comp_rssi.pkl'
# dist_file = '/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/exp-3/new-exp-3/10000rows/uncoded/uav_distance.pkl'
# rssi_file_name='/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/exp-3/new-exp-3/10000rows/coded/comp_rssi.pkl'
# dist_file = '/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/exp-3/new-exp-3/10000rows/coded/uav_distance.pkl'
# rssi_file_name = '../data/comp_rssi.pkl'
# with open(rssi_file_name, 'rb') as fp:
#     rssi_data = pickle.load(fp)
with open('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/exp-3/new-exp-3/10000rows/uncoded/comp_rssi.pkl', 'rb') as fp:
    rssi_data = pickle.load(fp)
with open('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/exp-3/new-exp-3/10000rows/uncoded/uav_distance.pkl', 'rb') as fp:
    dist = pickle.load(fp)

# time = [value[0] for value in rssi_data]
data_comms = []
rssi_data_temp = []
for i in range(num_workers):
    # data_comms.append([comm_bandwidth(value[1+i])*10**(-6) for value in rssi_data])
    # plt.plot(time, data_comms[i], linestyle = linestyles[i], linewidth = 3.5, label='Master and worker %d' %(i+1))
    data_comms.append([comm_bandwidth(value[1+i])*10**(-6) for value in rssi_data])
    plt.plot(dist, data_comms[i], linestyle = linestyles[i], linewidth = 3.5, label='Master and worker %d' %(i+1))
plt.legend()
plt.xlabel('Time (s)', fontsize=24)
plt.ylabel('Throughput (Mbps)', fontsize=24)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=12)
plt.subplots_adjust(bottom=0.13, left=0.12,right=0.98, top=0.99, wspace=0, hspace=0)
# plt.savefig('ros_rssi_static')
# plt.ylim([26,38])
# plt.xlim([45,61])
plt.tight_layout()
plt.show()



# plt.figure()
# comp_time_file = '/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/data/comp_time.pkl'
# # comp_time_file = '/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/exp-3/new-exp-3/10000rows/coded/comp_time.pkl'
# # comp_time_file='/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/exp-3/new-exp-3/10000rows/coded/comp_time.pkl'
# with open(comp_time_file, 'rb') as fp:
#     comp_time = pickle.load(fp)

# plt.plot(time, comp_time, linewidth = 3,marker="o")
# plt.xlabel('Time (m)', fontsize=24)
# plt.ylabel('Task completion time (s)', fontsize=24)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# # plt.ylim([0,20])
# # plt.xlim([45,61])
# plt.subplots_adjust(bottom=0.15, left=0.2, top=0.95, wspace=0, hspace=0)
# plt.tight_layout()
# plt.show()
