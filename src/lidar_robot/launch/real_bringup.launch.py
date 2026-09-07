import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command


def generate_launch_description():
    pkg_share = get_package_share_directory('lidar_robot')
    urdf_file = os.path.join(pkg_share, 'urdf', 'lidar_robot_real.urdf.xacro')
    rviz_config = os.path.join(pkg_share, 'rviz', 'lidar_robot.rviz')

    robot_description = Command(['xacro ', urdf_file])

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': False}]
    )

    lidar_node = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='sllidar_node',
        output='screen',
        parameters=[{
            'serial_port': '/dev/rplidar',
            'serial_baudrate': 115200,
            'frame_id': 'laser',
            'angle_compensate': True,
            'scan_mode': 'Sensitivity',
        }]
    )

    motor_driver_node = Node(
        package='lidar_robot',
        executable='motor_driver_node',
        name='motor_driver_node',
        output='screen',
        parameters=[{
            'serial_port': '/dev/arduino',
            'baudrate': 115200,
            'wheel_separation': 0.05,
            'max_speed': 255,
            'max_linear_vel': 4.0,
            'min_pwm': 100,
            'left_trim': 1.0,
            'right_trim': 0.85,
        }]
    )

    odometry_node = Node(
        package='rf2o_laser_odometry',
        executable='rf2o_laser_odometry_node',
        name='rf2o_laser_odometry',
        output='screen',
        parameters=[{
            'laser_scan_topic': '/scan',
            'odom_topic': '/odom',
            'publish_tf': True,
            'base_frame_id': 'base_link',
            'odom_frame_id': 'odom',
            'init_pose_from_topic': '',
            'freq': 10.0,
        }]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        lidar_node,
        motor_driver_node,
        odometry_node,
        rviz_node,
    ])