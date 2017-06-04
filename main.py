#http://www.instructables.com/id/Raspberry-Pi-I2C-Python/
#http://www.instructables.com/id/Read-and-write-from-serial-port-with-Raspberry-Pi/
import smbus
import serial

ser = serial.Serial(port='/dev/ttyUSB0',baudrate = 9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
I2Cbus = smbus.SMBus(1)
ADaddress = 0x48

def selfCheck():
    return False

class Message:
    def __init__(self):
        self.content = {}
    def updateValue(self, term, value):
        self.content[term] = value
    def sendMessage(self):
        for key in self.content:
            print key + ': ' + str(self.content[key])
    def selfCheck(self):
        return True
    def processJY901(self,line):
        print (line[0])
        print(line[0] == 0x55)
        xAngle = -1
        yAngle = -1
        zAngle = -1
        pass
        return xAngle, yAngle, zAngle
    def processDistance(self,RAW):
        voltage = RAW*3.3/255
        distance = voltage
        return distance
    def processTem(self,RAW):
        voltage = RAW*3.3/255
        temperture = voltage
        return temperture
    def update(self):
        #serialLine = ser.readline()
        #print "ser: "
        #print(serialLine)
        #xAngle, yAngle, zAngle = self.processJY901(serialLine)
        #self.updateValue('xAngle',xAngle)
        #self.updateValue('yAngle',yAngle)
        #self.updateValue('zAngle',zAngle)
        I2Cbus.write_byte(ADaddress,0x40)
        distanceRAW = I2Cbus.read_byte(ADaddress)
        I2Cbus.write_byte(ADaddress,0x41)
        tempertureRAW = I2Cbus.read_byte(ADaddress)
        #print "i2c"
        #print distanceRAW
        #print tempertureRAW
        distance = self.processDistance(distanceRAW)
        temperture = self.processTem(tempertureRAW)
        self.updateValue('temperture', temperture)
        self.updateValue('distance', distance)

def main():
    m = Message()

    if selfCheck():
        while True:
            print "error in self check"
    else:
        while True:
            m.update()
            m.sendMessage()

if __name__ == '__main__':
    main()
