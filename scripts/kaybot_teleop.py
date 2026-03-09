import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy, JointState
import math

class KaybotTeleop(Node):
    def __init__(self):
        super().__init__('kaybot_teleop')
        
        # Subscribe to the gamepad
        self.create_subscription(Joy, '/joy', self.joy_callback, 10)
        
        # Publish directly to joint_states for RViz
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        
        # Define our 10 joints in order
        self.joint_names = [
            'lt_abd', 'lt_rot', 'lt_flex', 'lt_knee', 'lt_ankle',
            'rt_abd', 'rt_rot', 'rt_flex', 'rt_knee', 'rt_ankle'
        ]
        
        self.get_logger().info("Teleop Node Started. Move those sticks!")

    def joy_callback(self, msg):
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = self.joint_names
        pos = [0.0] * 10
        
        # LEFT LEG CONTROL (Left Stick - Axis 1)
        left_input = msg.axes[1] 
        pos[2] = left_input * 0.8         # lt_flex (Hip)
        # Knee only bends backward (clamped at 0.0)
        pos[3] = min(0.0, left_input * -1.5) # lt_knee
        # Ankle tilts to keep foot somewhat level
        pos[4] = left_input * 0.4         # lt_ankle

        # RIGHT LEG CONTROL (Right Stick - Axis 3)
        right_input = msg.axes[3]
        pos[7] = right_input * 0.8        # rt_flex (Hip)
        # Knee only bends backward
        pos[8] = min(0.0, right_input * -1.5) # rt_knee
        # Ankle tilts
        pos[9] = right_input * 0.4        # rt_ankle

        # ABDUCTION 
        # Often Axis 0 and 2 are used for this
        pos[0] = msg.axes[0] * 0.3        # lt_abd
        pos[5] = msg.axes[2] * -0.3       # rt_abd
        
        
        # Rotation (Optional: Bumpers LT(4)/RT(5) for side-to-side)
        # Often Axis 0 and 2 are used for this
        pos[1] = msg.axes[4] * -0.3        # lt_rot
        pos[6] = msg.axes[5] * -0.3       # rt_rot
        
        knee_command = msg.axes[3] * -1.5  # Right stick moves knees
        

        js.position = pos
        self.publisher.publish(js)

def main():
    rclpy.init()
    node = KaybotTeleop()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
