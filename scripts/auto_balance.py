import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math

class AutoBalancer(Node):
    def __init__(self):
        super().__init__('auto_balance')
        
        # Subscriber to the IMU
        self.create_subscription(Imu, '/imu', self.imu_callback, 10)
        
        # Publisher to the legs
        self.publisher = self.create_publisher(JointTrajectory, '/leg_controller/joint_trajectory', 10)
        
        self.joints = ['lt_abd', 'lt_rot', 'lt_flex', 'lt_knee', 'lt_ankle',
                       'rt_abd', 'rt_rot', 'rt_flex', 'rt_knee', 'rt_ankle']
        
        self.get_logger().info("Auto-Balancer initialized. Stand the robot up!")

    def imu_callback(self, msg):
        # 1. Convert Quaternion to Pitch (Rotation around Y-axis)
        q = msg.orientation
        sinp = 2 * (q.w * q.y - q.z * q.x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)
        else:
            pitch = math.asin(sinp)

        # Convert to degrees for easier logging
        pitch_deg = math.degrees(pitch)
        
        # 2. Simple Compensation Logic (P-Control)
        # If leaning forward (positive pitch), flex hips forward and ankles back
        k_p = 0.5  # Gain: how hard we fight the tilt
        correction = pitch * k_p
        
        self.get_logger().info(f"Tilt: {pitch_deg:.2f}° | Correction: {correction:.2f}")

        # 3. Create Command
        traj = JointTrajectory()
        traj.joint_names = self.joints
        point = JointTrajectoryPoint()
        
        # Position indices: flex is 2/7, ankle is 4/9
        # We adjust the flex and ankle to counteract the tilt
        pos = [0.0] * 10
        pos[2] = correction  # lt_flex
        pos[4] = -correction # lt_ankle
        pos[7] = correction  # rt_flex
        pos[9] = -correction # rt_ankle
        
        point.positions = pos
        point.time_from_start.nanosec = 100_000_000 # 0.1 seconds (fast)
        traj.points.append(point)
        self.publisher.publish(traj)

def main():
    rclpy.init()
    node = AutoBalancer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
