
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

## Configuration
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


