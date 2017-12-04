
"use strict";

let AssemblyStates = require('./AssemblyStates.js');
let JointCommand = require('./JointCommand.js');
let HeadPanCommand = require('./HeadPanCommand.js');
let URDFConfiguration = require('./URDFConfiguration.js');
let DigitalIOStates = require('./DigitalIOStates.js');
let AnalogIOStates = require('./AnalogIOStates.js');
let HeadState = require('./HeadState.js');
let EndEffectorState = require('./EndEffectorState.js');
let CameraControl = require('./CameraControl.js');
let CollisionAvoidanceState = require('./CollisionAvoidanceState.js');
let CollisionDetectionState = require('./CollisionDetectionState.js');
let AnalogOutputCommand = require('./AnalogOutputCommand.js');
let NavigatorStates = require('./NavigatorStates.js');
let DigitalOutputCommand = require('./DigitalOutputCommand.js');
let AnalogIOState = require('./AnalogIOState.js');
let RobustControllerStatus = require('./RobustControllerStatus.js');
let EndpointState = require('./EndpointState.js');
let CameraSettings = require('./CameraSettings.js');
let EndEffectorCommand = require('./EndEffectorCommand.js');
let NavigatorState = require('./NavigatorState.js');
let DigitalIOState = require('./DigitalIOState.js');
let SEAJointState = require('./SEAJointState.js');
let EndpointStates = require('./EndpointStates.js');
let EndEffectorProperties = require('./EndEffectorProperties.js');
let AssemblyState = require('./AssemblyState.js');

module.exports = {
  AssemblyStates: AssemblyStates,
  JointCommand: JointCommand,
  HeadPanCommand: HeadPanCommand,
  URDFConfiguration: URDFConfiguration,
  DigitalIOStates: DigitalIOStates,
  AnalogIOStates: AnalogIOStates,
  HeadState: HeadState,
  EndEffectorState: EndEffectorState,
  CameraControl: CameraControl,
  CollisionAvoidanceState: CollisionAvoidanceState,
  CollisionDetectionState: CollisionDetectionState,
  AnalogOutputCommand: AnalogOutputCommand,
  NavigatorStates: NavigatorStates,
  DigitalOutputCommand: DigitalOutputCommand,
  AnalogIOState: AnalogIOState,
  RobustControllerStatus: RobustControllerStatus,
  EndpointState: EndpointState,
  CameraSettings: CameraSettings,
  EndEffectorCommand: EndEffectorCommand,
  NavigatorState: NavigatorState,
  DigitalIOState: DigitalIOState,
  SEAJointState: SEAJointState,
  EndpointStates: EndpointStates,
  EndEffectorProperties: EndEffectorProperties,
  AssemblyState: AssemblyState,
};
