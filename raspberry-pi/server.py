import http.server
import socketserver
import os
from gpiozero import LED
import time
PORT = 9001
# Vent = ETH
# FILL = NOX

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
# isQDEnabled = False


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if (self.path == "/vent"):
            print("Vent")
            externalVEN.on()

        elif (self.path == "/ventclose"):
            print("Vent close")
            externalVEN.off()

        elif (self.path == "/fill"):

            print("Fill")
            externalFIL.on()

        elif (self.path == "/fillclose"):
            print("Fill close")
            externalFIL.off()

        elif (self.path == "/arm"):
            armFire.on()
            print("Arm E-Match")

        elif (self.path == "/disarm"):
            armFire.off()
            print("Disarm E-Match")

        elif (self.path == "/fire"):
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
            print("Close valves")
            externalQD.off()
            externalETH.off()
            externalNOX.off()
            externalIREC2.on()
            time.sleep(0.5)
            externalIREC2.off()

        elif (self.path == "/abort"):
            print("Abort")
            externalETH.off()
            externalNOX.on()

        elif (self.path == "/power"):
            print("Power on")
            externalPWR.on()

        elif (self.path == "/poweroff"):
            print("Power Off")
            externalPWR.off()

        elif (self.path == "/qd"):
            print("Quick Disconnect")
            externalQD.on()

        elif (self.path == '/qdreset'):
            print("QD Reset")
            externalQD.off()
        elif (self.path == '/siren'):
            print("Siren")
            externalSIR.on()
        elif (self.path == '/sirenoff'):
            print("Sirenoff")
            externalSIR.off()

        # print(self.path)
        # print(self.headers)
Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    # print("Http Server Serving at port", PORT)
    httpd.serve_forever()
