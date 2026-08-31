import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_path = get_package_share_directory('my_lidar_robot')
    map_file = os.path.join(pkg_path, 'maps', 'my_map.yaml')
    nav2_params = os.path.join(pkg_path, 'config', 'nav2_params.yaml')

    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_file,
            'params_file': nav2_params,
            'use_sim_time': 'true'
        }.items()
    )

    return LaunchDescription([bringup])