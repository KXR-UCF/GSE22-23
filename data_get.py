import websocket
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision

# InfluxDB connection details
url = "http://192.168.1.101:8086"
token = "wsBdGMCQTrwXjuKu8JeuhpeB8dPzOaa5MT712Crheh62z5bndGDw2RamHOlnRA3EkShZnpWhepB60qIpNz6uFQ=="
org = "kxr"
bucket = "data"
websocket_url = "ws://<websocket_endpoint>"

# Establish a WebSocket connection
# ws = websocket.WebSocket()
# ws.connect(websocket_url)

# InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

# Fetch all measurements
query = f'from(bucket: "{bucket}") |> range(start: 0)'
tables = client.query_api().query(query)
measurements = [table['name'] for table in tables]

# Subscribe to real-time data updates for each measurement
for measurement in measurements:
    subscription_query = f'stream from(bucket: "{bucket}") |> filter(fn: (r) => r._measurement == "{measurement}")'
    subscription = client.query_api().query_stream(subscription_query)

    # Send data through WebSocket
    for table in subscription:
        data = json.dumps(table)
        print(data)
        # ws.send(data)

# ws.close()
