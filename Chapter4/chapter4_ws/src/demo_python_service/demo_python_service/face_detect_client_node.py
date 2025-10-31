import rclpy
from rclpy.node import Node
from chapter4_interface.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory
import os
from cv_bridge import CvBridge
import time

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        self.client = self.create_client(FaceDetector, 'face_detect')
        self.bridge = CvBridge()
        self.friends_image_path = os.path.join(get_package_share_directory('demo_python_service'), 'resource/friends.jpg')
        self.get_logger().info(f"face detect client has been launched.")
        self.image = cv2.imread(self.friends_image_path)

    def send_request(self):
        # 1.determine if the server is online
        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('waiting for the server to go online')
        # 2.structure Request
        request = FaceDetector.Request()
        request.image = self.bridge.cv2_to_imgmsg(self.image)
        # 3. send a request and wait for processing to complete
        future = self.client.call_async(request)
        # while not future.done():
        #     time.sleep(1.0)    # the current thread will be put to sleep, waiting for the service to complete
        rclpy.spin_until_future_complete(self, future)    # waiting for the service to complete
        response = future.result()    # obtain response
        self.get_logger().info(f'receive the response, {response.number} faces was detected, time consuming {response.use_time}s')
        self.show_response(response)

    def show_response(self, response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]
            cv2.rectangle(self.image, (left,top), (right,bottom), (255,0,0), 4)

        cv2.imshow('Face Detect Result', self.image)
        cv2.waitKey(0)


def main():
    rclpy.init()
    node = FaceDetectClientNode()
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()
