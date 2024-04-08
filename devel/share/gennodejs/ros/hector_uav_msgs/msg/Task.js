// Auto-generated. Do not edit!

// (in-package hector_uav_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Task {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.task_idx = null;
      this.size = null;
      this.processor_id = null;
      this.dependency = null;
      this.st = null;
      this.et = null;
      this.delta = null;
      this.ci = null;
      this.app_name = null;
    }
    else {
      if (initObj.hasOwnProperty('task_idx')) {
        this.task_idx = initObj.task_idx
      }
      else {
        this.task_idx = 0;
      }
      if (initObj.hasOwnProperty('size')) {
        this.size = initObj.size
      }
      else {
        this.size = 0;
      }
      if (initObj.hasOwnProperty('processor_id')) {
        this.processor_id = initObj.processor_id
      }
      else {
        this.processor_id = 0;
      }
      if (initObj.hasOwnProperty('dependency')) {
        this.dependency = initObj.dependency
      }
      else {
        this.dependency = [];
      }
      if (initObj.hasOwnProperty('st')) {
        this.st = initObj.st
      }
      else {
        this.st = 0.0;
      }
      if (initObj.hasOwnProperty('et')) {
        this.et = initObj.et
      }
      else {
        this.et = 0.0;
      }
      if (initObj.hasOwnProperty('delta')) {
        this.delta = initObj.delta
      }
      else {
        this.delta = 0.0;
      }
      if (initObj.hasOwnProperty('ci')) {
        this.ci = initObj.ci
      }
      else {
        this.ci = 0.0;
      }
      if (initObj.hasOwnProperty('app_name')) {
        this.app_name = initObj.app_name
      }
      else {
        this.app_name = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Task
    // Serialize message field [task_idx]
    bufferOffset = _serializer.int16(obj.task_idx, buffer, bufferOffset);
    // Serialize message field [size]
    bufferOffset = _serializer.int32(obj.size, buffer, bufferOffset);
    // Serialize message field [processor_id]
    bufferOffset = _serializer.int16(obj.processor_id, buffer, bufferOffset);
    // Serialize message field [dependency]
    bufferOffset = _arraySerializer.int16(obj.dependency, buffer, bufferOffset, null);
    // Serialize message field [st]
    bufferOffset = _serializer.float32(obj.st, buffer, bufferOffset);
    // Serialize message field [et]
    bufferOffset = _serializer.float32(obj.et, buffer, bufferOffset);
    // Serialize message field [delta]
    bufferOffset = _serializer.float32(obj.delta, buffer, bufferOffset);
    // Serialize message field [ci]
    bufferOffset = _serializer.float32(obj.ci, buffer, bufferOffset);
    // Serialize message field [app_name]
    bufferOffset = _serializer.string(obj.app_name, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Task
    let len;
    let data = new Task(null);
    // Deserialize message field [task_idx]
    data.task_idx = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [size]
    data.size = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [processor_id]
    data.processor_id = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [dependency]
    data.dependency = _arrayDeserializer.int16(buffer, bufferOffset, null)
    // Deserialize message field [st]
    data.st = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [et]
    data.et = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [delta]
    data.delta = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [ci]
    data.ci = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [app_name]
    data.app_name = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 2 * object.dependency.length;
    length += _getByteLength(object.app_name);
    return length + 32;
  }

  static datatype() {
    // Returns string type for a message object
    return 'hector_uav_msgs/Task';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '668dfc76f12c9bfd244f077958b63291';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int16 task_idx
    int32 size
    int16 processor_id
    int16[] dependency
    float32 st
    float32 et
    float32 delta
    float32 ci
    string app_name
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Task(null);
    if (msg.task_idx !== undefined) {
      resolved.task_idx = msg.task_idx;
    }
    else {
      resolved.task_idx = 0
    }

    if (msg.size !== undefined) {
      resolved.size = msg.size;
    }
    else {
      resolved.size = 0
    }

    if (msg.processor_id !== undefined) {
      resolved.processor_id = msg.processor_id;
    }
    else {
      resolved.processor_id = 0
    }

    if (msg.dependency !== undefined) {
      resolved.dependency = msg.dependency;
    }
    else {
      resolved.dependency = []
    }

    if (msg.st !== undefined) {
      resolved.st = msg.st;
    }
    else {
      resolved.st = 0.0
    }

    if (msg.et !== undefined) {
      resolved.et = msg.et;
    }
    else {
      resolved.et = 0.0
    }

    if (msg.delta !== undefined) {
      resolved.delta = msg.delta;
    }
    else {
      resolved.delta = 0.0
    }

    if (msg.ci !== undefined) {
      resolved.ci = msg.ci;
    }
    else {
      resolved.ci = 0.0
    }

    if (msg.app_name !== undefined) {
      resolved.app_name = msg.app_name;
    }
    else {
      resolved.app_name = ''
    }

    return resolved;
    }
};

module.exports = Task;
