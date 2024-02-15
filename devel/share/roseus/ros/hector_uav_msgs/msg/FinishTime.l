;; Auto-generated. Do not edit!


(when (boundp 'hector_uav_msgs::FinishTime)
  (if (not (find-package "HECTOR_UAV_MSGS"))
    (make-package "HECTOR_UAV_MSGS"))
  (shadow 'FinishTime (find-package "HECTOR_UAV_MSGS")))
(unless (find-package "HECTOR_UAV_MSGS::FINISHTIME")
  (make-package "HECTOR_UAV_MSGS::FINISHTIME"))

(in-package "ROS")
;;//! \htmlinclude FinishTime.msg.html


(defclass hector_uav_msgs::FinishTime
  :super ros::object
  :slots (_task_id _actual_finish_time ))

(defmethod hector_uav_msgs::FinishTime
  (:init
   (&key
    ((:task_id __task_id) 0)
    ((:actual_finish_time __actual_finish_time) 0.0)
    )
   (send-super :init)
   (setq _task_id (round __task_id))
   (setq _actual_finish_time (float __actual_finish_time))
   self)
  (:task_id
   (&optional __task_id)
   (if __task_id (setq _task_id __task_id)) _task_id)
  (:actual_finish_time
   (&optional __actual_finish_time)
   (if __actual_finish_time (setq _actual_finish_time __actual_finish_time)) _actual_finish_time)
  (:serialization-length
   ()
   (+
    ;; int32 _task_id
    4
    ;; float32 _actual_finish_time
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _task_id
       (write-long _task_id s)
     ;; float32 _actual_finish_time
       (sys::poke _actual_finish_time (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _task_id
     (setq _task_id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float32 _actual_finish_time
     (setq _actual_finish_time (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get hector_uav_msgs::FinishTime :md5sum-) "0a2b7ffc95095888c49a445900a66d0b")
(setf (get hector_uav_msgs::FinishTime :datatype-) "hector_uav_msgs/FinishTime")
(setf (get hector_uav_msgs::FinishTime :definition-)
      "int32 task_id
float32 actual_finish_time

")



(provide :hector_uav_msgs/FinishTime "0a2b7ffc95095888c49a445900a66d0b")


