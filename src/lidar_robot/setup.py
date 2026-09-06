import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'lidar_robot'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Launch files
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),

        # URDF / Xacro files
        (os.path.join('share', package_name, 'urdf'),
            glob(os.path.join('urdf', '*'))),

        # World files
        (os.path.join('share', package_name, 'worlds'),
            glob(os.path.join('worlds', '*'))),

        # RViz config files
        (os.path.join('share', package_name, 'rviz'),
            glob(os.path.join('rviz', '*'))),

        # Config (nav2/slam yaml)
        (os.path.join('share', package_name, 'config'),
            glob(os.path.join('config', '*'))),

        # Maps
        (os.path.join('share', package_name, 'maps'),
            glob(os.path.join('maps', '*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Custom lidar robot with Gazebo, RViz, SLAM and Nav2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor_driver_node = lidar_robot.motor_driver_node:main',
        ],
    },
)