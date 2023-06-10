import http.server 
import socketserver 
import serial 
import os
PORT = 9002
ser = serial.Serial(port = '/dev/ttyUSB0', baudrate = 115200) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
ser.flushInput()
ser.flushOutput() 
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    def do_POST(self):
        if(self.path == "/v"):
            ser.write('v'.encode())
        elif(self.path == "/vc"):
            ser.write('w'.encode())
        elif(self.path == "/f"):
            ser.write('f'.encode())
        elif(self.path == "/fc"):
            ser.write('g'.encode())
        elif(self.path == "/m"):
            ser.write('m'.encode())
        elif(self.path == "/mc"):
            ser.write('n'.encode())
        elif(self.path == "/e"):
            ser.write('e'.encode())
        elif(self.path == "/q"):
            ser.write('q'.encode())
        elif(self.path == 'a'):
            ser.write('a'.encode())
        elif(self.path == "/startdata"):
            os.spawnl(os.P_NOWAIT, './startdalejr', '/dev/null')
            #os.system('./startdalejr') 
        print(self.path)
        print(self.headers)
Handler = MyHttpRequestHandler
 
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()

