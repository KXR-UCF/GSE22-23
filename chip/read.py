import serial
import os
ser = serial.Serial(port = '/dev/ttyUSB0', baudrate = 115200)
ser.flushInput()
ser.flushOutput()
while True:
    data = ser.readline().decode('UTF-8').strip()
    print(data)
    if(data == 'f'):
        os.spawnl(os.P_NOWAIT, 'curl -X POST http://192.168.1.101:9001/f', '/dev/null')
    elif(data == 'fc'):
        os.spawnl(os.P_NOWAIT, 'curl -X POST http://192.168.1.101:9001/fc', '/dev/null')
    elif(data ==  'v'):
        os.spawnl(os.P_NOWAIT, 'curl -X POST http://192.168.1.101:9001/v', '/dev/null')
    elif(data == 'vc'):
        os.spawnl(os.P_NOWAIT, 'curl -X POST http://192.168.1.101:9001/vc', '/dev/null')
    elif(data == 'q'):
        os.spawnl(os.P_NOWAIT, 'curl -X POST http://192.168.1.101:9001/q', '/dev/null')
    elif(data == 'm'):
        os.spawnl(os.P_NOWAIT, 'curl -X POST http://192.168.1.101:9001/m', '/dev/null')
    elif(data == 'mc'):
        os.spawnl(os.P_NOWAIT, 'curl -X POST http://192.168.1.101:9001/mc', '/dev/null')
    elif(data == 'e'):
        os.spawnl(os.P_NOWAIT, 'curl -X POST http://192.168.1.101:9001/e', '/dev/null')
    elif(data == 'a'):
        os.spawnl(os.P_NOWAIT, 'curl -X POST http://192.168.1.101:9001/a', '/dev/null')

