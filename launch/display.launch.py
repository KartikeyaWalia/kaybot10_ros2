import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
import xacro

def generate_launch_description():
    pkg_name = 'kaybot10'
    
    # Path to your xacro file
    xacro_file = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'kaybot10.xacro')
    
    # Process xacro into raw XML robot_description
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    return LaunchDescription([
        # Starts the TF tree publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_raw}]
        ),
        # Starts the GUI with sliders for your 10 joints
        #Node(
        #    package='joint_state_publisher_gui',
        #    executable='joint_state_publisher_gui',
        #    name='joint_state_publisher_gui'
        #),
        # Opens RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.join(get_package_share_directory('kaybot10'), 'config', 'display.rviz')]
        )
    ])

