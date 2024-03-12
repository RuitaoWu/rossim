
<a name="readme-top"></a>



[![Contributors][contributors-shield]](https://github.com/RuitaoWu/rossim/graphs/contributors)
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]](https://github.com/RuitaoWu/rossim/stargazers)
[![LinkedIn][linkedin-shield]](https://www.linkedin.com/in/ruitao-wu)


<!-- ABOUT THE PROJECT -->
## About The Project

ROS and Gazebo base simulator for UAV-asssted mobile edge computing

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
    - [1. Support Complex 3D World Simulation](#1-support-complex-3d-world-simulation)
    - [2. Random UAV Mobility](#2-random-uav-mobility)
    - [3. Energy Analysis](#3-energy-analysis)
    - [4. Computation and Communication Analysis](#4-computation-and-communication-analysis)
    - [5. Task Scheduling for Heterogeneous Computing](#5-task-scheduling-for-heterogeneous-computing)
    - [6. Gazebo Launch File](#6-gazebo-launch-file) 
- [File Descriptions](#file-descriptions)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

<!-- GETTING STARTED -->
## Getting Started  

Instructions on setting up your project locally.    


### Prerequisites    
  
This is an example of how to list things you need to use the software and how to install them.  
* [Linux Ubuntu 20.04.5 LTS](https://old-releases.ubuntu.com/releases/20.04.5/)
* [ROS-1](https://wiki.ros.org/noetic/Installation/Ubuntu)
* [hector_quadrotor](https://github.com/tu-darmstadt-ros-pkg/hector_quadrotor)
  * This is for the hector_quadrotor model
* [mpi4py](https://mpi4py.readthedocs.io/en/stable/install.html)
  
### Installation

1. Clone this repo to your ROS workstation:
    1. Source your ROS setup file:
        ```bash
        source /your/path/to/setup.sh #other setup files like setup.bash also work
        ```

    2. Set up your workspace:
        ```bash
        mkdir -p ~/your_work_space/src
        cd ~/your_work_space/
        catkin_make
        ```

2. After successfully building, run the following to launch Gazebo world:
    1. Launch Gazebo:
        ```bash
        roslaunch hector_quadrotor_gazebo task.launch
        ```

    2. Open a new terminal and run the following commands to start the simulation:
        ```bash
        cd ~/your/path/to/ros_mpi/scripts
        mpirun -n number_uav python3 master.py
        ```

## Features

This secion is introduce what features are included

### 1. Support Complex 3D World Simulation


- This simulator supports Gazebo for constructing complex environments.
- Users can take advantage of Gazebo's capabilities to create intricate 3D worlds.
- The provided launch file is convenient for users to alter and build multi-UAV scenarios.


### 2. Random UAV Mobility

- Provided random waypoint generator
  - user is able to define an aear which an UAV is random moving within this area


### 3. Energy Analysis

- Include the energy analysis model for communication and computation


### 4. Computation and Communication Analysis

- Computation and communication time analysis

### 5. Task Scheduling for Heterogeneous Computing
- [Heterogeneous Earliest-Finish-Time](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=993206)
- [Improved Predict Earliest Finish Time](https://onlinelibrary.wiley.com/doi/full/10.1002/cpe.3944)
   - [GitHub Implementation](https://github.com/sharma-n/DAG_Scheduling/tree/master) 

### 6. Gazebo Launch File
- User is able to add/remove UAVs by edit the launch file


## File Descriptions
This section provides a brief description of the main files and directories in the project.

- `src/ros_mpi/scripts`: This directory contains all the source code for the project.
- `src/ros_mpi/task_succ`: This directory contains the result of task scheduling.
- `src/pos_controller/data`: This directory contains all the trajectory data for the UAVs.
- `src/pos_controller/scripts`: This directory contains the source code for the UAV controller.
- `src/ros_mpi/scripts/graph`: This is the result graphs of the simulation.
- `src/hector_quadrotor`: This directory contains the model of the UAV which is submoduled from the hector_quadrotor package.
- `hector_quadrotor_gazebo/launch`: This folder contains the launch file for the Gazebo world.
- `hector_uav_msgs/msg`: This folder contains the message file for the UAV.
- **Note:** back slash or forward slash is interchangeable depending on the operating system.

## Configuration
This section provides a brief description of the configuration files in the project.
- `.launch` files: These files are where you can add or remove UAVs. They are located in the `hector_quadrotor_gazebo/launch` directory.
```xml
<?xml version="1.0"?>

<launch>
   <arg name="model" default="$(find hector_quadrotor_description)/urdf/quadrotor.gazebo.xacro" />
    <!-- add two UAVs -->
    <!-- add more UAV to create more group, and give initiaal position  -->
   <group ns="uav1">
     <include file="$(find hector_quadrotor_gazebo)/launch/spawn_quadrotor.launch">
       <arg name="name" value="uav1" />
       <arg name="tf_prefix" value="uav1" />
       <arg name="model" value="$(arg model)" />
       <arg name="x" value="10.0" />
       <arg name="y" value="-1.0" />
     </include>
   </group>

   <group ns="uav2">
     <include file="$(find hector_quadrotor_gazebo)/launch/spawn_quadrotor.launch">
       <arg name="name" value="uav2" />
       <arg name="tf_prefix" value="uav2" />
       <arg name="model" value="$(arg model)" />
       <arg name="x" value="10.0" />
       <arg name="y" value="-1.0" />
     </include>
   </group>

</launch>
```
- `.properties` files: These files are where you can set up parameters and variables for the simulation.
```ini
#.properties file description
[UAV]
#max cpu
max_cpu = 200000001 
#min cpu
min_cpu = 100000001
#ros sleep time
sleep_time = 1 
comm_range = 10

[Task]
#number of total tasks
numberOfTask = 87 
#computing node
computing = 3 
#density
density = 0.8 
#task size range(max, min)
task_size_max = 50000
task_size_min = 40000
#ips: instruction per second
ips_max = 50000
ips_min = 40000
#only two optioin either: Dependent or Independent
task_type = Independent
#define the master uav index start from 1, e.g. if there are 3-uavs the index for each of them are: 1,2,3
master_uav = 2
#maxiteration
maxiter = 5

[Mobile]
numberOfPoints = 5
xMax = 50
xMin = -50
yMax = 50
yMin = -50
# zMin must be greated than 0 since 0 representing the ground
zMin = 1
zMax = 20

[DatarateConfig]
#default datarate configuration setup
#transmission power is 0.5 watt
#noise power is 0.0000000000001
#band width is 5MHz 5000000
#alpha=4.0 which is loss index
noise=0.0000000001
band_width=5000000
transmission_power=0.05
alpha=4.0
```
<!-- CONTRIBUTING -->
## Contributing  

TBD 


<!-- LICENSE -->
## License  
This project is licensed under the [MIT License](https://github.com/RuitaoWu/rossim/blob/main/LICENSE) - see the [LICENSE](https://github.com/RuitaoWu/rossim/blob/main/LICENSE) file for details.




<!-- CONTACT -->
## Contact

Your Name - [@RuitaoWu](https://github.com/RuitaoWu) - rwu9937@sdsu.edu

Project Link: [ROSSIM](https://github.com/RuitaoWu/rossim)





<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
TBA


[contributors-shield]: https://img.shields.io/badge/contributors-green?style=for-the-badge
[forks-shield]: https://img.shields.io/badge/fork-blue?style=for-the-badge
[forks-url]: https://github.com/RuitaoWu/rossim/forks
[stars-shield]: https://img.shields.io/badge/start-green?style=for-the-badge
[linkedin-shield]:https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge

## TODO
- existing issue
  - the graph partition strategy may only working for level-by-level (tree) structure which may ignore dependencies if convert to a spanning tree or MST
- Possible solution: convert to maximum spnning tree
