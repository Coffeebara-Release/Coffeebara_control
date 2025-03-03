"""
import serial
import sys
import time

"""

"""
class SerialComm:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port, baudrate)

    @property
    def isReady(self):
        _cnt = 0

        if self.serial.readable():
            dots, spaces, _cnt = "." * (_cnt := (_cnt + 1) % 5), " " * (5 - _cnt), _cnt
            sys.stdout.write(f"\rconnecting{dots}{spaces}")  
            sys.stdout.flush()
            time.sleep(0.1)
            
            try:
                data = int(self.serial.readline().decode().strip())
                return (data >> 7) & 0x01 == 1
            except ValueError:
                pass
            continue
        
        return False

    def sendCommand(self, command):
        _ret = self.serial.write(command.to_bytes(1, byteorder='big'))
        print("{0} {1} bytes written".format('Success!' if _ret == 1 else 'Error!', _ret))

    def readResponse(self):
        if self.serial.readable():
            data = self.serial.readline().decode().strip()
            return int(data)
        return None   
"""