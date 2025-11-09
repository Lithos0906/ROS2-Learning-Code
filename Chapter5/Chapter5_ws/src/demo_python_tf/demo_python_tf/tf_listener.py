import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer # coordinate listener
from tf_transformations import euler_from_quaternion # euler angle to quaternion function

class TFListener(Node):
    def __init__(self):
        super().__init__('tf_listener')
        self.buffer_ = Buffer()
        self.listener_ = TransformListener(self.buffer_, self)
        self.timer_ = self.create_timer(1.0, self.get_transform)

    def get_transform(self):
        # real-time query relations of coordinates buffer_
        try:
            result = self.buffer_.lookup_transform('base_link', 'bottle_link', rclpy.time.Time(seconds=0), rclpy.time.Duration(seconds=1.0))
            transform = result.transform
            self.get_logger().info(f"Translation: {transform.translation}")
            self.get_logger().info(f"Rotation: {transform.rotation}")
            rotation_euler = euler_from_quaternion([
                transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w])
            self.get_logger().info(f"Rotation_RPY: {rotation_euler}")
            
        except Exception as e:
            self.get_logger().warn(f"failed to obtain coordinate transformation, the reason is: {str(e)}")

def main():
    rclpy.init()
    node = TFListener()
    rclpy.spin(node)
    rclpy.shutdown()
