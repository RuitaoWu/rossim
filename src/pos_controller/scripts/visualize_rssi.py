#! /usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import argparse
from matplotlib.ticker import MaxNLocator
import pickle
from scipy.interpolate import interp1d

num_uavs = 4


rssi_file_name = '../data/rssi_data.pkl'
with open(rssi_file_name, 'rb') as fp:
    rssi_data = pickle.load(fp)

plt.figure()
font_size = 15
ax = plt.axes(projection='3d')


# new_t = 1
min_value = float('inf')
for i in range(1, num_uavs+1):
    time_file = '../data/path_time%d.pkl' %i
    with open(time_file, 'rb') as fp:
        time = pickle.load(fp)
        # print('min time', np.min(time))
        value = np.max(time)
        # print('time', value)

    min_value = min(min_value, value)

new_t = np.arange(1, min_value, 0.1)
length = len(new_t)

# print('min value', min_value)
paths_x = []
paths_y = []
paths_z = []
linestyles = ['-', '-.', ':', '--']
font_size = 18

for i in range(1, num_uavs+1):

    path_x_file = '../data/path_x%d.pkl' %i
    path_y_file = '../data/path_y%d.pkl' %i
    path_z_file = '../data/path_z%d.pkl' %i

    time_file = '../data/path_time%d.pkl' %i
    with open(time_file, 'rb') as fp:
        time = pickle.load(fp)

    #print('time1', len(time1))
    with open(path_x_file, 'rb') as fp:
        path_x = pickle.load(fp)

    interp_funcx = interp1d(time, path_x)
    new_x = interp_funcx(new_t)

    with open(path_y_file, 'rb') as fp:
        path_y = pickle.load(fp)
    # print(len(time),len(path_y),len(path_x))
    interp_funcy = interp1d(time, path_y)

    new_y = interp_funcy(new_t)

    with open(path_z_file, 'rb') as fp:
        path_z = pickle.load(fp)
    interp_funcz = interp1d(time, path_z)
    new_z = interp_funcz(new_t)
    #print('path x', path_x[-1], 'path y', path_y[-1], 'path_z', path_z[-1])
    paths_x.append(new_x)
    paths_y.append(new_y)
    paths_z.append(new_z)
    #ax.plot3D(new_x, new_y, new_z, label = 'UAV%d' %i)
    if i == 1:
        ax.plot3D(path_x, path_y, path_z, linestyle=linestyles[i-1], linewidth = 3.5, label = 'Master')
    else:
        ax.plot3D(path_x, path_y, path_z, linestyle=linestyles[i-1], linewidth = 3.5, label = 'Worker %d' %(i-1))
# ax.plot3D(path2_x, path2_y, path2_z, label = 'UAV2')
# ax.plot3D(path3_x, path3_y, path3_z, label = 'UAV3')
# ax.plot3D(path4_x, path4_y, path4_z, label = 'UAV4')
ax.set_xlabel('X (m)', fontsize=font_size)
ax.set_ylabel('Y (m)', fontsize=font_size)
ax.set_zlabel('Z (m)', fontsize=font_size)
plt.subplots_adjust(bottom=0.15, left=0.2, top=0.95, wspace=0, hspace=0)
#plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax.legend(fontsize=font_size)
plt.savefig('ros_path')
plt.show()

masterx = paths_x[0]
mastery = paths_y[0]
masterz = paths_z[0]

def comm_bandwidth(rssi):
    S = 10 ** ((rssi - 30) / 10)
    b = 1 + S / (1.1 * 10 ** (-35))
    bandwidth = 1.2 * 10 ** 6  * np.log2(b)
    #print(bandwidth)
    return bandwidth


plt.figure()
num_workers = 3
rssi_file_name = '/home/smile/nac_sim/src/ros_mpi/data/comp_rssi.pkl'
with open(rssi_file_name, 'rb') as fp:
    rssi_data = pickle.load(fp)
#print(rssi_data[1])
time = [value[0] for value in rssi_data]
data_comms = []
for i in range(num_workers):
    data_comms.append([comm_bandwidth(value[1+i])*10**(-6) for value in rssi_data])
    #data_comms.append([value[1+i] for value in rssi_data])
    #plt.plot(time, data_comms[i], label='UAV%d comm'  %(i+2))



font_size = 15
for j in range(1, num_uavs):
    dist = [np.sqrt((paths_x[j][k]-masterx[k])**2 + (paths_y[j][k]-mastery[k])**2 + (paths_z[j][k]-masterz[k])**2) for k in range(length)]
    plt.plot(new_t, dist, linestyle=linestyles[j-1], linewidth = 3.5, label = 'Master and worker %d' %(j))
plt.subplots_adjust(bottom=0.15, left=0.2, top=0.95, wspace=0, hspace=0)
plt.xlabel('Time (s)', fontsize=font_size)
plt.ylabel('Distance (m)', fontsize=font_size)
#plt.xlim([0, 0])
plt.xticks(fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.legend(fontsize=font_size)
# plt.savefig('ros_dist')
plt.show()
