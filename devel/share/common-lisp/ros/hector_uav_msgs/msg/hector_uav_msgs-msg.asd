
(cl:in-package :asdf)

(defsystem "hector_uav_msgs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :actionlib_msgs-msg
               :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Altimeter" :depends-on ("_package_Altimeter"))
    (:file "_package_Altimeter" :depends-on ("_package"))
    (:file "AttitudeCommand" :depends-on ("_package_AttitudeCommand"))
    (:file "_package_AttitudeCommand" :depends-on ("_package"))
    (:file "Compass" :depends-on ("_package_Compass"))
    (:file "_package_Compass" :depends-on ("_package"))
    (:file "ControllerState" :depends-on ("_package_ControllerState"))
    (:file "_package_ControllerState" :depends-on ("_package"))
    (:file "HeadingCommand" :depends-on ("_package_HeadingCommand"))
    (:file "_package_HeadingCommand" :depends-on ("_package"))
    (:file "HeightCommand" :depends-on ("_package_HeightCommand"))
    (:file "_package_HeightCommand" :depends-on ("_package"))
    (:file "LandingAction" :depends-on ("_package_LandingAction"))
    (:file "_package_LandingAction" :depends-on ("_package"))
    (:file "LandingActionFeedback" :depends-on ("_package_LandingActionFeedback"))
    (:file "_package_LandingActionFeedback" :depends-on ("_package"))
    (:file "LandingActionGoal" :depends-on ("_package_LandingActionGoal"))
    (:file "_package_LandingActionGoal" :depends-on ("_package"))
    (:file "LandingActionResult" :depends-on ("_package_LandingActionResult"))
    (:file "_package_LandingActionResult" :depends-on ("_package"))
    (:file "LandingFeedback" :depends-on ("_package_LandingFeedback"))
    (:file "_package_LandingFeedback" :depends-on ("_package"))
    (:file "LandingGoal" :depends-on ("_package_LandingGoal"))
    (:file "_package_LandingGoal" :depends-on ("_package"))
    (:file "LandingResult" :depends-on ("_package_LandingResult"))
    (:file "_package_LandingResult" :depends-on ("_package"))
    (:file "MotorCommand" :depends-on ("_package_MotorCommand"))
    (:file "_package_MotorCommand" :depends-on ("_package"))
    (:file "MotorPWM" :depends-on ("_package_MotorPWM"))
    (:file "_package_MotorPWM" :depends-on ("_package"))
    (:file "MotorStatus" :depends-on ("_package_MotorStatus"))
    (:file "_package_MotorStatus" :depends-on ("_package"))
    (:file "PoseAction" :depends-on ("_package_PoseAction"))
    (:file "_package_PoseAction" :depends-on ("_package"))
    (:file "PoseActionFeedback" :depends-on ("_package_PoseActionFeedback"))
    (:file "_package_PoseActionFeedback" :depends-on ("_package"))
    (:file "PoseActionGoal" :depends-on ("_package_PoseActionGoal"))
    (:file "_package_PoseActionGoal" :depends-on ("_package"))
    (:file "PoseActionResult" :depends-on ("_package_PoseActionResult"))
    (:file "_package_PoseActionResult" :depends-on ("_package"))
    (:file "PoseFeedback" :depends-on ("_package_PoseFeedback"))
    (:file "_package_PoseFeedback" :depends-on ("_package"))
    (:file "PoseGoal" :depends-on ("_package_PoseGoal"))
    (:file "_package_PoseGoal" :depends-on ("_package"))
    (:file "PoseResult" :depends-on ("_package_PoseResult"))
    (:file "_package_PoseResult" :depends-on ("_package"))
    (:file "PositionXYCommand" :depends-on ("_package_PositionXYCommand"))
    (:file "_package_PositionXYCommand" :depends-on ("_package"))
    (:file "RC" :depends-on ("_package_RC"))
    (:file "_package_RC" :depends-on ("_package"))
    (:file "RawImu" :depends-on ("_package_RawImu"))
    (:file "_package_RawImu" :depends-on ("_package"))
    (:file "RawMagnetic" :depends-on ("_package_RawMagnetic"))
    (:file "_package_RawMagnetic" :depends-on ("_package"))
    (:file "RawRC" :depends-on ("_package_RawRC"))
    (:file "_package_RawRC" :depends-on ("_package"))
    (:file "RuddersCommand" :depends-on ("_package_RuddersCommand"))
    (:file "_package_RuddersCommand" :depends-on ("_package"))
    (:file "ServoCommand" :depends-on ("_package_ServoCommand"))
    (:file "_package_ServoCommand" :depends-on ("_package"))
    (:file "Supply" :depends-on ("_package_Supply"))
    (:file "_package_Supply" :depends-on ("_package"))
    (:file "TakeoffAction" :depends-on ("_package_TakeoffAction"))
    (:file "_package_TakeoffAction" :depends-on ("_package"))
    (:file "TakeoffActionFeedback" :depends-on ("_package_TakeoffActionFeedback"))
    (:file "_package_TakeoffActionFeedback" :depends-on ("_package"))
    (:file "TakeoffActionGoal" :depends-on ("_package_TakeoffActionGoal"))
    (:file "_package_TakeoffActionGoal" :depends-on ("_package"))
    (:file "TakeoffActionResult" :depends-on ("_package_TakeoffActionResult"))
    (:file "_package_TakeoffActionResult" :depends-on ("_package"))
    (:file "TakeoffFeedback" :depends-on ("_package_TakeoffFeedback"))
    (:file "_package_TakeoffFeedback" :depends-on ("_package"))
    (:file "TakeoffGoal" :depends-on ("_package_TakeoffGoal"))
    (:file "_package_TakeoffGoal" :depends-on ("_package"))
    (:file "TakeoffResult" :depends-on ("_package_TakeoffResult"))
    (:file "_package_TakeoffResult" :depends-on ("_package"))
    (:file "Task" :depends-on ("_package_Task"))
    (:file "_package_Task" :depends-on ("_package"))
    (:file "ThrustCommand" :depends-on ("_package_ThrustCommand"))
    (:file "_package_ThrustCommand" :depends-on ("_package"))
    (:file "VelocityXYCommand" :depends-on ("_package_VelocityXYCommand"))
    (:file "_package_VelocityXYCommand" :depends-on ("_package"))
    (:file "VelocityZCommand" :depends-on ("_package_VelocityZCommand"))
    (:file "_package_VelocityZCommand" :depends-on ("_package"))
    (:file "YawrateCommand" :depends-on ("_package_YawrateCommand"))
    (:file "_package_YawrateCommand" :depends-on ("_package"))
  ))