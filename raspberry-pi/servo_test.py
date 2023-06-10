import http.server
import socketserver
import os
from gpiozero import LED
import time
PORT = 9001

"""Part of the 3 servo reciever code cinematic universe"""

# Pins based on bits
# VEN - 0
# FIL - 1
# NOX - 2
# ETH - 3
# 1 = OPEN, 0 = Close, X = Previous State/Doesnt Matter
# Concept Behind This Code:
# State      | DPF | IREC
# ------------------------------------------
# Close ALL  | 0000 | 00X0
# Fire       | 0011 | 00X1
# Abort      | 0010 | 00X0
# Fill       | 0100 | 01X0
# Vent       | 1000 | 10X0
# Close Vent | 0XXX | 0XXX
# Close Fill | X0XX | X0XX
# fire - 17
# armFire - 27
# fill - 22
# externalETH - 23
# externalNOX - 24
# externalFIL - 25


fire = LED(17)
armFire = LED(27)
externalETH = LED(23)
externalNOX = LED(24)
externalFIL = LED(25)
externalVEN = LED(26)

externalETH.on()
