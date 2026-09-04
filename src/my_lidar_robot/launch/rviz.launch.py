import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_my_lidar_robot = get_package_share_directory('my_lidar_robot')
    rviz_config_file = os.path.join(pkg_my_lidar_robot, 'rviz', 'my_robot.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}]
    )
    return LaunchDescription([rviz_node])