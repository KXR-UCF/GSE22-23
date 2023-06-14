import serial
import os
import time
# import websocket

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
ser.flushInput()
ser.flushOutput()

# websocket_url = "ws://"

# ws = websocket.Websocket()
# ws.connect(websocket_url)

while True:
    data = ser.readline().decode('UTF-8').strip()
    print(data)
    if (data == 'fill'):
        os.system('curl -X POST http://192.168.1.102:9001/fill')
    elif (data == 'fillclose'):
        os.system('curl -X POST http://192.168.1.102:9001/fillclose')
    elif (data == 'vent'):
        os.system('curl -X POST http://192.168.1.102:9001/vent')
    elif (data == 'ventclose'):
        os.system('curl -X POST http://192.168.1.102:9001/ventclose')
    elif (data == 'qd'):
        os.system('curl -X POST http://192.168.1.102:9001/qd')
    elif (data == 'arm'):
        os.system('curl -X POST http://192.168.1.102:9001/arm')
    elif (data == 'disarm'):
        os.system('curl -X POST http://192.168.1.102:9001/disarm')
    elif (data == 'fire'):
        os.system('curl -X POST http://192.168.1.102:9001/fire')
    elif (data == 'abort'):
        os.system('curl -X POST http://192.168.1.102:9001/abort')
    elif (data == 'power'):
        os.system('curl -X POST http://192.168.1.102:9001/power')
    elif (data == 'poweroff'):
        os.system('curl -X POST http://192.168.1.102:9001/poweroff')
    elif (data == 'closeall'):
        os.system('curl -X POST http://192.168.1.102:9001/closeall')
