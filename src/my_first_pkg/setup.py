from setuptools import find_packages, setup

package_name = 'my_first_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='migara',
    maintainer_email='migaraten@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher = my_first_pkg.publisher:main',
            'subscriber = my_first_pkg.subscriber:main',
            'service_server = my_first_pkg.service_server:main',
            'service_client = my_first_pkg.service_client:main',
            'action_server = my_first_pkg.action_server:main',
        ],
    },
)
