import serial
import time

class MHZ14A():
    PACKET = [0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]
    RANGE1 = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x07, 0xd0, 0x8F]
    RANGE2 = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x13, 0x88, 0xCB]
    RANGE3 = [0xFF, 0x01, 0x99, 0x00, 0x00, 0x00, 0x27, 0x10, 0x2F]
    AUTOCALON = [0xFF, 0x01, 0x79, 0xA0, 0x00, 0x00, 0x00, 0x00, 0xE6]
    AUTOCALOFF = [0xFF, 0x01, 0x79, 0x00, 0x00, 0x00, 0x00, 0x00, 0x86]

    def __init__(self, ser):
        self.serial = serial.Serial(ser, 9600, timeout=2)
        time.sleep(2)

    def get(self):
        self.serial.write(bytearray(MHZ14A.PACKET))
        res = self.serial.read(size=9)
        res = bytearray(res)
        checksum = 0xff & (~(res[1] + res[2] + res[3] + res[4] + res[5] + res[6] + res[7]) + 1)
        if res[8] == checksum:
            ppm = (res[2]*256)+res[3]
            #return (res[2] << 8|res[3])
            return(ppm)
        else:
            raise Exception("checksum: " + hex(checksum))

    def close(self):
        self.serial.close()
"""
#Acquires and returns the CO2 concentration from the sensor
def main():
    sensor = MHZ14A("/dev/serial0")
    #autocal(1)
    #autocal(0)
    while 1:
        try:
            print (int(sensor.get()))
            time.sleep(2)
            #return (int(sensor.get()))
        except:
            print("???")
            pass
        #sensor.close()

#Self-On / off of calibration function(No return value)
def autocal(x):
    sensor = MHZ14A("/dev/serial0")
    if x == 0:
        sensor.serial.write(bytearray(MHZ14A.AUTOCALOFF))
    elif x == 1:
        sensor.serial.write(bytearray(MHZ14A.AUTOCALON))
    sensor.close()

#Send a command to change the measurement range(No return value)
def range(y):
    sensor = MHZ14A("/dev/serial0")
    if y == 1:
        sensor.serial.write(bytearray(MHZ14A.RANGE1))
    elif y == 2:
        sensor.serial.write(bytearray(MHZ14A.RANGE2))
    elif y == 3:
        sensor.serial.write(bytearray(MHZ14A.RANGE3))
    sensor.close

if __name__ == '__main__':
    main()"""