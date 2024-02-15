#include "WifiReceiverPlugin.hh"
#include "gazebo/sensors/SensorFactory.hh"
#include "gazebo/sensors/SensorManager.hh"
#include "ignition/math/Rand.hh"
#include "gazebo/msgs/msgs.hh"
#include "gazebo/transport/Node.hh"
#include "gazebo/transport/Publisher.hh"
#include "gazebo/sensors/WirelessTransmitter.hh"
#include "gazebo/util/system.hh"
#include "ros/ros.h"
#include "std_msgs/Float32.h"
#include "std_msgs/Float32MultiArray.h"



using namespace std;
using namespace gazebo;
using namespace sensors;
GZ_REGISTER_SENSOR_PLUGIN(WifiReceiverPlugin)

std::string ns = ros::this_node::getNamespace();
ros::NodeHandle nh;
ros::Publisher recv_signal = nh.advertise<std_msgs::Float32MultiArray>(ns + "recv_Signal", 1000);


WifiReceiverPlugin::WifiReceiverPlugin() : SensorPlugin()
{

}

WifiReceiverPlugin::~WifiReceiverPlugin()
{
}

void WifiReceiverPlugin::Load(sensors::SensorPtr _sensor, sdf::ElementPtr /*_sdf*/)
{
  // Get the parent sensor.
  this->parentSensor =
    std::dynamic_pointer_cast<sensors::WirelessReceiver>(_sensor);

  // Make sure the parent sensor is valid.
  if (!this->parentSensor)
  {
    gzerr << "WifiReceiverPlugin requires a Wireless Transmitter Sensor.\n";
    return;
  }

  // Connect to the sensor update event.
  this->updateConnection = this->parentSensor->ConnectUpdated(
      std::bind(&WifiReceiverPlugin::UpdateImpl, this));

  // Make sure the parent sensor is active.
  this->parentSensor->SetActive(true);
  // this->parentSensor->SetPose(ignition::math::Pose3d (100, 100, 100, 0, 0, 0));

}

bool WifiReceiverPlugin::UpdateImpl()
{

  std_msgs::Float32MultiArray rssi;

  vector<SensorPtr> currSensors;
  currSensors = SensorManager::Instance()->GetSensors();
  double time_value;
  time_value = ros::Time::now().toSec();
  // std::cout << time_value << endl;
  rssi.data.push_back(time_value);

  for (int i = 0; i < currSensors.size(); i++)
  {
    std::string txEssid;
    // msgs::WirelessNodes msg;
    double rxPower;
    double txFreq;

    sensors::SensorPtr sensor_ptr;
    sensor_ptr = SensorManager::Instance()->GetSensor("wirelessTransmitter");
    if (currSensors[i]->Type() == "wireless_transmitter")
    {
      sensors::WirelessTransmitterPtr transmitSensor;
      transmitSensor = std::dynamic_pointer_cast<sensors::WirelessTransmitter>(currSensors[i]);
      // std::cout << "Connected to: " + transmitSensor->ESSID() + "\n";
      double signal_strength;
      signal_strength = transmitSensor->SignalStrength(this->parentSensor->Pose(), this->parentSensor->Gain());
      // std::cout << "Signal strengh: " << signal_strength << "\n";
      rssi.data.push_back(signal_strength);

      ignition::math::Pose3d myPos = this->parentSensor->Pose();
      // std::cout << "Pose: " << myPos << "\n";

    }


  }
  // std::cout << "RSSI: " << rssi << "\n";
  recv_signal.publish(rssi);
  return true;

}
