import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster # static coordinate publisher
from geometry_msgs.msg import TransformStamped # message interface
from tf_transformations import quaternion_from_euler # euler angle to quaternion function
import math # angle to radians

class StaticTFBroadcaster(Node):
    def __init__(self):
        super().__init__('static_tf_broadcaster')
        self.static_broadcaster_ = StaticTransformBroadcaster(self)
        self.publish_static_tf()

    def publish_static_tf(self):
        # publish the static coordinate
        # the coordinate relation between base_link and camera_link
        transform = TransformStamped()
        transform.header.frame_id = 'base_link'     # define the header point
        transform.child_frame_id = 'camera_link'    # define the child point
        transform.header.stamp = self.get_clock().now().to_msg()    # get the time stamp

        transform.transform.translation.x = 0.5     # set the relation of coordinate
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.6
        
        q = quaternion_from_euler(math.radians(180), 0, 0)    # euler angle to quaternion q=x,y,z,w

        transform.transform.rotation.x = q[0]    # assign values ​​to the rotated part
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]

        self.static_broadcaster_.sendTransform(transform)    # publish the static coordinate relation

        self.get_logger().info(f"publish static TF: {transform}")

def main():
    rclpy.init()
    node = StaticTFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
