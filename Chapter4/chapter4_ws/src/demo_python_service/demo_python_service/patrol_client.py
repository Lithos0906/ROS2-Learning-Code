import rclpy
from rclpy.node import Node
from chapter4_interface.srv import Partol
import random

class PartolClient(Node):
    def __init__(self):
        super().__init__('turtle_controller_client_node')
        self.client = self.create_client(Partol, 'partol')
        self.get_logger().info(f"patrol client has been launched.")
        self.create_timer(10, self.send_request)

    def send_request(self):
        # 1.determine if the server is online
        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('waiting for the server to go online')

        # 2.structure Request
        request = Partol.Request()
        request.target_x = random.uniform(1,12)
        request.target_y = random.uniform(1,12)
        self.get_logger().info(f"Prepare the target point: {request.target_x}, {request.target_y}")
        
        # 3. send a request and wait for processing to complete
        future = self.client.call_async(request)
        
        def result_callback(result_future):
            response = result_future.result()    # obtain response
            if response.result==Partol.Response.SUCCESS:
                self.get_logger().info('Requesting patrol target point successful')
            if response.result==Partol.Response.FAIL:
                self.get_logger().info('Requesting patrol target point fail')

        future.add_done_callback(result_callback)


def main():
    rclpy.init()
    node = PartolClient()
    rclpy.spin(node)
    rclpy.shutdown()
