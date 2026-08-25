import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'my_bot'
    pkg_path = get_package_share_directory(pkg_name)
    
    # URDF file path
    urdf_file = os.path.join(pkg_path, 'urdf', 'my_robot.urdf')

    # Read URDF file
    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': True
        }]
    )

    # Gazebo ROS Launch (Gazebo server & client)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # Spawn Entity Node (Delayed by 5 seconds to let Gazebo start fully)
    spawn_entity = TimerAction(
        period=5.0,
        actions=[Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'my_robot'],
            output='screen'
        )]
    )

    # RViz2 Node (Delayed by 7 seconds)
    rviz2 = TimerAction(
        period=7.0,
        actions=[Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        )]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher_node,
        spawn_entity,
        rviz2
    ])