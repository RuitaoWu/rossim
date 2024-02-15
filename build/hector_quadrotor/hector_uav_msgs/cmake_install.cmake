# Install script for directory: /home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/jxie/rossim/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs/msg" TYPE FILE FILES
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/Altimeter.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/AttitudeCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/Compass.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/ControllerState.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/HeadingCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/HeightCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/MotorCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/MotorPWM.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/MotorStatus.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/PositionXYCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/RawImu.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/RawMagnetic.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/RawRC.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/RC.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/RuddersCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/ServoCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/Supply.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/ThrustCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/VelocityXYCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/VelocityZCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/YawrateCommand.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/Task.msg"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/msg/FinishTime.msg"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs/srv" TYPE FILE FILES "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/srv/EnableMotors.srv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs/action" TYPE FILE FILES
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/action/Pose.action"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/action/Landing.action"
    "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/action/Takeoff.action"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs/msg" TYPE FILE FILES
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/PoseAction.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/PoseActionGoal.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/PoseActionResult.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/PoseActionFeedback.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/PoseGoal.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/PoseResult.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/PoseFeedback.msg"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs/msg" TYPE FILE FILES
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/LandingAction.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/LandingActionGoal.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/LandingActionResult.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/LandingActionFeedback.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/LandingGoal.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/LandingResult.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/LandingFeedback.msg"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs/msg" TYPE FILE FILES
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/TakeoffAction.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/TakeoffActionGoal.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/TakeoffActionResult.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/TakeoffActionFeedback.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/TakeoffGoal.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/TakeoffResult.msg"
    "/home/jxie/rossim/devel/share/hector_uav_msgs/msg/TakeoffFeedback.msg"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs/cmake" TYPE FILE FILES "/home/jxie/rossim/build/hector_quadrotor/hector_uav_msgs/catkin_generated/installspace/hector_uav_msgs-msg-paths.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/jxie/rossim/devel/include/hector_uav_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/jxie/rossim/devel/share/roseus/ros/hector_uav_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/jxie/rossim/devel/share/common-lisp/ros/hector_uav_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/jxie/rossim/devel/share/gennodejs/ros/hector_uav_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/jxie/rossim/devel/lib/python3/dist-packages/hector_uav_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/jxie/rossim/devel/lib/python3/dist-packages/hector_uav_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/jxie/rossim/build/hector_quadrotor/hector_uav_msgs/catkin_generated/installspace/hector_uav_msgs.pc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs/cmake" TYPE FILE FILES "/home/jxie/rossim/build/hector_quadrotor/hector_uav_msgs/catkin_generated/installspace/hector_uav_msgs-msg-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs/cmake" TYPE FILE FILES
    "/home/jxie/rossim/build/hector_quadrotor/hector_uav_msgs/catkin_generated/installspace/hector_uav_msgsConfig.cmake"
    "/home/jxie/rossim/build/hector_quadrotor/hector_uav_msgs/catkin_generated/installspace/hector_uav_msgsConfig-version.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/hector_uav_msgs" TYPE FILE FILES "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/hector_uav_msgs" TYPE DIRECTORY FILES "/home/jxie/rossim/src/hector_quadrotor/hector_uav_msgs/include/hector_uav_msgs/")
endif()

