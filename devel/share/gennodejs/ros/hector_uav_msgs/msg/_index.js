
"use strict";

let PositionXYCommand = require('./PositionXYCommand.js');
let HeadingCommand = require('./HeadingCommand.js');
let ThrustCommand = require('./ThrustCommand.js');
let ServoCommand = require('./ServoCommand.js');
let VelocityZCommand = require('./VelocityZCommand.js');
let MotorCommand = require('./MotorCommand.js');
let Compass = require('./Compass.js');
let MotorPWM = require('./MotorPWM.js');
let Task = require('./Task.js');
let RawImu = require('./RawImu.js');
let AttitudeCommand = require('./AttitudeCommand.js');
let Supply = require('./Supply.js');
let RC = require('./RC.js');
let RawRC = require('./RawRC.js');
let Altimeter = require('./Altimeter.js');
let YawrateCommand = require('./YawrateCommand.js');
let HeightCommand = require('./HeightCommand.js');
let ControllerState = require('./ControllerState.js');
let VelocityXYCommand = require('./VelocityXYCommand.js');
let FinishTime = require('./FinishTime.js');
let RawMagnetic = require('./RawMagnetic.js');
let RuddersCommand = require('./RuddersCommand.js');
let MotorStatus = require('./MotorStatus.js');
let TakeoffGoal = require('./TakeoffGoal.js');
let LandingActionGoal = require('./LandingActionGoal.js');
let TakeoffActionResult = require('./TakeoffActionResult.js');
let TakeoffFeedback = require('./TakeoffFeedback.js');
let TakeoffActionFeedback = require('./TakeoffActionFeedback.js');
let PoseActionFeedback = require('./PoseActionFeedback.js');
let LandingGoal = require('./LandingGoal.js');
let PoseFeedback = require('./PoseFeedback.js');
let LandingActionFeedback = require('./LandingActionFeedback.js');
let LandingFeedback = require('./LandingFeedback.js');
let LandingAction = require('./LandingAction.js');
let LandingActionResult = require('./LandingActionResult.js');
let TakeoffActionGoal = require('./TakeoffActionGoal.js');
let LandingResult = require('./LandingResult.js');
let PoseGoal = require('./PoseGoal.js');
let PoseActionGoal = require('./PoseActionGoal.js');
let PoseActionResult = require('./PoseActionResult.js');
let PoseResult = require('./PoseResult.js');
let PoseAction = require('./PoseAction.js');
let TakeoffAction = require('./TakeoffAction.js');
let TakeoffResult = require('./TakeoffResult.js');

module.exports = {
  PositionXYCommand: PositionXYCommand,
  HeadingCommand: HeadingCommand,
  ThrustCommand: ThrustCommand,
  ServoCommand: ServoCommand,
  VelocityZCommand: VelocityZCommand,
  MotorCommand: MotorCommand,
  Compass: Compass,
  MotorPWM: MotorPWM,
  Task: Task,
  RawImu: RawImu,
  AttitudeCommand: AttitudeCommand,
  Supply: Supply,
  RC: RC,
  RawRC: RawRC,
  Altimeter: Altimeter,
  YawrateCommand: YawrateCommand,
  HeightCommand: HeightCommand,
  ControllerState: ControllerState,
  VelocityXYCommand: VelocityXYCommand,
  FinishTime: FinishTime,
  RawMagnetic: RawMagnetic,
  RuddersCommand: RuddersCommand,
  MotorStatus: MotorStatus,
  TakeoffGoal: TakeoffGoal,
  LandingActionGoal: LandingActionGoal,
  TakeoffActionResult: TakeoffActionResult,
  TakeoffFeedback: TakeoffFeedback,
  TakeoffActionFeedback: TakeoffActionFeedback,
  PoseActionFeedback: PoseActionFeedback,
  LandingGoal: LandingGoal,
  PoseFeedback: PoseFeedback,
  LandingActionFeedback: LandingActionFeedback,
  LandingFeedback: LandingFeedback,
  LandingAction: LandingAction,
  LandingActionResult: LandingActionResult,
  TakeoffActionGoal: TakeoffActionGoal,
  LandingResult: LandingResult,
  PoseGoal: PoseGoal,
  PoseActionGoal: PoseActionGoal,
  PoseActionResult: PoseActionResult,
  PoseResult: PoseResult,
  PoseAction: PoseAction,
  TakeoffAction: TakeoffAction,
  TakeoffResult: TakeoffResult,
};
