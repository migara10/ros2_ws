import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 1. Environment Variable එක (TURTLEBOT3_MODEL=burger) Set කිරීම
    set_tb3_model = SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger')

    # Packages වල Paths ලබාගැනීම
    turtlebot3_gazebo_dir = get_package_share_directory('turtlebot3_gazebo')
    turtlebot3_cartographer_dir = get_package_share_directory('turtlebot3_cartographer')
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')

    # 2. Gazebo World එක Launch කිරීම
    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_gazebo_dir, 'launch', 'turtlebot3_world.launch.py')
        )
    )

    # 3. SLAM Toolbox (Online Sync Mode) Launch කිරීම
    launch_slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_toolbox_dir, 'launch', 'online_sync_launch.py')
        )
    )

    # 4. RViz2 Launch කිරීම
    turtlebot3_bringup_dir = get_package_share_directory('turtlebot3_bringup')
    launch_rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(turtlebot3_bringup_dir, 'launch', 'rviz2.launch.py')
        )
    )

    return LaunchDescription([
        set_tb3_model,
        launch_gazebo,
        launch_slam,
        launch_rviz
    ])