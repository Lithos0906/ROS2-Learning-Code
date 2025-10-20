import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node = Node('python_node')
    node.get_logger().info('Hello Python Node!')
    node.get_logger().warn('Hello Python Node!')
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
