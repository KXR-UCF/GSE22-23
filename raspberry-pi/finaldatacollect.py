import serial
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
global ser


def connect_ser():
    ser_error = False
    global ser

    while True:
        try:
            ser = serial.Serial(port='/dev/ttyUSB2', baudrate=115200)
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
write_api = client.write_api(write_options=ASYNCHRONOUS)

test = influxdb_client.Point("test").field("t", 3)
write_api.write(bucket=bucket, org=org, record=test)
# with open('/home/kxr/' + str(datetime.datetime.now()), 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow(csvdata)
while True:
    try:
        data_raw = ser.readline()
        arr = data_raw.decode('UTF-8').split()
    except:
        connect_ser()

    # csvdata = []
    # csvdata.append(datetime.datetime.now().strftime("%H:%M:%S.%f"))
    # csvdata.extend(arr)

    # Write data to CSV file

    t1 = float(arr[1])
    t2 = float(arr[2])
    t3 = float(arr[3])
    thrust = t1+t2 + t3

    lc = influxdb_client.Point("LoadCell").field("Thrust", thrust).field("Thrust1", t1).field(
        "Thrust2", t2).field("Thrust3", t3).field("OxidizerTank", float(arr[0])).field("Mass", float(arr[6]))
    pt = influxdb_client.Point("PressureTransducer").field(
        "CombustionChamber", float(arr[4])).field("OxidizerTank", float(arr[5]))

    write_api.write(bucket=bucket, org=org, record=lc)
    write_api.write(bucket=bucket, org=org, record=pt)
    # write_api.write(bucket=bucket, org=org, record=ts)
