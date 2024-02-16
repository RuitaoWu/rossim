;; Auto-generated. Do not edit!


(when (boundp 'hector_uav_msgs::Task)
  (if (not (find-package "HECTOR_UAV_MSGS"))
    (make-package "HECTOR_UAV_MSGS"))
  (shadow 'Task (find-package "HECTOR_UAV_MSGS")))
(unless (find-package "HECTOR_UAV_MSGS::TASK")
  (make-package "HECTOR_UAV_MSGS::TASK"))

(in-package "ROS")
;;//! \htmlinclude Task.msg.html


(defclass hector_uav_msgs::Task
  :super ros::object
  :slots (_task_idx _size _processor_id _dependency _st _et ))

(defmethod hector_uav_msgs::Task
  (:init
   (&key
    ((:task_idx __task_idx) 0)
    ((:size __size) 0)
    ((:processor_id __processor_id) 0)
    ((:dependency __dependency) (make-array 0 :initial-element 0 :element-type :integer))
    ((:st __st) 0.0)
    ((:et __et) 0.0)
    )
   (send-super :init)
   (setq _task_idx (round __task_idx))
   (setq _size (round __size))
   (setq _processor_id (round __processor_id))
   (setq _dependency __dependency)
   (setq _st (float __st))
   (setq _et (float __et))
   self)
  (:task_idx
   (&optional __task_idx)
   (if __task_idx (setq _task_idx __task_idx)) _task_idx)
  (:size
   (&optional __size)
   (if __size (setq _size __size)) _size)
  (:processor_id
   (&optional __processor_id)
   (if __processor_id (setq _processor_id __processor_id)) _processor_id)
  (:dependency
   (&optional __dependency)
   (if __dependency (setq _dependency __dependency)) _dependency)
  (:st
   (&optional __st)
   (if __st (setq _st __st)) _st)
  (:et
   (&optional __et)
   (if __et (setq _et __et)) _et)
  (:serialization-length
   ()
   (+
    ;; int16 _task_idx
    2
    ;; int32 _size
    4
    ;; int16 _processor_id
    2
    ;; int16[] _dependency
    (* 2    (length _dependency)) 4
    ;; float32 _st
    4
    ;; float32 _et
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int16 _task_idx
       (write-word _task_idx s)
     ;; int32 _size
       (write-long _size s)
     ;; int16 _processor_id
       (write-word _processor_id s)
     ;; int16[] _dependency
     (write-long (length _dependency) s)
     (dotimes (i (length _dependency))
       (write-word (elt _dependency i) s)
       )
     ;; float32 _st
       (sys::poke _st (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _et
       (sys::poke _et (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int16 _task_idx
     (setq _task_idx (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int32 _size
     (setq _size (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int16 _processor_id
     (setq _processor_id (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; int16[] _dependency
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _dependency (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _dependency i) (sys::peek buf ptr- :short)) (incf ptr- 2)
     ))
   ;; float32 _st
     (setq _st (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _et
     (setq _et (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get hector_uav_msgs::Task :md5sum-) "ebe954c7abe191b746293c22f87ec843")
(setf (get hector_uav_msgs::Task :datatype-) "hector_uav_msgs/Task")
(setf (get hector_uav_msgs::Task :definition-)
      "int16 task_idx
int32 size
int16 processor_id
int16[] dependency
float32 st
float32 et
")



(provide :hector_uav_msgs/Task "ebe954c7abe191b746293c22f87ec843")


