import rclpy
from rclpy.node import Node
from chapter4_interface.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory
import os
from cv_bridge import CvBridge
import time
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        self.client = self.create_client(FaceDetector, 'face_detect')
        self.bridge = CvBridge()
        self.friends_image_path = os.path.join(get_package_share_directory('demo_python_service'), 'resource/friends.jpg')
        self.get_logger().info(f"face detect client has been launched.")
        self.image = cv2.imread(self.friends_image_path)

    def call_set_parameters(self, parameters):
        # 1.creating a client, wait for the service to go online
        update_param_client = self.create_client(SetParameters, '/face_detect_node/set_parameters')
        while update_param_client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('waiting for the params update server to go online')

        # 2.structure request
        request = SetParameters.Request()
        request.parameters = parameters

        # 3.call the server to update parameters
        future = update_param_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)    # waiting for the service to complete
        response = future.result()    # obtain response
        return response

    def update_detect_model(self, model='hog'):
        # 1.create a param orient
        param = Parameter()
        param.name = 'model'

        # 2.cope values
        param_value = ParameterValue()
        param_value.string_value = model
        param_value.type = ParameterType.PARAMETER_STRING
        param.value = param_value

        # 3.request to update params
        response = self.call_set_parameters([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f"set the result of params: {result.successful} {result.reason}")

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
        # rclpy.spin_until_future_complete(self, future)    # waiting for the service to complete
        def result_callback(result_future):
            response = result_future.result()    # obtain response
            self.get_logger().info(f'receive the response, {response.number} faces was detected, time consuming {response.use_time}s')
            # self.show_response(response)

        future.add_done_callback(result_callback)
        
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
    # node.update_detect_model('hog')
    # node.send_request()
    node.update_detect_model('cnn')
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()
