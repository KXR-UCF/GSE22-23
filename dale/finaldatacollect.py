import serial
import influxdb_client
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS
from time import sleep
token = "jwrod6dhQ-fsQRioNkXahfzXRFiTRHy1OH3ZVahlHmoH-OahKVVYI3Elhr2Z8uZl9S5XNIncDM6PS1o-2cFUnw=="
org = "kxr"
url = "http://192.168.1.100:8086"
bucket = "DaleJR"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
global ser


def connect_ser():
    ser_error = False
    global ser

    while True:
        try:
            ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
            ser_error = False

        except:
            ser_error = True
            pass

        if ser_error:
            print("sleepy")
            ser_error = False
            time.sleep(2)
        else:
            print("success")
            break


connect_ser()

ser.flushInput()
ser.flushOutput()
# sleep(10)
# print("qweqwh")
write_api = client.write_api(write_options=ASYNCHRONOUS)

test = influxdb_client.Point("test").field("t", 3)
write_api.write(bucket=bucket, org=org, record=test)
while True:
    try:
        data_raw = ser.readline()
        arr = data_raw.decode('UTF-8').split()
    except:
        connect_ser()

    # print(arr)

    t1 = float(arr[1])
    t2 = float(arr[2])
    t3 = float(arr[3])
    thrust = t1+t2 + t3

    lc = influxdb_client.Point("LoadCell").field("Thrust", thrust).field("Thrust1", t1).field(
        "Thrust2", t2).field("Thrust3", t3).field("OxidizerTank", float(arr[0]))
    pt = influxdb_client.Point("PressureTransducer")
    # try to get Combustion Chamber
    try:
        pt = pt.field("CombustionChamber", int(arr[4]))
    except:
        print("CombustionChamber is not connected")
    # try to see if there is any Oxidizer Pressure data
    try:
        pt = pt.field("OxidizerTank", int(arr[5]))
    except:
        print("OxidizerTank is not Connected")
    # ts = influxdb_client.Point("TemperatureSensor").field("Temp1", int(arr[6])).field("Temp2", int(arr[7]))

    write_api.write(bucket=bucket, org=org, record=lc)
    write_api.write(bucket=bucket, org=org, record=pt)
    # write_api.write(bucket=bucket, org=org, record=ts)
