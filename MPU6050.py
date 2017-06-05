import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
address = 0x68

Xdata = 0x43
Ydata = 0x45
Zdata = 0x47

bus = smbus.SMBus(1)
bus.write_byte_data(address, power_mgmt_1, 0)

def read(address,diff):
    high = bus.read_byte_data(address, diff)
    low = bus.read_byte_data(address, diff+1)
    val = (high << 8) + low
    if val >= 0x8000:
        val = -((65535 - val) + 1)
    val /= 16384.0
    return val

def getAngle(x,s):
    return math.degree(math.atan2(x,s))

def main():
    x = read(address,Xdata)
    y = read(address,Ydata)
    z = read(address,Zdata)
    Yangle = -getAngle(x,math.sqrt(y**2+z**2))
    Xangle = getAngle(y,math.sqrt(x**2+z**2))

if __name__ == "__main__":
    main()
