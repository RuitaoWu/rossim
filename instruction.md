# clone this repository then deleve build/ , devel/ and .catkin_workspace


# run the following in linux kernel
```
rm -rf build/
rm -rf devel/
rm .catkin_workspace
```

#Install Eigen3 (Ubuntu) if you do not have intall yet

```sudo apt install libeigen3-dev```

#gazebo_plusgins
 
#PS: current version is noetic, if you have different version you need change accordingly

```sudo apt-get install ros-noetic-gazebo-ros-pkgs ros-noetic-gazebo-ros-control```


# geographic_msgs installation

```sudo apt-get install ros-noetic-geographic-msgs```

#tf2-sensor-msgs installation
```sudo apt-get install ros-noetic-tf2-sensor-msgs```

# Could not find a package configuration file provided by "tf2_geometry_msgs"
```sudo apt-get install ros-noetic-tf2-geometry-msgs```


#hector_localization

#PS:this repose is already include hector_localization
#if you did not see you could install from the following: https://github.com/tu-darmstadt-ros-pkg/hector_localization.git

```cd hector_localization```
```catkin_make --source hector_localization```

# missing gazebo
```sudo apt install libgazebo9-dev```

#regarding error message make -j16 -l16

## caused by gazebo_wifi_plugin

if it is not compiler successfully caused by this reason, I have re-clone the source code, then it worked forme

``` 
https://github.com/Lakshadeep/gazebo_wifi_plugin.git
```

## the flag

```
 -j [N], --jobs[=N]          Allow N jobs at once; infinite jobs with no arg.
 -l [N], --load-average[=N], --max-load[=N] Don't start multiple jobs unless load is below N.

```

Personally I do not have soluation nor why it occures, but according to the answer from the following forum it said out of memory, thus you cou rerun catkin_make
https://unix.stackexchange.com/questions/710460/invoking-make-j16-l16-failed

