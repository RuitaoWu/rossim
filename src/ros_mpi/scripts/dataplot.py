#! /usr/bin/env python
from cProfile import label
import configparser
import time
from xml.sax.handler import feature_string_interning
import matplotlib
from matplotlib import markers
from matplotlib.lines import lineStyles
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse
from matplotlib.ticker import MaxNLocator
import pickle,math
from scipy.interpolate import interp1d
from sympy import content, li
from collections import defaultdict
from datarate import Datarate
config = configparser.ConfigParser()
config.read('/home/jxie/rossim/src/ros_mpi/scripts/property.properties')
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
        fast,faft = [0]*20,[0]*20
        for x in task_time:
            for y in x:
                fast[y['task_id']] = y['start_time']
                faft[y['task_id']] = y['end_time']
        print(f'final start time { fast}')
        print(f'final end time { faft}')
        print(f'length of time {len(faft)} with makespan {max(faft)}')
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
        # ax.set_xlim(0, max(faft))
        plt.tight_layout()
        # Show the plot
        # plt.grid(axis='x',color='r', linestyle='-', linewidth=2)
        plt.grid(axis='x')
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/gantt_chart.png')
        plt.close()
    def comm_graph(self):
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_energy.pkl'%self.uavid, 'rb') as file:
            content = pickle.load(file)
        energy,taskId = [],[]
        for x,y in content:
            if y >=0:
                energy.append(x)
                taskId.append(str(y))
        # print(energy)
        plt.plot(taskId,energy,marker='o',lineStyle='None')
        plt.autoscale(axis='y')
        plt.xlabel('Task ID')
        plt.ylabel('Energy (mJ)')
        # plt.legend()
        # plt.ylim(-min(energy)*2,max(energy)+min(energy))
        plt.title('UAV-%d Single Task Communication Energy Consumption'%self.uavid)
        # plt.show()
        print('uav-%d communication graph saved'%self.uavid)
        plt.tight_layout()
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-%d-comm-energy.png'%self.uavid)
        plt.close()
    def comp_energy_graph(self):
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_energy.pkl'%self.uavid, 'rb') as file:
            content = pickle.load(file)
        energy,taskid = [],[]
        for x,y in content:
            energy.append(x)
            taskid.append(y)
        plt.plot(taskid,energy,marker='o',lineStyle='None')
        plt.autoscale(axis='y')
        plt.xlabel('Task ID')
        plt.ylabel('Energy (mJ)')
        plt.title('UAV-%d Single Task Computation Energy Consumption'%self.uavid)
        print('uav-%d computation graph saved'%self.uavid)
        plt.tight_layout()
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-%d-comp-energy.png'%self.uavid)
        plt.close()
    def comp_time(self):
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comp_time.pkl'%self.uavid, 'rb') as file:
            content = pickle.load(file)
        energy,taskid = [],[]
        for x,y in content:
            energy.append(x * 1000) #convert to Millisecond MS
            taskid.append(y)
        # print(f'energy {energy}')
        plt.plot(taskid,energy,marker='o',lineStyle='None')
        plt.xlabel('Task ID')
        plt.ylabel('Time (Millisecond)')
        plt.title('UAV-%d Single Task Computation Time'%self.uavid)
        # plt.autoscale(axis='y')
        print('uav-%d time graph saved'%self.uavid)
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-%d-comp-time.png'%self.uavid)
        plt.close()
    def fly_energy(self):
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_fly_energy.pkl'%self.uavid, 'rb') as file:
            content = pickle.load(file)
        energy,taskid = [],[]
        for x,y in content:
            if y >= 0:
                energy.append(x)
                taskid.append(str(y))
        # print(content)
        plt.plot(taskid,energy,marker='v',lineStyle='None')
        plt.xlabel('Time')
        plt.ylabel('Energy (mJ)')
        plt.title('UAV-%d Single Fly Energy Consumption'%self.uavid)
        # plt.autoscale(axis='y')
        # print(energy)
        print('uav-%d fly graph saved'%self.uavid)
        plt.tight_layout()
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-%d-fly-energy.png'%self.uavid)
        plt.close()
    def trajectory(self):
        num_uavs = int(config.get('Task','computing'))
        plt.figure()
        font_size = 24
        ax = plt.axes(projection='3d')
        min_value = float('inf')
        for i in range(1, num_uavs+1):
            time_file = '/home/jxie/rossim/src/pos_controller/data/path_time%d.pkl' %i
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
        linestyles = ['-', '-.', ':', '--', '--', '--', '--', '--', '--', '--', '--']
        font_size = 18

        for i in range(1, num_uavs+1):

            path_x_file = '/home/jxie/rossim/src/pos_controller/data/path_x%d.pkl' %i
            path_y_file = '/home/jxie/rossim/src/pos_controller/data/path_y%d.pkl' %i
            path_z_file = '/home/jxie/rossim/src/pos_controller/data/path_z%d.pkl' %i
            time_file = '/home/jxie/rossim/src/pos_controller/data/path_time%d.pkl' %i
            with open(time_file, 'rb') as fp:
                time = pickle.load(fp)

            with open(path_x_file, 'rb') as fp:
                path_x = pickle.load(fp)

            interp_funcx = interp1d(time, path_x,bounds_error=False)
            new_x = interp_funcx(new_t)

            with open(path_y_file, 'rb') as fp:
                path_y = pickle.load(fp)
            # print(len(time),len(path_y),len(path_x))
            interp_funcy = interp1d(time, path_y,bounds_error=False)

            new_y = interp_funcy(new_t)

            with open(path_z_file, 'rb') as fp:
                path_z = pickle.load(fp)
            interp_funcz = interp1d(time, path_z,bounds_error=False)
            new_z = interp_funcz(new_t)
            #print('path x', path_x[-1], 'path y', path_y[-1], 'path_z', path_z[-1])
            paths_x.append(new_x)
            paths_y.append(new_y)
            paths_z.append(new_z)
            if i == 1:
                ax.plot3D(path_x, path_y, path_z, linestyle=linestyles[i-1], linewidth = 3.5, label = 'Master')
            else:
                ax.plot3D(path_x, path_y, path_z, linestyle=linestyles[i-1], linewidth = 3.5, label = 'Worker %d' %(i-1))
        ax.set_xlabel('X (m)', fontsize=16)
        ax.set_ylabel('Y (m)', fontsize=16)
        ax.set_zlabel('Z (m)', fontsize=16)
        plt.subplots_adjust(bottom=0.15, left=0.2, top=0.95, wspace=0, hspace=0)
        ax.legend(fontsize=14,loc='upper left',framealpha=0.5)
        # plt.savefig('ros_path')
        ax.tick_params(labelsize=14)
        plt.tight_layout()
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-trajectory.png')
        plt.close()
    def dataRateGraph(self):
        config = configparser.ConfigParser()
        config.read('/home/jxie/rossim/src/ros_mpi/scripts/property.properties')
        # noise=0.0000000000001,band_width=5000000 , transmission_power=0.5,alpha=4.0
        # density = float(config.get('Task','density'))
        test= Datarate(noise=float(config.get('DatarateConfig','noise')),
                                 band_width=float(config.get('DatarateConfig','band_width')),
                                 transmission_power=float(config.get('DatarateConfig','transmission_power')),
                                 alpha=float(config.get('DatarateConfig','alpha')))
        
        m_x_file = '/home/jxie/rossim/src/pos_controller/data/path_x%d.pkl' %1
        m_y_file = '/home/jxie/rossim/src/pos_controller/data/path_y%d.pkl' %1
        m_z_file = '/home/jxie/rossim/src/pos_controller/data/path_z%d.pkl' %1
        time_file = '/home/jxie/rossim/src/pos_controller/data/path_time%d.pkl' %1
        with open(time_file, 'rb') as fp:
            time_m = pickle.load(fp)
        with open(m_x_file, 'rb') as fp:
            m_x = pickle.load(fp)

        with open(m_x_file, 'rb') as fp:
            m_y = pickle.load(fp)

        with open(m_x_file, 'rb') as fp:
            m_z = pickle.load(fp)

        _distance = []
        for i in range(2, 4):
            path_x_file = '/home/jxie/rossim/src/pos_controller/data/path_x%d.pkl' %i
            path_y_file = '/home/jxie/rossim/src/pos_controller/data/path_y%d.pkl' %i
            path_z_file = '/home/jxie/rossim/src/pos_controller/data/path_z%d.pkl' %i
            with open(path_x_file, 'rb') as fp:
                temp_x = pickle.load(fp)

            with open(path_y_file, 'rb') as fp:
                temp_y = pickle.load(fp)

            with open(path_z_file, 'rb') as fp:
                temp_z = pickle.load(fp)
            temp_d = []
            for x,y,z,x1,y1,z1 in zip(m_x,m_y,m_z,temp_x,temp_y,temp_z):
                temp_d.append(math.sqrt((x - x1)**2 + (y - y1)**2 + (z - z1)**2))
            _distance.append(temp_d)
        bandwidth = []
        for i in _distance:
            temp = []
            for j in i:
                temp.append(test.data_rate(j)/1000000)
            bandwidth.append(temp)
        # plt.ylim((min(bandwidth),max(bandwidth)))
        for x in bandwidth:
            plt.plot(time_m[:len(x)],x,lineStyle='--',label='Master to %d'%(bandwidth.index(x)+1))
        
        plt.ylabel("Data Rate (Mbps)")
        plt.xlabel("Time (seconds)")
        plt.legend()
        print('datarate saved')
        plt.tight_layout()
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-datarate.png')
        plt.close()
    def comm_time(self):
        with open('/home/jxie/rossim/src/ros_mpi/data/uav%d_comm_time.pkl'%self.uavid, 'rb') as file:
            content = pickle.load(file)
        plt.plot([content.index(x) for x in content],content,marker='v',lineStyle='--')
        # plt.autoscale(axis='y')
        plt.tight_layout()
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/uav-%d-comm-time.png'%self.uavid)
        plt.close()
    def task_analysis(self):
        # succ_rate,iter_num = [],[]
        # for i in range(0,5):
        #     with open('/home/jxie/rossim/src/ros_mpi/task_succ/completed_%d_iter_%d.pkl'%(self.uavid,i),'rb') as file:
        #         completed_tasks = pickle.load(file)
        #     with open('/home/jxie/rossim/src/ros_mpi/task_succ/incompleted_%d_iter_%d.pkl'%(self.uavid,i),'rb') as file:
        #         incomplete_tasks = pickle.load(file)
        #     completed_x, _ = zip(*completed_tasks)
        #     incomplete_x, _= zip(*incomplete_tasks)
        #     succ_rate.append(float((len(completed_x)/(len(completed_x)+len(incomplete_x)))) *100)

        #     print(len(completed_x)/(len(completed_x)+len(incomplete_x)))
        #     iter_num.append(str(i))
        # plt.plot(iter_num,succ_rate, color='b',marker='^',linestyle='--')

        # plt.xlabel('Number of Iteration')
        # plt.ylabel('Success Rate (%)')
        # plt.title('Task Success Rate')
        # # plt.legend()
        
        # plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/task_succ_rate.png')
        # plt.close()
        completed_total = []
        incomplete_total = []
        complete_rate = []
        incomplete_rate = []
        iter_num = []

        for i in range(0, 5):
            # with open('/home/jxie/rossim/src/ros_mpi/task_succ/completed_%d_iter_%d.pkl' % (self.uavid, i), 'rb') as file:
            with open('/home/jxie/rossim/src/ros_mpi/task_succ/completed_%d_iter_%d.pkl' % (3, i), 'rb') as file:
                completed_tasks = pickle.load(file)
                completed_x, _ = zip(*completed_tasks)
                completed_total.append(len(completed_x))

            # with open('/home/jxie/rossim/src/ros_mpi/task_succ/incompleted_%d_iter_%d.pkl' % (self.uavid, i), 'rb') as file:
            with open('/home/jxie/rossim/src/ros_mpi/task_succ/incompleted_%d_iter_%d.pkl' % (3, i), 'rb') as file:
                # incomplete_tasks = pickle.load(file)
                # incomplete_x, _ = zip(*incomplete_tasks)
                # incomplete_total.append(len(incomplete_x))
                incomplete_tasks = pickle.load(file)
                if incomplete_tasks:  # Check if incomplete_tasks is not empty
                    incomplete_x, _ = zip(*incomplete_tasks)
                    incomplete_total.append(len(incomplete_x))
                else:
                    incomplete_x = []
                    incomplete_total.append(0)

            total_tasks = len(completed_x) + len(incomplete_x)
            complete_rate.append((len(completed_x) / total_tasks) * 100)
            incomplete_rate.append((len(incomplete_x) / total_tasks) * 100)
            iter_num.append(str(i))
        # First subplot: Completed, Incomplete, and Total Tasks
        plt.figure(figsize=(12, 6))

        plt.subplot(2, 1, 1)
        plt.plot(iter_num, completed_total, label='Completed', marker='o',linestyle='-.')
        plt.plot(iter_num, incomplete_total, label='Incomplete', marker='x',linestyle='--')
        plt.plot(iter_num, [completed_total[i] + incomplete_total[i] for i in range(len(iter_num))], label='Total', marker='s',linestyle=':')
        plt.xlabel('Number of Iteration')
        plt.ylabel('Number of Tasks')
        plt.title('Task Completion Analysis')
        plt.legend()

        # Second subplot: Complete Rate and Incomplete Rate
        plt.subplot(2, 1, 2)
        plt.plot(iter_num, complete_rate, label='Complete Rate', marker='o',linestyle='-.')
        plt.plot(iter_num, incomplete_rate, label='Incomplete Rate', marker='x',linestyle='--')
        plt.xlabel('Number of Iteration')
        plt.ylabel('Rate (%)')
        plt.title('Task Completion Rate Analysis')
        plt.legend()

        plt.tight_layout()
        # plt.show()
        plt.savefig('/home/jxie/rossim/src/ros_mpi/scripts/graph/task_succ_rate.png')
        plt.close()

    def run(self):
        self.comm_graph()
        self.comp_energy_graph()
        self.comp_time()
        self.fly_energy()
        self.trajectory()
        self.dataRateGraph()
    
    
if __name__ == '__main__':

    data=[]
    for i in range(5):
        with open('/home/jxie/rossim/src/ros_mpi/task_succ/capacity3_iter_%d.pkl'%i, 'rb') as file:
            content = pickle.load(file)
        data.append(content)
        # plt.plot([x for x in content],[y for y in range(len(content))],label='Iteration%d'%i, marker=i)
    dt = [ele for sub in data for ele in sub]
    plt.plot([y for y in range(len(dt))],[x for x in dt],label='Iteration%d'%i, marker=i)
    plt.xlabel('Iteration Number')
    plt.ylabel('Capacity Cost (Unit Bits)')
    plt.title('Capacity Cost vs. Iteration Number')
    plt.legend()
    plt.grid(True)
    plt.show()
    # with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.pkl'%2, 'rb') as file:
    #     content = pickle.load(file)
    # print(f'content { len(content)}')
    # with open('/home/jxie/rossim/src/ros_mpi/data/uav%d.pkl'%3, 'rb') as file:
    #     content = pickle.load(file)
    # print(f'content { len(content)}')

    for x in range(1,3):
        plgraph = PlotGraph(x)
        print('current uav%d'%x)
        # plgraph.comm_time()
    
        plgraph.run()
    # plgraph = PlotGraph(1)
    # plgraph.gantt_chart()   
    # plgraph = PlotGraph(3)

    plgraph.task_analysis()
    # plgraph.trajectory()
