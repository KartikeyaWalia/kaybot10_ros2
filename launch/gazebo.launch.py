import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_name = 'kaybot10'
    
    # REQUIRED: Tell Gazebo where your meshes are
    pkg_share = get_package_share_directory(package_name)
    os.environ["GZ_SIM_RESOURCE_PATH"] = os.path.join(pkg_share, '..')

    xacro_file = os.path.join(pkg_share, 'urdf', 'kaybot10.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'kaybot10', '-z', '0.5'],
        output='screen'
    )
    
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    leg_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["leg_controller"], # This name must match the YAML
    )

    return LaunchDescription([
        gazebo_sim,
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description_raw, 'use_sim_time': True}]
        ),
        spawn_entity,
        joint_state_broadcaster_spawner,
        leg_controller_spawner,
    ])
    
    
    

   
