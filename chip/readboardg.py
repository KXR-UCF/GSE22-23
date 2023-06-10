import serial
import os
ser = serial.Serial(port = '/dev/ttyUSB0', baudrate = 115200)
ser.flushInput()
ser.flushOutput()
while True:
    data = ser.readline().decode('UTF-8').strip()
    print(data)
    if(data == 'f'):
        os.system('curl -X POST http://192.168.1.102:9001/f')
    elif(data == 'fc'):
        os.system('curl -X POST http://192.168.1.102:9001/fc')
    elif(data ==  'v'):
        os.system('curl -X POST http://192.168.1.102:9001/v')
    elif(data == 'vc'):
        os.system('curl -X POST http://192.168.1.102:9001/vc')
    elif(data == 'q'):
        os.system('curl -X POST http://192.168.1.102:9001/q')
    elif(data == 'm'):
        os.system('curl -X POST http://192.168.1.102:9001/m')
    elif(data == 'mc'):
        os.system('curl -X POST http://192.168.1.102:9001/mc')
    elif(data == 'e'):
        os.system('curl -X POST http://192.168.1.102:9001/e')
    elif(data == 'a'):
        os.system('curl -X POST http://192.168.1.102:9001/a')

