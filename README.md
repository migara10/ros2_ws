# ros2-lidar

cd ~/ros2_ws
rm -rf build install log
colcon build --symlink-install
source install/setup.bash
ros2 launch lidar_robot real_bringup.launch.py


cd ~/ros2_ws
source install/setup.bash
ros2 launch lidar_robot real_bringup.launch.py


cd ~/ros2_ws
source install/setup.bash
ros2 launch lidar_robot slam.launch.py


cd ~/ros2_ws
source install/setup.bash
ros2 launch lidar_robot nav2.launch.py




source /opt/ros/jazzy/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard


ls /dev/ttyUSB*
sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyUSB1



source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws/src/lidar_robot/maps
ros2 run nav2_map_server map_saver_cli -f my_map_real



ros2 run lidar_robot motor_driver_node --ros-args -p serial_port:=/dev/arduino -p min_pwm:=100

ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: 0.8}}" -r 10