import asyncio
import websockets
import serial
import json
from gpiozero import LED
import time
import datetime

fire = LED(21)
armFire = LED(26)
externalETH = LED(2)
externalNOX = LED(3)
externalFIL = LED(25)
externalVEN = LED(8)
externalPWR = LED(20)

state = {
    'Time': datetime.datetime.now(),
    'Type': 'State',
    'Vent': 'Close',
    'Fill': 'Close',
    'Chamber': 'Close',
    'Ematch': 'Disarmed',
    'Power': 'Off'
}

# Reads in commands from CHIP and send back what state its in


async def handle_message(websocket, message):
    if message == 'fire':
        print("Fire!!")
        fire.on()
        time.sleep(0.25)
        externalETH.on()
        externalNOX.on()
        time.sleep(0.1)
        fire.off()
        state['Chamber'] = 'Close'
    elif message == 'vent':
        print("Vent")
        externalVEN.on()
        state['Vent'] = 'Open'
    elif message == 'ventclose':
        print("Vent close")
        externalVEN.off()
        state['Vent'] = 'Close'
    elif message == 'fill':
        print("Fill")
        externalFIL.on()
        state['Fill'] = 'Open'
    elif message == 'fillclose':
        print("Fill close")
        externalFIL.off()
        state['Fill'] = 'Close'
    elif message == 'arm':
        armFire.on()
        print("Arm E-Match")
        state['Ematch'] = 'Armed'
    elif message == 'disarm':
        armFire.off()
        print("Disarm E-Match")
        state['Ematch'] = 'Disarmed'
    elif message == 'closeall':
        print("Close valves")
        externalETH.off()
        externalNOX.off()
        state['Servos'] = 'Close'
    elif message == 'abort':
        print("Abort")
        externalETH.off()
        externalNOX.on()
        state['Servos'] = 'Abort'
    elif message == 'power':
        print("Power on")
        externalPWR.on()
        state['Power'] = 'On'
    elif message == 'poweroff':
        print("Power Off")
        externalPWR.off()
        state['Power'] = 'Off'

    state['time'] = datetime.datetime.now()

    json_data = json.dumps(state)

    await websocket.send(json_data)


async def serial_setup():
    global ser
    ser_error = False

    while True:
        try:
            ser = serial.Serial(port='/dev/ttyAMA0',
                                baudrate=115200, timeout=2)
            ser_error = False

        except Exception as e:
            print(str(e))
            ser_error = True
            pass

        if ser_error:
            print("sleepy")
            ser_error = False
            time.sleep(2)
        else:
            print("success")
            break

    ser.flushInput()
    ser.flushOutput()


async def websocket_handler(websocket, path):

    while True:
        message = await websocket.recv()
        print("Received:", message)
        await handle_message(websocket, message)


async def send_data(websocket):
    while True:
        # Read data from serial port
        data_raw = ser.readline()
        arr = data_raw.decode('UTF-8').split()

        # Create a data dictionary
        data = {
            'Time': datetime.datetime.now(),
            'Type': 'data',
            'T1': float(arr[1]),
            'T2': float(arr[2]),
            'T3': float(arr[3]),
            'Thrust': float(arr[1]) + float(arr[2]) + float(arr[3]),
            'Oxidizer': float(arr[0]),
            'P1': float(arr[4]),
            'P2': float(arr[5]),
        }

        # Convert data to JSON format
        json_data = json.dumps(data)

        # Send the WebSocket message
        await websocket.send(json_data)

        # Adjust the sleep duration as per your requirements
        await asyncio.sleep(1)


async def main():
    loop = asyncio.get_running_loop()

    # Start the WebSocket server
    start_server = await websockets.serve(websocket_handler, '0.0.0.0', 8765, loop=loop)
    await serial_setup()
    print("WebSocket server started")

    # Create a separate task for sending serial data
    serial_task = loop.create_task(
        send_data(start_server))

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        fire.off()
        armFire.off()
        externalETH.off()
        externalNOX.off()
        externalFIL.off()
        externalVEN.off()
        externalPWR.off()
        ser.close()
        serial_task.cancel()

asyncio.run(main())
