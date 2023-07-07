import serial
import re
import influxdb_client
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS
from time import sleep
import datetime
import csv
token = "c3PVhNaPlnEEgNi6EyoGt-D4JUohV0IBZajfT3f8GZ1nsMeSUSl3LeR3DtDLRd1_HhswsK-WmRhGU_axOtQRmQ=="
org = "kxr"
url = "http://192.168.1.100:8086"
bucket = "kxr"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


def connect_ser(pattern):
    global ser
    ser = None
    available_ports = list(serial.tools.list_ports.comports())

    for port in available_ports:
        port_name = port.device
        if port_name.startswith('/dev/ttyUSB'):
            try:
                ser = serial.Serial(port_name)
                while True:
                    line = ser.readline().decode().strip()
                    if re.match(pattern, line):
                        break  # Found a matching value, exit the loop
            except serial.SerialException:
                # Port is unavailable or cannot be opened
                pass

    if ser is not None:
        # Port was successfully opened and validated, return the serial port instance
        return ser
    else:
        # No matching port found, return None
        return None


connect_ser()

ser.flushInput()
ser.flushOutput()

write_api = client.write_api(write_options=ASYNCHRONOUS)

while True:
    if ser.in_waiting > 0:
        data = ser.read()
        p = influxdb_client.Point("DaleSr").from_dict(data)
        write_api.write(bucket=bucket, org=org, record=p)
