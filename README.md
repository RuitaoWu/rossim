
<a name="readme-top"></a>

<div align="center">

[![Contributors][contributors-shield]](https://github.com/RuitaoWu/rossim/graphs/contributors)
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]](https://github.com/RuitaoWu/rossim/stargazers)
[![LinkedIn][linkedin-shield]](https://www.linkedin.com/in/ruitao-wu)




<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/RuitaoWu/rossim">
    <img src="images/smile_logo_title.png" alt="smile-logo" width="80" height="80">
  </a> -->

  <h3 align="center">ROSSIM PROJECT DOCUMENTATION</h3>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](<img src="images/smile_logo_title.png" alt="smile-logo" width="80" height="80">)

<!-- 
<p align="right">(<a href="#readme-top">back to top</a>)</p> -->


<p align="right">(<a href="#readme-top">back to top</a>)</p>



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

1. **Clone this repo to your ROS workstation:**
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

2. **After successfully building, run the following to launch Gazebo world:**
    1. Launch Gazebo:
        ```bash
        roslaunch hector_quadrotor_gazebo task.launch
        ```

    2. Open a new terminal and run the following commands to start the simulation:
        ```bash
        cd ~/your/path/to/ros_mpi/scripts
        mpirun -n number_uav python3 master.py
        ```




<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing  

Ruitao Wu  

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License  
TBA  

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@RuitaoWu](https://github.com/RuitaoWu) - rwu9937@sdsu.edu

Project Link: [ROSSIM](https://github.com/RuitaoWu/rossim)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
TBA


<p align="right">(<a href="#readme-top">back to top</a>)</p>


[contributors-shield]: https://img.shields.io/badge/contributors-green?style=for-the-badge
[forks-shield]: https://img.shields.io/badge/fork-blue?style=for-the-badge
[forks-url]: https://github.com/RuitaoWu/rossim/forks
[stars-shield]: https://img.shields.io/badge/start-green?style=for-the-badge
[linkedin-shield]:https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge


