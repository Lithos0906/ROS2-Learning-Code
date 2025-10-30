import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory
import os

def main():
    # obatin the real path of the pic
    default_image_path = os.path.join(get_package_share_directory('demo_python_service'), 'resource/default.jpg')
    print(f"the real path of the pic{default_image_path}")
    # using cv2 loading pic
    image = cv2.imread(default_image_path)
    # detect faces
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample = 1, model = 'hog')
    # draw the face frame
    for top, right, bottom, left in face_locations:
        cv2.rectangle(image, (left,top), (right,bottom), (255,0,0), 4)
    # result
    cv2.imshow('Face Detect Result', image)
    cv2.waitKey(0)
