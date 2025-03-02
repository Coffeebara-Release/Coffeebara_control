from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import serial
import time
import math

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import requests

tx_rx_data = 0x00

# cup, entrance, holder, straw class id 정의
cup_class_id      = 0
entrance_class_id = 1
holder_class_id   = 2
straw_class_id    = 3

# python 메인 프로그램 state machine 정의
PY_RESET          = 0
PY_READY          = 1
PY_START          = 2
PY_DETECTING      = 3
PY_DETECTED       = 4

current_state = PY_RESET

# 디바이스 state machine 정의
ONLY_WAITING                = 0
RESET                       = 1
RESET_QUEUE                 = 2 
RESET_SERVO                 = 3
RESET_HORIZONTAL_INTERRUPT  = 4 
RESET_HORIZONTAL_DEFAULT    = 5 
RESET_VERTICAL_DEFAULT      = 6
STARTING                    = 7
VERTICAL_HOLD_CUP           = 8
VERTICAL_REMOVE_LID_HOLDER  = 9
HORIZONTAL_HOLD_HOLDER      = 10
HORIZONTAL_PLACE_HOLDER     = 11
HORIZONTAL_HOLD_CUP         = 12
HORIZONTAL_WASTE_CUP        = 13
HORIZONTAL_WASH_CUP         = 14
HORIZONTAL_LOAD_CUP         = 15

model = None

# 시리얼 통신을 위한 연결
py_serial = serial.Serial(
    port = "/dev/ttyUSB0",
    baudrate = 9600
)

# 로컬 서버와의 통신을 위한 URL 호출
server_URL = 'http://203.252.136.226:8080/device'

# 로컬 서버 개방 및 SocketIO 연결
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins = '*')

class Cup:
    def __init__(self, x1, y1, x2, y2, width, height):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.height = height

class Entrance:
    def __init__(self, x1, y1, x2, y2, width, height):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.height = height

class Holder:
    def __init__(self, x1, y1, x2, y2, width, height):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.height = height

model_path = "./model.pt"
webcam = None

# command[0] : holder, command[1 : 2] : 컵 크기에 따른 size, command[3 : 4] : entrance 크기에 따른 size
# binary 기준
# 00 : None
# 01 : small
# 10 : regular
# 11 : large
def results_processing(largest_cup, largest_entrance, largest_holder):
    command = 0x00

    # 아예 인식되지 않은 경우는 바로 리턴
    if largest_cup is None or largest_entrance is None:
        print("there's no cup")
        return command
    
    # 홀더 유무
    if largest_holder:
        print("w. Holder ")
        command = command | 0x01
    else:
        print("wo. Holder")

    command = command << 2

    # 컵 크기에 따른 size
    entrance_2_cup = largest_cup.y2 - largest_entrance.y2
    if entrance_2_cup >= 420:
        print("Cup size : Large")
        command = command | 0x03
    elif entrance_2_cup < 420 and entrance_2_cup > 350:
        print("Cup size : Regular")
        command = command | 0x02
    else:
        print("Cup size : Small")
        command = command | 0x01

    command = command << 2

    # entrance 크기에 따른 size
    entrance_x_diff = largest_entrance.x2 - largest_entrance.x1
    if entrance_x_diff >= 280:
        print("Ent size : Large")
        command = command | 0x03
    elif entrance_x_diff < 280 and entrance_x_diff > 255:
        print("Ent size : Regular")
        command = command | 0x02
    else:
        print("Ent size : Small")
        command = command | 0x01

    command = command << 3
    return command

    # 인식된 컵 없는 경우 'F' 리턴
    # 인식된 컵이 있는 경우 command 리턴

def state_update():
    global RESET, READY, START, DETECTING, DETECTED, model_path, webcam, current_state, model
    global tx_rx_data
    tx_rx_data = 0x00
    
    response = None
    print(current_state)

    if py_serial.readable(): # 시리얼 연결 활성화된 경우 
        
        # 초기 설정 state
        if current_state == PY_RESET: 
            time.sleep(5)
            model = YOLO(model_path) # AI 모델 호출
            print("model loaded")
            current_state = PY_READY
            return
        
        # python 프로그램 활성화 state
        elif current_state == PY_READY:
            while ((tx_rx_data >> 7) & 0x01) == 0: # 아두이노로부터 1000_0000 신호가 수신될 때까지 (컵 인식 준비가 될 때까지) 시리얼 데이터 수신
                tx_rx_data = py_serial.readline()
                tx_rx_data = int(tx_rx_data.decode()[:-2])

            current_state = PY_START
            return

        # 웹캠 활성화 state
        elif current_state == PY_START:
            webcam = cv2.VideoCapture(2)
            while (webcam.isOpened()) == None:
                webcam = cv2.VideoCapture(2)
                time.sleep(0.1)

            print("Webcam is opened")
            current_state = PY_DETECTING
            return

        # 프레임 호출 및 컵 정보 처리 state
        elif current_state == PY_DETECTING:
            ret, frame = webcam.read()
            while ret is False:
                print("Capture video")
                ret, frame = webcam.read()

            largest_cup = None
            largest_entrance = None
            largest_holder = None

            # 모델 results 저장
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            results = model(frame,imgsz = (320,320))

            for result in results:
                for box in result.boxes:
                    confidence = math.ceil((box.conf[0]*100))/100
                    
                    # bounding box를 활용한 너비, 높이 저장
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    width = x2 - x1
                    height = y2 - y1
                    print(confidence, int(box.cls[0]), width, height)

                    # confidence가 너무 낮거나 인식된 클래스의 크기가 너무 크거나 작은 경우 제거
                    if confidence < 0.6 or width > 350 or width < 200: 
                        continue

                    object_size = width * height
                    class_id = int(box.cls[0])

                    # 각 클래스의 가장 큰 요소를 largest_ 객체에 저장
                    if class_id == cup_class_id:
                        if largest_cup is None or object_size > (largest_cup.width * largest_cup.height):
                            largest_cup = Cup(x1, y1, x2, y2, width, height)

                    elif class_id == entrance_class_id:
                        if largest_entrance is None or object_size > (largest_entrance.width * largest_entrance.height):
                            largest_entrance = Entrance(x1, y1, x2, y2, width, height)
                                
                    elif class_id == holder_class_id:
                        if largest_holder is None or object_size > (largest_holder.width * largest_holder.height):
                            largest_holder = Holder(x1, y1, x2, y2, width, height)

            # 홀더 유무, 컵 & 입구 크기 처리 결과 저장
            command = results_processing(largest_cup, largest_entrance, largest_holder) 
            print("command", command)

            # socketio 송신을 통한 디바이스 UI 갱신
            socketio.emit('cup update', {'cup' : command})  

            # 시리얼 통신을 통한 컵 정보 전달
            py_serial.write(command.to_bytes(1, byteorder='big'))
            time.sleep(0.1)
            
            current_state = PY_DETECTED
            return

        # 컵 인식 후 디바이스 UI 갱신을 위한 디바이스 state machine 수신 state
        elif current_state == PY_DETECTED:
            webcam.release()

            while True:
                response = py_serial.readline()
                while response is None:
                    response = py_serial.readline()

                response = int(response.decode()[:-2])

                # 현재 아두이노에서 처리중인 컵이 없는 경우 초기 state로 변경
                if response & (1 << 7) : 
                    current_state = PY_READY
                    return

                # 디바이스 state response에 저장
                # 해당 response를 특정 분기마다 디바이스 UI js파일로 전송하여 UI 갱신
                response = response >> 3

                # 디바이스 state가 '분리' 인 경우 
                if response == VERTICAL_HOLD_CUP :
                    socketio.emit('state update', {'state' : 1})
                
                # 디바이스 state가 '세척' 인 경우 
                elif response == HORIZONTAL_WASTE_CUP or response == HORIZONTAL_WASH_CUP:
                    socketio.emit('state update', {'state' : 2})
                
                # 디바이스 state가 '적재' 인 경우 
                elif response == HORIZONTAL_LOAD_CUP:
                    socketio.emit('state update', {'state' : 3})
                    
                time.sleep(0.1)

                print(response)

                # 디바이스 state가 적재인 경우 : 내부 컵 처리 종료된 상태
                if response == HORIZONTAL_LOAD_CUP:
                    
                    # 아두이노 로드셀로부터 폐수 무게 호출
                    waste_weight = py_serial.readline()
                    while waste_weight is None:
                        waste_weight = py_serial.readline()

                    waste_weight = int(waste_weight.decode()[:-2])

                    # 폐수 무게와 디바이스 정보를 json 형태로 로컬 서버로 patch
                    waste_data = {
                        'deviceId' : 1,
                        'capacity' : waste_weight
                    }
                    server_response = requests.patch(server_URL, json=waste_data)
                    print(server_response.status_code)
                    print(server_response.json())

                    time.sleep(0.3)
                    current_state = PY_READY
                    return

    else:
        print("Serial disconnected")
        return
    
@app.route('/')
def index():
    return render_template('UI_test.html')

def start_state_update_loop():
    while True:
        state_update()

if __name__ == "__main__":
    socketio.start_background_task(target=start_state_update_loop)
    socketio.run(app, host = 'localhost', port = 5115, debug = True)