; Auto-generated. Do not edit!


(cl:in-package hector_uav_msgs-msg)


;//! \htmlinclude FinishTime.msg.html

(cl:defclass <FinishTime> (roslisp-msg-protocol:ros-message)
  ((task_id
    :reader task_id
    :initarg :task_id
    :type cl:integer
    :initform 0)
   (actual_finish_time
    :reader actual_finish_time
    :initarg :actual_finish_time
    :type cl:float
    :initform 0.0))
)

(cl:defclass FinishTime (<FinishTime>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FinishTime>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FinishTime)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hector_uav_msgs-msg:<FinishTime> is deprecated: use hector_uav_msgs-msg:FinishTime instead.")))

(cl:ensure-generic-function 'task_id-val :lambda-list '(m))
(cl:defmethod task_id-val ((m <FinishTime>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hector_uav_msgs-msg:task_id-val is deprecated.  Use hector_uav_msgs-msg:task_id instead.")
  (task_id m))

(cl:ensure-generic-function 'actual_finish_time-val :lambda-list '(m))
(cl:defmethod actual_finish_time-val ((m <FinishTime>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hector_uav_msgs-msg:actual_finish_time-val is deprecated.  Use hector_uav_msgs-msg:actual_finish_time instead.")
  (actual_finish_time m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FinishTime>) ostream)
  "Serializes a message object of type '<FinishTime>"
  (cl:let* ((signed (cl:slot-value msg 'task_id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'actual_finish_time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FinishTime>) istream)
  "Deserializes a message object of type '<FinishTime>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'task_id) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'actual_finish_time) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FinishTime>)))
  "Returns string type for a message object of type '<FinishTime>"
  "hector_uav_msgs/FinishTime")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FinishTime)))
  "Returns string type for a message object of type 'FinishTime"
  "hector_uav_msgs/FinishTime")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FinishTime>)))
  "Returns md5sum for a message object of type '<FinishTime>"
  "0a2b7ffc95095888c49a445900a66d0b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FinishTime)))
  "Returns md5sum for a message object of type 'FinishTime"
  "0a2b7ffc95095888c49a445900a66d0b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FinishTime>)))
  "Returns full string definition for message of type '<FinishTime>"
  (cl:format cl:nil "int32 task_id~%float32 actual_finish_time~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FinishTime)))
  "Returns full string definition for message of type 'FinishTime"
  (cl:format cl:nil "int32 task_id~%float32 actual_finish_time~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FinishTime>))
  (cl:+ 0
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FinishTime>))
  "Converts a ROS message object to a list"
  (cl:list 'FinishTime
    (cl:cons ':task_id (task_id msg))
    (cl:cons ':actual_finish_time (actual_finish_time msg))
))
