#! /usr/bin/env python
from cProfile import label
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse
from matplotlib.ticker import MaxNLocator
import pickle
from scipy.interpolate import interp1d
from sympy import li

# num_uavs = 3
# rssi_file_name = '/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/data/comp_rssi.pkl'
# with open(rssi_file_name, 'rb') as fp:
#     rssi_data = pickle.load(fp)

# plt.figure()
# font_size = 24
# ax = plt.axes(projection='3d')


# # new_t = 1
# min_value = float('inf')
# for i in range(1, num_uavs+1):
#     time_file = '/home/jxie/Workspace/hzhang3986/nac_sim/src/pos_controller/data/path_time%d.pkl' %i
#     with open(time_file, 'rb') as fp:
#         time = pickle.load(fp)
#         # print('min time', np.min(time))
#         value = np.max(time)
#         # print('time', value)

#     min_value = min(min_value, value)

# new_t = np.arange(1, min_value, 0.1)
# length = len(new_t)

# # print('min value', min_value)
# paths_x = []
# paths_y = []
# paths_z = []
# linestyles = ['-', '-.', ':', '--', '--', '--', '--', '--', '--', '--', '--']
# font_size = 18

# for i in range(1, num_uavs+1):
#   #/home/jxie/Workspace/hzhang3986/nac_sim/src/pos_controller/data
#     path_x_file = '/home/jxie/Workspace/hzhang3986/nac_sim/src/pos_controller/data/path_x%d.pkl' %i
#     path_y_file = '/home/jxie/Workspace/hzhang3986/nac_sim/src/pos_controller/data/path_y%d.pkl' %i
#     path_z_file = '/home/jxie/Workspace/hzhang3986/nac_sim/src/pos_controller/data/path_z%d.pkl' %i
#     time_file = '/home/jxie/Workspace/hzhang3986/nac_sim/src/pos_controller/data/path_time%d.pkl' %i
#     with open(time_file, 'rb') as fp:
#         time = pickle.load(fp)

#     with open(path_x_file, 'rb') as fp:
#         path_x = pickle.load(fp)

#     interp_funcx = interp1d(time, path_x,bounds_error=False)
#     new_x = interp_funcx(new_t)

#     with open(path_y_file, 'rb') as fp:
#         path_y = pickle.load(fp)
#     # print(len(time),len(path_y),len(path_x))
#     interp_funcy = interp1d(time, path_y,bounds_error=False)

#     new_y = interp_funcy(new_t)

#     with open(path_z_file, 'rb') as fp:
#         path_z = pickle.load(fp)
#     interp_funcz = interp1d(time, path_z,bounds_error=False)
#     new_z = interp_funcz(new_t)
#     #print('path x', path_x[-1], 'path y', path_y[-1], 'path_z', path_z[-1])
#     paths_x.append(new_x)
#     paths_y.append(new_y)
#     paths_z.append(new_z)
#     #ax.plot3D(new_x, new_y, new_z, label = 'UAV%d' %i)
#     if i == 1:
#         ax.plot3D(path_x, path_y, path_z, linestyle=linestyles[i-1], linewidth = 3.5, label = 'Master')
#     else:
#         ax.plot3D(path_x, path_y, path_z, linestyle=linestyles[i-1], linewidth = 3.5, label = 'Worker %d' %(i-1))
# ax.set_xlabel('X (m)', fontsize=16)
# ax.set_ylabel('Y (m)', fontsize=16)
# ax.set_zlabel('Z (m)', fontsize=16)
# # plt.ylim(0,40)
# plt.subplots_adjust(bottom=0.15, left=0.2, top=0.95, wspace=0, hspace=0)
# ax.legend(fontsize=14,loc='upper left',framealpha=0.5)

# ax.tick_params(labelsize=14)
# plt.show()

# # with open('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/scripts/datarate/datarate_one.pkl','rb') as f:
# #     data = pickle.load(f)
# # with open('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/scripts/datarate/datarate_two.pkl','rb') as f1:
# #     data2 = pickle.load(f1)

# with open('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/scripts/commtime/commtime_one.pkl','rb') as f:
#     data = pickle.load(f)
# with open('/home/jxie/Workspace/hzhang3986/nac_sim/src/ros_mpi/scripts/commtime/commtime_two.pkl','rb') as f1:
#     data2 = pickle.load(f1)

# plt.figure(figsize=(10,6))
# plt.plot(data,label='data one')
# plt.plot(data2,label='data one')
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.title('Data')
# plt.show()




# import matplotlib.pyplot as plt





# new_schedule_list = [[1, 8], [3, 2, 7, 9], [0, 4, 5, 6]]
# fast,faft = [-1]*10,[-1]*10
# # Your provided data
# tasks_data = [
#     [{'task_id': 0, 'start_time': 0.711, 'end_time': 9.711, 'duration': 9}, {'task_id': 4, 'start_time': 19.99, 'end_time': 29.99, 'duration': 10}, {'task_id': 5, 'start_time': 29.99, 'end_time': 38.989999999999995, 'duration': 9}, {'task_id': 6, 'start_time': 46.431, 'end_time': 57.431, 'duration': 11}],
#     [{'task_id': 1, 'start_time': 2.794, 'end_time': 15.794, 'duration': 13}, {'task_id': 8, 'start_time': 26.316, 'end_time': 44.316, 'duration': 18}],
#     [{'task_id': 3, 'start_time': 17.904, 'end_time': 25.904, 'duration': 8}, {'task_id': 2, 'start_time': 25.904, 'end_time': 38.903999999999996, 'duration': 13}, {'task_id': 7, 'start_time': 48.528, 'end_time': 59.528, 'duration': 11}, {'task_id': 9, 'start_time': 59.528, 'end_time': 66.52799999999999, 'duration': 7}]
# ]

# for x in tasks_data:
#     for y in x:
#         fast[y['task_id']] = y['start_time']
#         faft[y['task_id']] = y['end_time']



# task_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k','black','white','gray']

# # Create a figure and axis
# fig, ax = plt.subplots()

# # Iterate through task_schedule_list and plot the bars
# for i, task_indices in enumerate(new_schedule_list):
#     for task_index in task_indices:
#         start_time = fast[task_index]
#         end_time = faft[task_index]
#         task_name = f'Task {task_index+1}'  # Task number label
#         w = end_time - start_time
#         ax.barh(i, width=w, left=start_time, height=0.6,align='center', edgecolor='black', color='white', alpha=0.95)
#         ax.text(start_time + (end_time - start_time) / 2, i, task_name, ha='center', va='center', color=task_colors[(i)], fontweight='bold', fontsize=18, alpha=0.75)

# # Set labels and title
# ax.set_xlabel('Time', fontsize=20)
# ax.set_ylabel('Tasks', fontsize=20)
# ax.set_title('Gantt Chart', fontsize=20)

# # Set the y-axis ticks and labels
# ax.set_yticks(range(3))
# ax.set_yticklabels([f'Schedule {i+1}' for i in range(3)])

# # Set the x-axis range
# ax.set_xlim(0, max(faft) + 5)

# # Show the plot
# # plt.grid(axis='x',color='r', linestyle='-', linewidth=2)
# plt.grid(axis='x')
# plt.show()
# with open('/home/jxie/rossim/src/ros_mpi/data/task_ast_master.pkl', 'rb') as file:
#     # Read the entire content of the file into a string
#     content = pickle.load(file)

from collections import defaultdict
task_time = []
task_sch = []
number_of_uav = 3


for i in range(0,number_of_uav):
    temp =[]
    sch = []
    with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.pkl'%i, 'rb') as file:
        content = pickle.load(file)
    for j in content:
        temp.append({'task_id': j.task_idx, 'start_time': j.st, 'end_time': j.et, 'duration': j.et - j.st})
        sch.append(j.task_idx)
    task_time.append(temp)
    task_sch.append(sch)

task_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k','black','white','gray']

# Create a figure and axis
fig, ax = plt.subplots()
fast,faft = [-1]*10,[-1]*10
for x in task_time:
    for y in x:
        fast[y['task_id']] = y['start_time']
        faft[y['task_id']] = y['end_time']

# Iterate through task_schedule_list and plot the bars
for i, task_indices in enumerate(task_sch):
    for task_index in task_indices:
        start_time = fast[task_index]
        end_time = faft[task_index]
        task_name = f'Task {task_index+1}'  # Task number label
        w = end_time - start_time
        ax.barh(i, width=w, left=start_time, height=0.6,align='center', edgecolor='black', color='white', alpha=0.95)
        ax.text(start_time + (end_time - start_time) / 2, i, task_name, ha='center', va='center', color=task_colors[(i)], fontweight='bold', fontsize=18, alpha=0.75)

# Set labels and title
ax.set_xlabel('Time', fontsize=20)
ax.set_ylabel('Tasks', fontsize=20)
ax.set_title('Gantt Chart', fontsize=20)

# Set the y-axis ticks and labels
ax.set_yticks(range(3))
ax.set_yticklabels([f'Schedule {i+1}' for i in range(3)])

# Set the x-axis range
ax.set_xlim(0, max(faft))

# Show the plot
# plt.grid(axis='x',color='r', linestyle='-', linewidth=2)
plt.grid(axis='x')
plt.show()