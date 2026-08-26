import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_path = get_package_share_directory('my_lidar_robot')
    slam_params = os.path.join(pkg_path, 'config', 'mapper_params_online_async.yaml')

    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('slam_toolbox'),
                'launch', 'online_async_launch.py'
            )
        ),
        launch_arguments={
            'slam_params_file': slam_params,
            'use_sim_time': 'true'
        }.items()
    )

    return LaunchDescription([slam_toolbox])