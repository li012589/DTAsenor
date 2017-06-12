#import os
#import sys
import math

import serial

jy_sensor = serial.Serial(port="/dev/ttyUSB0", baudrate="9600", timeout=1)
print(jy_sensor.name)
while True:
    data = jy_sensor.read(size=1)
    if data == b'\x55':
        print("success!")
        jy_sensor.read(size=10)
        break;
    print("trying", data)

try:
    while True:
        data = jy_sensor.read(size=11)
        if not len(data) == 11:
            print('byte error:', len(data))
            break
        #Angle
        if data[1] == 83:
            x = int.from_bytes(data[2:4], byteorder='little')/32768*180
            y = int.from_bytes(data[4:6], byteorder='little')/32768*180
            z = int.from_bytes(data[6:8], byteorder='little')/32768*180
            print("Angle output:{}, {}, {}".format(x, y, z))
        #Acceleration
except KeyboardInterrupt:
    jy_sensor.close()
    print("close port")