import asyncio
import threading
import socketserver
import http.server
import serial
import os
import time
import influxdb_client
from gpiozero import LED
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS

# Servo Handling
fire = LED(17)
armFire = LED(27)
externalETH = LED(23)
externalNOX = LED(24)
externalFIL = LED(8)
externalVEN = LED(7)
externalPWR = LED(22)
externalIREC1 = LED(0)
externalIREC2 = LED(5)
externalSIR = LED(13)
externalQD = LED(6)
port = 9001

# InfluxDB Client
token = "c3PVhNaPlnEEgNi6EyoGt-D4JUohV0IBZajfT3f8GZ1nsMeSUSl3LeR3DtDLRd1_HhswsK-WmRhGU_axOtQRmQ=="
org = "kxr"
url = "http://192.168.1.100:8086"
bucket = "kxr"

# Teensy 4.1 details
serial_port = '/dev/ttyACM1'
baud_rate = 115200
global ser

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=ASYNCHRONOUS)

# Connect to the teensy 4.1
async def connect_ser():
    global ser
    while not os.path.exists(serial_port):
        print(f"Device {serial_port} does not exist.")
        await asyncio.sleep(1)

    ser = serial.Serial(port=serial_port, baudrate=baud_rate)
    print(f"Device {serial_port} Connected")

# Datacollection system
async def datacollect():
    print("datacollect")
    ser.flushInput()
    ser.flushOutput()

    while True:
        if ser.in_waiting > 0:
            data_raw = ser.readline()
            arr = data_raw.decode('UTF-8').split()
            # TODO: Make the Teensy worry about making the Object
            data = {
                "measurement": "DaleSr",
                "fields": {
                    "thrust1": float(arr[0]),
                    "thrust2": float(arr[1]),
                    "thrust3": float(arr[2]),
                    "thrust": float(arr[0])+float(arr[1])+float(arr[2]),
                    "mass": float(arr[3]),
                    "pt1": float(arr[4]),
                    "pt2": float(arr[5]),
                    "tc1": float(arr[6]),
                    "tc2": float(arr[7]),
                    }
            }

            p = Point.from_dict(data, WritePrecision.NS)
            write_api.write(bucket=bucket, org=org, record=p)


def httpserver():
    print("http")
    # HTTP handler
    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.path = 'index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        def do_POST(self):
            p = influxdb_client.Point("Dale")

            if (self.path == "/vent"):
                p.field("command", "vent")
                print("Vent")
                externalVEN.on()

            elif (self.path == "/ventclose"):
                p.field("command", "ventclose")
                print("Vent close")
                externalVEN.off()

            elif (self.path == "/fill"):
                p.field("command", "fill")
                print("Fill")
                externalFIL.on()

            elif (self.path == "/fillclose"):
                p.field("command", "fillclose")
                print("Fill close")
                externalFIL.off()

            elif (self.path == "/arm"):
                p.field("command", "arm")
                armFire.on()
                print("Arm E-Match")

            elif (self.path == "/disarm"):
                p.field("command", "disarm")
                armFire.off()
                print("Disarm E-Match")

            elif (self.path == "/fire"):
                p.field("command", "fire")
                print("Fire!!")
                fire.on()
                time.sleep(0.3)
                externalETH.on()
                externalNOX.on()
                externalIREC1.on()
                time.sleep(0.05)
                externalIREC1.off()
                time.sleep(0.1)
                fire.off()

            elif (self.path == "/closeall"):
                p.field("command", "closeall")
                externalQD.off()
                externalETH.off()
                externalNOX.off()
                externalIREC2.on()
                time.sleep(0.5)
                externalIREC2.off()

            elif (self.path == "/abort"):
                p.field("command", "abort")
                print("Abort")
                externalETH.off()
                externalNOX.on()

            elif (self.path == "/power"):
                p.field("command", "power")
                print("Power on")
                externalPWR.on()

            elif (self.path == "/poweroff"):
                p.field("command", "poweroff")
                print("Power Off")
                externalPWR.off()

            elif (self.path == "/qd"):
                p.field("command", "qd")
                print("Quick Disconnect")
                externalQD.on()

            elif (self.path == '/qdreset'):
                p.field("command", "qdreset")
                print("QD Reset")
                externalQD.off()
            elif (self.path == '/siren'):
                p.field("command", "siren")
                print("Siren")
                externalSIR.on()
            elif (self.path == '/sirenoff'):
                p.field("command", "sirenoff")
                print("Sirenoff")
                externalSIR.off()

            write_api.write(bucket=bucket, org=org, record=p)
            self.send_response(200)


    Handler = MyHttpRequestHandler

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()

async def main():

    # HTTP server is on a separate thread due to I/O restrictions with datacollection
    http_server_thread = threading.Thread(target=httpserver)
    http_server_thread.start()

    await connect_ser()
    # Run data collection task
    data_collection_task = asyncio.create_task(datacollect())

    # Wait for the data collection task to "complete"
    await data_collection_task

    # Stop the HTTP server thread
    http_server_thread.join()


# Run the main function
asyncio.run(main())
