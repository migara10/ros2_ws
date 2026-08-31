import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    pkg_path = get_package_share_directory('my_lidar_robot')
    xacro_file = os.path.join(pkg_path, 'urdf', 'my_lidar_robot.urdf.xacro')
    robot_description = Command(['xacro ', xacro_file])
    map_file = os.path.join(pkg_path, 'maps', 'my_map.yaml')
    nav2_params = os.path.join(pkg_path, 'config', 'nav2_params.yaml')
    rviz_config = os.path.join(pkg_path, 'rviz', 'my_config.rviz')

        # Gazebo
    world_file = os.path.join(pkg_path, 'worlds', 'my_world.world')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'),
            'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file}.items()
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': True}],
        output='screen'
    )

    # Spawn Robot
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_lidar_robot'],
        output='screen'
    )

    # Nav2 - 5 seconds delay දාලා (Gazebo fully load වෙනකම් ඉන්න)
    nav2 = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('nav2_bringup'),
                    'launch', 'bringup_launch.py')
                ),
                launch_arguments={
                    'map': map_file,
                    'params_file': nav2_params,
                    'use_sim_time': 'true'
                }.items()
            )
        ]
    )

    # RViz - 8 seconds delay (Nav2 load වෙනකම් ඉන්න)
    rviz = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='rviz2',
                executable='rviz2',
                arguments=['-d', rviz_config],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        nav2,
        rviz,
    ])