#! /usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse
from matplotlib.ticker import MaxNLocator
import pickle
from scipy.interpolate import interp1d


rssi_file_name = '../data/rssi_data.pkl'
with open(rssi_file_name, 'rb') as fp:
    rssi_data = pickle.load(fp)


path1_x_file = '../data/path_x1.pkl'
path1_y_file = '../data/path_y1.pkl'
path1_z_file = '../data/path_z1.pkl'
time1_file = '../data/path_time1.pkl'

with open(time1_file, 'rb') as fp:
    time1 = pickle.load(fp)

#print('time1', len(time1))
with open(path1_x_file, 'rb') as fp:
    path1_x = pickle.load(fp)
interp_func1x = interp1d(time1, path1_x)


with open(path1_y_file, 'rb') as fp:
    path1_y = pickle.load(fp)
interp_func1y = interp1d(time1, path1_x)

with open(path1_z_file, 'rb') as fp:
    path1_z = pickle.load(fp)


path2_x_file = '../data/path_x2.pkl'
path2_y_file = '../data/path_y2.pkl'
path2_z_file = '../data/path_z2.pkl'
time2_file = '../data/path_time2.pkl'

with open(time2_file, 'rb') as fp:
    time2 = pickle.load(fp)

print('time2', len(time2))

with open(path2_x_file, 'rb') as fp:
    path2_x = pickle.load(fp)

with open(path2_y_file, 'rb') as fp:
    path2_y = pickle.load(fp)

with open(path2_z_file, 'rb') as fp:
    path2_z = pickle.load(fp)


path3_x_file = '../data/path_x3.pkl'
path3_y_file = '../data/path_y3.pkl'
path3_z_file = '../data/path_z3.pkl'
time3_file = '../data/path_time3.pkl'


with open(time3_file, 'rb') as fp:
    time3 = pickle.load(fp)

print('time3', time3[:5])

with open(path3_x_file, 'rb') as fp:
    path3_x = pickle.load(fp)

with open(path3_y_file, 'rb') as fp:
    path3_y = pickle.load(fp)

with open(path3_z_file, 'rb') as fp:
    path3_z = pickle.load(fp)

path4_x_file = '../data/path_x4.pkl'
path4_y_file = '../data/path_y4.pkl'
path4_z_file = '../data/path_z4.pkl'
time4_file = '../data/path_time4.pkl'

with open(time4_file, 'rb') as fp:
    time4 = pickle.load(fp)

print('time4', time4[:5])

with open(path4_x_file, 'rb') as fp:
    path4_x = pickle.load(fp)

with open(path4_y_file, 'rb') as fp:
    path4_y = pickle.load(fp)

with open(path4_z_file, 'rb') as fp:
    path4_z = pickle.load(fp)

# path5_x_file = '../data/path_x5.pkl'
# path5_y_file = '../data/path_y5.pkl'
# path5_z_file = '../data/path_z5.pkl'
# time5_file = '../data/path_time5.pkl'

# with open(time5_file, 'rb') as fp:
#     time5 = pickle.load(fp)

# with open(path5_x_file, 'rb') as fp:
#     path5_x = pickle.load(fp)

# with open(path5_y_file, 'rb') as fp:
#     path5_y = pickle.load(fp)

# with open(path5_z_file, 'rb') as fp:
#     path5_z = pickle.load(fp)


# path6_x_file = '../data/path_x6.pkl'
# path6_y_file = '../data/path_y6.pkl'
# path6_z_file = '../data/path_z6.pkl'
# time6_file = '../data/path_time6.pkl'

# with open(time6_file, 'rb') as fp:
#     time6 = pickle.load(fp)

# with open(path6_x_file, 'rb') as fp:
#     path6_x = pickle.load(fp)

# with open(path6_y_file, 'rb') as fp:
#     path6_y = pickle.load(fp)

# with open(path6_z_file, 'rb') as fp:
#     path6_z = pickle.load(fp)


# path7_x_file = '../data/path_x7.pkl'
# path7_y_file = '../data/path_y7.pkl'
# path7_z_file = '../data/path_z7.pkl'
# time7_file = '../data/path_time7.pkl'

# with open(time7_file, 'rb') as fp:
#     time7 = pickle.load(fp)

# with open(path7_x_file, 'rb') as fp:
#     path7_x = pickle.load(fp)

# with open(path7_y_file, 'rb') as fp:
#     path7_y = pickle.load(fp)

# with open(path7_z_file, 'rb') as fp:
#     path7_z = pickle.load(fp)






plt.figure()
font_size = 15
ax = plt.axes(projection='3d')
ax.plot3D(path1_x, path1_y, path1_z, label = 'UAV1')
ax.plot3D(path2_x, path2_y, path2_z, label = 'UAV2')
ax.plot3D(path3_x, path3_y, path3_z, label = 'UAV3')
ax.plot3D(path4_x, path4_y, path4_z, label = 'UAV4')
# ax.plot3D(path5_x, path5_y, path5_z, label = 'UAV5')
# ax.plot3D(path6_x, path6_y, path6_z, label = 'UAV6')
# ax.plot3D(path7_x, path7_y, path7_z, label = 'UAV7')

ax.set_xlabel('X (m)', fontsize=font_size)
ax.set_ylabel('Y (m)', fontsize=font_size)
ax.set_zlabel('Z (m)', fontsize=font_size)
#plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax.legend(fontsize=font_size)
# ax.set_xticks(fontsize=font_size)
# ax.set_yticks(fontsize=font_size)
# ax.set_zticks(fontsize=font_size)
plt.show()
