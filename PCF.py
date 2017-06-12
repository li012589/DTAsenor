import smbus
import time
import math
import serial

I2Cbus = smbus.SMBus(1)
ADaddress = 0x48

while True:
    I2Cbus.write_byte(ADaddress,0x41)
    time.sleep(0.5)
    a1 = []
    for i in range(1,10):
        a1.append(I2Cbus.read_byte(ADaddress)/float(255)*5)
    a1.remove(max(a1))
    a1.remove(min(a1))
    a1 = sum(a1)/len(a1)
    #time.sleep(0.5)
    I2Cbus.write_byte(ADaddress,0x40)
    time.sleep(0.5)
    a0 = []
    for i in range(1,10):
        a0.append(I2Cbus.read_byte(ADaddress)/float(255)*5)
    a0.remove(max(a0))
    a0.remove(min(a0))
    a0 = sum(a0)/len(a0)
    #time.sleep(0.5)
    if a0>=1.05 and a0<1.25:
        distance = -50*a0+112.5
    elif a0>=1.25 and a0<1.5:
        distance = -40*a0+100
    elif a0>=1.5 and a0 <=2.5:
        distance = -20*a0+70
    else:
        distance = -1

    temp = 50*a1-53
    #print("a0:")
    #print(a0)
    #print("a1;")
    #print(a1)
    print("distance:")
    print(distance)
    print("temperture")
    print(temp)
