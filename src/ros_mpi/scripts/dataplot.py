#! /usr/bin/env python
from cProfile import label
import matplotlib
from matplotlib.lines import lineStyles
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse
from matplotlib.ticker import MaxNLocator
import pickle
from scipy.interpolate import interp1d
from sympy import li
from collections import defaultdict
class PlotGraph:
    def __init__(self,uavid) -> None:
        self.uavid = uavid
    #TODO:
    #optimize the gantt_chart() function
    def gantt_chart(self):

        task_time = []
        task_sch = []
        number_of_uav = 4


        for i in range(1,number_of_uav):
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
    def comm_graph(self):
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_energy.pkl'%self.uavid, 'rb') as file:
            content = pickle.load(file)
        energy,taskId = [],[]
        for x,y in content:
            if y >=0:
                energy.append(x)
                taskId.append(str(y))
        # print(energy)
        plt.scatter(taskId,energy,marker='o',lineStyle='-')
        plt.xlabel('Task ID')
        plt.ylabel('Energy (mJ)')
        # plt.legend()
        # plt.ylim(-min(energy)*2,max(energy)+min(energy))
        plt.title('UAV-%d Single Task Communication Energy Consumption'%self.uavid)
        # plt.show()
        print('uav-%d communication graph saved'%self.uavid)
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-%d-comm-energy.png'%self.uavid)
        plt.close()
    def comp_energy_graph(self):
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_energy.pkl'%self.uavid, 'rb') as file:
            content = pickle.load(file)
        energy,taskid = [],[]
        for x,y in content:
            energy.append(x)
            taskid.append(y)
        plt.plot(taskid,energy,marker='o',lineStyle='-')
        plt.xlabel('Task ID')
        plt.ylabel('Energy (mJ)')
        plt.title('UAV-%d Single Task Computation Energy Consumption'%self.uavid)
        print('uav-%d computation graph saved'%self.uavid)
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-%d-comp-energy.png'%self.uavid)
        plt.close()
    def comp_time(self):
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_time.pkl'%self.uavid, 'rb') as file:
            content = pickle.load(file)
        energy,taskid = [],[]
        for x,y in content:
            energy.append(x)
            taskid.append(y)
        plt.scatter(taskid,taskid,marker='o',lineStyle='-')
        plt.xlabel('Task ID')
        plt.ylabel('Time (second)')
        plt.title('UAV-%d Single Task Computation Time'%self.uavid)
        print('uav-%d time graph saved'%self.uavid)
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-%d-comp-time.png'%self.uavid)
        plt.close()
    def fly_energy(self):
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_fly_energy.pkl'%self.uavid, 'rb') as file:
            content = pickle.load(file)
        energy,taskid = [],[]
        for x,y in content:
            energy.append(x)
            taskid.append(y)
        plt.plot(taskid,energy,marker='v',lineStyle='-')
        plt.xlabel('Task ID')
        plt.ylabel('Energy (mJ)')
        plt.title('UAV-%d Single Fly Energy Consumption'%self.uavid)
        # print(energy)
        print('uav-%d fly graph saved'%self.uavid)
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-%d-fly-energy.png'%self.uavid)
        plt.close()
    def run(self):
         self.comm_graph()
         self.comp_energy_graph()
         self.comp_time()
         self.fly_energy()
# if __name__ == '__main__':
#     # for x in range(1,4):
#     #     plgraph = PlotGraph(x)
#     #     plgraph.run()
#     # plgraph = PlotGraph(3)
#     # plgraph.run()
