import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    set_tb3_model = SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger')

    turtlebot3_gazebo_dir = get_package_share_directory('turtlebot3_gazebo')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    
    map_yaml_file = os.path.join(os.path.expanduser('~'), 'ros2_ws', 'my_map.yaml')
    params_file = os.path.join(nav2_bringup_dir, 'params', 'nav2_params.yaml')
    rviz_config_file = os.path.join(nav2_bringup_dir, 'rviz', 'nav2_default_view.rviz')

    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo_dir, 'launch', 'turtlebot3_world.launch.py')
        )
    )

    launch_nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_yaml_file,
            'params_file': params_file,
            'use_sim_time': 'true',
            'autostart': 'true'
        }.items()
    )

    rviz2_node = TimerAction(
        period=7.0,
        actions=[Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen'
        )]
    )

    return LaunchDescription([
        set_tb3_model,
        launch_gazebo,
        launch_nav2,
        rviz2_node
    ])