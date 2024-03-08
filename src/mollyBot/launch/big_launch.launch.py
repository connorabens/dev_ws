#all launch commands i've been entering into terminal 
#manually that I'd like to make into a single launch file.

#ros2 launch mollyBot navigation_launch.py
#ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/mollyBot/config/mapper_params_online_async.yaml use_sim_time:=true
#rviz2  -- for now I'll continue to run this from the terminal.  First method didn't work.
#ros2 run teleop_twist_keyboard teleop_twist_keyboard
#ros2 launch mollyBot launch_sim.launch.py world:=./src/mollyBot/worlds/blockroom.world
#

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    slam_params_file = LaunchConfiguration('slam_params_file', default=os.path.join(
        get_package_share_directory('mollyBot'), 'config', 'mapper_params_online_async.yaml'))

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    world_file = LaunchConfiguration('world', default=os.path.join(
        get_package_share_directory('mollyBot'), 'worlds', 'blockroom.world'))

    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mollyBot'),
            'launch',
            'navigation_launch.py'
        )])
    )

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('slam_toolbox'),
            'launch',
            'online_async_launch.py'
        )]),
        launch_arguments={'slam_params_file': slam_params_file, 'use_sim_time': use_sim_time}.items(),
    )

    teleop_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist_keyboard',
        output='screen',
        prefix='xterm -e'
    )

    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('mollyBot'),
            'launch',
            'launch_sim.launch.py'
        )]),
        launch_arguments={'world': world_file}.items(),
    )
    return LaunchDescription([
        navigation_launch,
        slam_launch,
        teleop_node,
        sim_launch
     ])

