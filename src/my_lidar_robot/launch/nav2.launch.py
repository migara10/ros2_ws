import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_my_lidar_robot = get_package_share_directory('my_lidar_robot')
    map_file = os.path.join(pkg_my_lidar_robot, 'maps', 'my_map.yaml')
    params_file = os.path.join(pkg_my_lidar_robot, 'config', 'nav2_params.yaml')

    lifecycle_nodes_localization = ['map_server', 'amcl']
    lifecycle_nodes_navigation = [
        'controller_server', 'smoother_server', 'planner_server',
        'behavior_server', 'bt_navigator', 'waypoint_follower',
        'velocity_smoother', 'collision_monitor',
    ]

    nodes = [
        Node(package='nav2_map_server', executable='map_server', name='map_server',
             output='screen', parameters=[params_file, {'use_sim_time': True, 'yaml_filename': map_file}]),
        Node(package='nav2_amcl', executable='amcl', name='amcl',
             output='screen', parameters=[params_file, {'use_sim_time': True}]),
        Node(package='nav2_controller', executable='controller_server', name='controller_server',
             output='screen', parameters=[params_file, {'use_sim_time': True}]),
        Node(package='nav2_smoother', executable='smoother_server', name='smoother_server',
             output='screen', parameters=[params_file, {'use_sim_time': True}]),
        Node(package='nav2_planner', executable='planner_server', name='planner_server',
             output='screen', parameters=[params_file, {'use_sim_time': True}]),
        Node(package='nav2_behaviors', executable='behavior_server', name='behavior_server',
             output='screen', parameters=[params_file, {'use_sim_time': True}]),
        Node(package='nav2_bt_navigator', executable='bt_navigator', name='bt_navigator',
             output='screen', parameters=[params_file, {'use_sim_time': True}]),
        Node(package='nav2_waypoint_follower', executable='waypoint_follower', name='waypoint_follower',
             output='screen', parameters=[params_file, {'use_sim_time': True}]),
        Node(package='nav2_velocity_smoother', executable='velocity_smoother', name='velocity_smoother',
             output='screen', parameters=[params_file, {'use_sim_time': True}]),
        Node(package='nav2_collision_monitor', executable='collision_monitor', name='collision_monitor',
             output='screen', parameters=[params_file, {'use_sim_time': True}]),
        Node(package='nav2_lifecycle_manager', executable='lifecycle_manager', name='lifecycle_manager_localization',
             output='screen', parameters=[{'use_sim_time': True, 'autostart': True, 'node_names': lifecycle_nodes_localization}]),
        Node(package='nav2_lifecycle_manager', executable='lifecycle_manager', name='lifecycle_manager_navigation',
             output='screen', parameters=[{'use_sim_time': True, 'autostart': True, 'node_names': lifecycle_nodes_navigation}]),
    ]
    return LaunchDescription(nodes)