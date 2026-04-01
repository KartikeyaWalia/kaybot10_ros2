#🤖 Kaybot10 Bipedal Robot

A 10-DOF bipedal robot simulation built for ROS 2 Jazzy and Gazebo Harmonic. This project features a custom URDF with optimized collision geometry and gamepad teleoperation.
##🛠 Installation & Build

Follow these steps to set up the environment and build the package from source.
1. Prerequisites

Ensure you have ROS 2 Jazzy installed on Ubuntu 24.04. You will also need the following dependencies:
Bash

```
sudo apt update
sudo apt install ros-jazzy-joy joystick ros-jazzy-xacro ros-jazzy-ros2-control
```

2. Building the Workspace

Ensure your workspace is structured as ~/your_ws/src/kaybot10.
Bash

# Navigate to workspace root
cd ~/your_ws

# Build the package
colcon build --symlink-install --packages-select kaybot10

# Source the workspace
source install/setup.bash

🚀 Running the Simulation
Mode A: Visualization (RViz Only)

Use this mode to check joint axes and URDF limits without physics overhead.

Note: This mode uses a custom script to "puppet" the robot.
Bash

ros2 launch kaybot10 teleop.launch.py

Mode B: Physics (Gazebo)

Launch the full physics environment with ROS 2 Control enabled.
Bash

ros2 launch kaybot10 gazebo.launch.py

🎮 Gamepad Teleop Setup

Control Kaybot10 using a Bluetooth gamepad.
Step 1: Hardware Verification

Connect your controller via Bluetooth and identify the device index:
Bash

ls /dev/input/js*
# Usually /dev/input/js0

Test the raw inputs:
Bash

sudo jstest /dev/input/js0

Step 2: Launch Control Nodes

In separate terminals, run the driver and the mapping script:

    Joy Driver: ros2 run joy joy_node

    Teleop Script: python3 src/kaybot10/scripts/kaybot_teleop.py

    Note: The teleop script uses the Left Stick for the left leg and Right Stick for the right leg, with safety clamping on the knee joints to prevent forward hyperextension.

🧪 Manual Testing & Poses

If you do not have a gamepad, you can send a specific pose directly to the Gazebo controllers via the terminal.
Send a "Squat/Ready" Pose

Run the following command to move all 10 joints to a crouched, stable position:
Bash

ros2 topic pub --once /leg_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{
  header: {stamp: {sec: 0, nanosec: 0}},
  joint_names: ['lt_abd', 'lt_rot', 'lt_flex', 'lt_knee', 'lt_ankle', 'rt_abd', 'rt_rot', 'rt_flex', 'rt_knee', 'rt_ankle'],
  points: [{
    positions: [0.05, 0.05, 0.6, -1.2, 0.4, -0.05, -0.05, 0.6, -1.2, 0.4],
    time_from_start: {sec: 2, nanosec: 0}
  }]
}"

🔍 Troubleshooting

    Red Model in RViz: If the robot appears solid red, check the Global Options and ensure Fixed Frame is set to base_link.

    Slow Gazebo Performance: Ensure the collision geometry is using Primitives (Boxes/Cylinders) rather than high-poly meshes.

    Controller Failure: Run ros2 control list_controllers to verify that leg_controller is active.
