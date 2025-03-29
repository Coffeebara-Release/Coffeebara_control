"""
import cv2
import time
import sys
import requests

from serialcomm import SerialComm
from detector import Cup, CupDetector 
from socket
"""

"""
class StateMachine:
    PY_RESET     = 0
    PY_READY     = 1
    PY_START     = 2
    PY_DETECTING = 3
    PY_DETECTED  = 4

    def __init__(self, serialComm, cupDetector):
        self.serial_comm = serialComm
        self.detector = cupDetector
        self.current_state = self.PY_RESET
        self.webcam = None

    def update(self):
        if self.current_state == self.PY_RESET:
            self._reset()
        elif self.current_state == self.PY_READY:
            self._wait_for_ready()
        elif self.current_state == self.PY_START:
            self._start_camera()
        elif self.current_state == self.PY_DETECTING:
            self._detect_objects()
        elif self.current_state == self.PY_DETECTED:
            self._wait_for_completion()
    
    def _reset(self):
        time.sleep(1)
        print("reset")
        self.current_state = PY_READY

    def _wait_for_ready(self):
        if self.serial_comm.is_ready():
            self.current_state = self.PY_START

    def _start_camera(self):
        self.webcam = cv2.VideoCapture(2)
        if self.webcam.isOpened():
            print("webcam connected!")
            self.current_state = self.PY_DETECTING

    def _detect_objects(self):
        ret, frame = self.webcam.read()
        
        _cnt = 0
        while ret is False:
            self.webcam = cv2.VideoCapture(2)
            dots, spaces, _cnt = "." * (_cnt := (_cnt + 1) % 5), " " * (5 - _cnt), _cnt
            sys.stdout.write(f"\rcheck webcam{dots}{spaces}")  
            sys.stdout.flush()
            time.sleep(0.1)

        print("Webcam is opened")

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        cup, entrance, holder = self.detector.detect_objects(frame)

        command = self._generate_command(cup, entrance, holder)
        self.serial_comm.send_command(command)

        self.current_state = self.PY_DETECTED

    def _wait_for_completion(self):
        waste_weight = self.serial_comm.readResponse()
        while waste_weight is None:
            waste_weight = self.serial_comm.readResponse()

        waste_weight = int(waste_weight.decode()[:-2])

        waste_data = {
            'deviceId' : 1,
            'capacity' : waste_weight
        }
        server_response = requests.patch(, json=waste_data)
        print(server_response.status_code)
        print(server_response.json())
        self.webcam.release()
        

    def _generate_command(self, cup: DetectedObject, entrance: DetectedObject, holder: DetectedObject)
        if not cup or not entrance:
            return 0x00
        command = 0x01 if holder else 0x00
        return int(command << 2)
"""