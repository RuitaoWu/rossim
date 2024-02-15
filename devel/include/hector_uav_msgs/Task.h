// Generated by gencpp from file hector_uav_msgs/Task.msg
// DO NOT EDIT!


#ifndef HECTOR_UAV_MSGS_MESSAGE_TASK_H
#define HECTOR_UAV_MSGS_MESSAGE_TASK_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace hector_uav_msgs
{
template <class ContainerAllocator>
struct Task_
{
  typedef Task_<ContainerAllocator> Type;

  Task_()
    : task_idx(0)
    , size(0)
    , processor_id(0)
    , dependency()  {
    }
  Task_(const ContainerAllocator& _alloc)
    : task_idx(0)
    , size(0)
    , processor_id(0)
    , dependency(_alloc)  {
  (void)_alloc;
    }



   typedef int16_t _task_idx_type;
  _task_idx_type task_idx;

   typedef int32_t _size_type;
  _size_type size;

   typedef int16_t _processor_id_type;
  _processor_id_type processor_id;

   typedef std::vector<int16_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int16_t>> _dependency_type;
  _dependency_type dependency;





  typedef boost::shared_ptr< ::hector_uav_msgs::Task_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::hector_uav_msgs::Task_<ContainerAllocator> const> ConstPtr;

}; // struct Task_

typedef ::hector_uav_msgs::Task_<std::allocator<void> > Task;

typedef boost::shared_ptr< ::hector_uav_msgs::Task > TaskPtr;
typedef boost::shared_ptr< ::hector_uav_msgs::Task const> TaskConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::hector_uav_msgs::Task_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::hector_uav_msgs::Task_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::hector_uav_msgs::Task_<ContainerAllocator1> & lhs, const ::hector_uav_msgs::Task_<ContainerAllocator2> & rhs)
{
  return lhs.task_idx == rhs.task_idx &&
    lhs.size == rhs.size &&
    lhs.processor_id == rhs.processor_id &&
    lhs.dependency == rhs.dependency;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::hector_uav_msgs::Task_<ContainerAllocator1> & lhs, const ::hector_uav_msgs::Task_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace hector_uav_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::hector_uav_msgs::Task_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::hector_uav_msgs::Task_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::hector_uav_msgs::Task_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::hector_uav_msgs::Task_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::hector_uav_msgs::Task_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::hector_uav_msgs::Task_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::hector_uav_msgs::Task_<ContainerAllocator> >
{
  static const char* value()
  {
    return "c0a76fc7e9a4dae61b315833b98d9564";
  }

  static const char* value(const ::hector_uav_msgs::Task_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xc0a76fc7e9a4dae6ULL;
  static const uint64_t static_value2 = 0x1b315833b98d9564ULL;
};

template<class ContainerAllocator>
struct DataType< ::hector_uav_msgs::Task_<ContainerAllocator> >
{
  static const char* value()
  {
    return "hector_uav_msgs/Task";
  }

  static const char* value(const ::hector_uav_msgs::Task_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::hector_uav_msgs::Task_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int16 task_idx\n"
"int32 size\n"
"int16 processor_id\n"
"int16[] dependency\n"
;
  }

  static const char* value(const ::hector_uav_msgs::Task_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::hector_uav_msgs::Task_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.task_idx);
      stream.next(m.size);
      stream.next(m.processor_id);
      stream.next(m.dependency);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Task_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::hector_uav_msgs::Task_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::hector_uav_msgs::Task_<ContainerAllocator>& v)
  {
    s << indent << "task_idx: ";
    Printer<int16_t>::stream(s, indent + "  ", v.task_idx);
    s << indent << "size: ";
    Printer<int32_t>::stream(s, indent + "  ", v.size);
    s << indent << "processor_id: ";
    Printer<int16_t>::stream(s, indent + "  ", v.processor_id);
    s << indent << "dependency[]" << std::endl;
    for (size_t i = 0; i < v.dependency.size(); ++i)
    {
      s << indent << "  dependency[" << i << "]: ";
      Printer<int16_t>::stream(s, indent + "  ", v.dependency[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // HECTOR_UAV_MSGS_MESSAGE_TASK_H
