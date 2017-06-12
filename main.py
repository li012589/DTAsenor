import smbus
import time
import math
import serial

I2Cbus = smbus.SMBus(1)
ADaddress = 0x48
jy_sensor = serial.Serial(port="/dev/ttyUSB0", baudrate="9600", timeout=1)

def selfCheck():
    return False

class Message:
    def __init__(self):
        #I2Cbus.write_byte_data(MPUaddress, power_mgmt_1, 0)
        #print(I2Cbus.read_byte_data(MPUaddress,power_mgmt_1))
        self.content = {}
    def updateValue(self, term, value):
        self.content[term] = value
    def sendMessage(self):
        for key in self.content:
            print(key + ': ' + str(self.content[key]))
    def selfCheck(self):
        return True
    def processDistance(self,RAW):
        voltage = RAW*5.0/255
        if voltage>=1.05 and voltage <=1.25:
            distance = -50*voltage+112.5
        elif voltage>1.25 and voltage <=1.5:
            distance = -40*voltage+100
        elif voltage >1.5 and voltage<=2.5:
            distance = -20*voltage+70
        else:
            distance = -1
        return distance
    def processTem(self,RAW):
        voltage = RAW*5.0/255
        temperture = 50*voltage-53
        return temperture
    def readMPU(self):
        while True:
            data = jy_sensor.read(size=1)
            if data == b'\x55':
                #print("success!")
                jy_sensor.read(size=10)
                break;
            #print("trying", data)

        try:
            while True:
                data = jy_sensor.read(size=11)
                if not len(data) == 11:
                    print('byte error:', len(data))
                    continue
                if data[1] == 83:
                    x = int.from_bytes(data[2:4], byteorder='little')/32768*16
                    y = int.from_bytes(data[4:6], byteorder='little')/32768*16
                    z = int.from_bytes(data[6:8], byteorder='little')/32768*16
                    t = int.from_bytes(data[8:10],byteorder='little')/100
                    break
                #print("----",data[0], data[1])
            #print("Angle output:{}, {}, {}".format(x, y, z))
            return x,y,z,t
        except:
            jy_sensor.close()
            print("close port")
    def getAngle(self,x,s):
        return math.degrees(math.atan2(x,s))
    def update(self):
        I2Cbus.write_byte(ADaddress,0x41)
        time.sleep(0.2)
        a1 = []
        for i in range(1,10):
            a1.append(I2Cbus.read_byte(ADaddress))
        a1.remove(max(a1))
        a1.remove(min(a1))
        a1 = sum(a1)/len(a1)
        I2Cbus.write_byte(ADaddress,0x40)
        time.sleep(0.2)
        a0 = []
        for i in range(1,10):
            a0.append(I2Cbus.read_byte(ADaddress))
        a0.remove(max(a0))
        a0.remove(min(a0))
        a0 = sum(a0)/len(a0)
        x,y,z,t = self.readMPU()
        distance = self.processDistance(a0)
        temperture = self.processTem(a1)
        self.updateValue("Angle output(x,y,z)",[x,y,z])
        self.updateValue('temperture', temperture)
        #self.updateValue('Traw',a1/float(255)*5)
        #self.updateValue('Draw',a0/float(255)*5)
        self.updateValue('distance', distance)

def main():
    m = Message()

    if selfCheck():
        while True:
            print("error in self check")
    else:
        while True:
            time.sleep(0.5)
            m.update()
            m.sendMessage()

if __name__ == '__main__':
    main()
