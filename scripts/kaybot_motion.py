import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class KaybotMotion(Node):
    def __init__(self):
        super().__init__('kaybot_motion')
        self.publisher = self.create_publisher(JointTrajectory, '/leg_controller/joint_trajectory', 10)
        
        # Exact order from your YAML
        self.joints = [
            'lt_abd', 'lt_rot', 'lt_flex', 'lt_knee', 'lt_ankle',
            'rt_abd', 'rt_rot', 'rt_flex', 'rt_knee', 'rt_ankle'
        ]
        
        print("Kaybot Motion Controller Started")
        print("Press 1 to SIT, 2 to STAND (0.0 position)")

    def send_movement(self, positions):
        msg = JointTrajectory()
        msg.joint_names = self.joints
        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = 2  # Move slowly over 2 seconds
        msg.points.append(point)
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = KaybotMotion()
    
    try:
        while rclpy.ok():
            user_input = input("Enter Command: ")
            if user_input == '1':
                # SITTING: Hips flex forward, Knees bend back, Ankles adjust
                # [abd, rot, flex, knee, ankle] x2
                sit_pos = [0.0, 0.0, 0.8, -1.6, 0.5,  0.0, 0.0, 0.8, -1.6, 0.5]
                node.send_movement(sit_pos)
                print("Sitting...")
            elif user_input == '2':
                # STANDING: All zeros
                stand_pos = [0.0] * 10
                node.send_movement(stand_pos)
                print("Standing up...")
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
