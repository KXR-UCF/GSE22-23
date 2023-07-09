import http.server
import socketserver
import os
from gpiozero import LED
import time
import influxdb_client
import serial
import re
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS
import datetime
import csv


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

token = "c3PVhNaPlnEEgNi6EyoGt-D4JUohV0IBZajfT3f8GZ1nsMeSUSl3LeR3DtDLRd1_HhswsK-WmRhGU_axOtQRmQ=="
org = "kxr"
url = "http://192.168.1.100:8086"
bucket = "kxr"
port = 9001

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=ASYNCHRONOUS)
global ser


def connect_ser():
    global ser
    ser = None
    path = '/dev/ttyACM0'

    while not os.path.exists(path):
        print(f"Device {path} does not exist.")

    print("Connected")

    ser = serial.Serial(port=port, baudrate=115200)


async def datacollect():
    connect_ser()

    ser.flushInput()
    ser.flushOutput()

    while True:
        if ser.in_waiting > 0:
            data = ser.read()
            p = influxdb_client.Point("DaleSr").from_dict(data)
            write_api.write(bucket=bucket, org=org, record=p)


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


        # print(self.path)
        # print(self.headers)
Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    # print("Http Server Serving at port", PORT)
    httpd.serve_forever()
    datacollect()
