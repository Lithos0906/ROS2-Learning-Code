import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster # static coordinate publisher
from geometry_msgs.msg import TransformStamped # message interface
from tf_transformations import quaternion_from_euler # euler angle to quaternion function
import math # angle to radians

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.broadcaster_ = TransformBroadcaster(self)
        self.timer_ = self.create_timer(0.01, self.publish_tf)

    def publish_tf(self):
        # publish the static coordinate
        # the coordinate relation between camera_link and bottle_link
        transform = TransformStamped()
        transform.header.frame_id = 'camera_link'     # define the header point
        transform.child_frame_id = 'bottle_link'      # define the child point
        transform.header.stamp = self.get_clock().now().to_msg()    # get the time stamp

        transform.transform.translation.x = 0.2     # set the relation of coordinate
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.5
        
        q = quaternion_from_euler(0, 0, 0)    # euler angle to quaternion q=x,y,z,w

        transform.transform.rotation.x = q[0]    # assign values ​​to the rotated part
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]

        self.broadcaster_.sendTransform(transform)    # publish the static coordinate relation

        self.get_logger().info(f"publish TF: {transform}")

def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
