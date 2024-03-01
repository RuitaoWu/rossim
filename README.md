
<a name="readme-top"></a>



[![Contributors][contributors-shield]](https://github.com/RuitaoWu/rossim/graphs/contributors)
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]](https://github.com/RuitaoWu/rossim/stargazers)
[![LinkedIn][linkedin-shield]](https://www.linkedin.com/in/ruitao-wu)


<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](<img src="images/smile_logo_title.png" alt="smile-logo" width="80" height="80">)



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


<!-- CONTRIBUTING -->
## Contributing  

Ruitao Wu  


<!-- LICENSE -->
## License  
TBA  




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


