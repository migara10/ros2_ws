import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg_my_lidar_robot = get_package_share_directory('my_lidar_robot')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_my_lidar_robot, 'launch', 'gazebo.launch.py'))
    )
    slam_launch = TimerAction(
        period=5.0,
        actions=[IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_my_lidar_robot, 'launch', 'slam.launch.py'))
        )]
    )
    return LaunchDescription([gazebo_launch, slam_launch])