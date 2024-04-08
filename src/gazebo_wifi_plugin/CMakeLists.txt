cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
project(gazebo_wifi_plugin)

find_package(gazebo REQUIRED)
find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs)
catkin_package()

include_directories(${catkin_INCLUDE_DIRS})
include_directories(${GAZEBO_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})
list(APPEND CMAKE_CXX_FLAGS "${GAZEBO_CXX_FLAGS}")

add_library(wifirouter SHARED WifiRouterPlugin.cc)
target_link_libraries(wifirouter ${GAZEBO_libraries})

add_library(wifireceiver SHARED WifiReceiverPlugin.cc)
target_link_libraries(wifireceiver ${GAZEBO_libraries})
