import board
import time
import adafruit_bh1750
import Adafruit_BMP.BMP085 as BMP085
from SmokeAndDust import sensor
import SDL_Pi_HDC1000
from MHZ14A_1 import MHZ14A
import pigpio

class Monitoring:
    
    def HDC1000Calibration(self):
        self.hdc1000.turnHeaterOn() 
        self.hdc1000.turnHeaterOff() 
        self.hdc1000.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
        self.hdc1000.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)
    
    def __init__(self):
        self.i2c = board.I2C()
        self.lux_sensor = adafruit_bh1750.BH1750(self.i2c)
        self.tempPress = BMP085.BMP085()
        self.CO2 = MHZ14A("/dev/serial0")
        self.hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()
        self.HDC1000Calibration()
        self.values = []
        pi = pigpio.pi('localhost') 
        self.SmokeandDust = sensor(pi,4)
        self.BMP = BMP085.BMP085()
        
    
    def getValues(self):
        self.values = []
#values = [LUX, TEMPERATURE, HUMIDITY, SMOKE AND DUST, CO2]
        #LUX Sensor BH1750
        self.values.append(self.lux_sensor.lux)
        #HUMIDITY AND TEMPERATURE SENSOR HDC1000
        self.values.append(self.BMP.read_temperature())
        self.values.append(self.hdc1000.readHumidity())
        #SMOKE AND DUST SENSOR
        
        DustValues = self.SmokeandDust.read()
        self.values.append(DustValues[2])
        #CO2
        self.values.append(int(self.CO2.get()))
        for i in range(4):
            self.values[i] = round(self.values[i],2)
        return(self.values)
    
    def printValues(self, valores: list):
       print("-------------------")
       print(f'LUX: {valores[0]:,.2f}\n')
       print(f'TEMPERATURE: {valores[1]:,.2f}°C \n')
       print(f'HUMIDITY: {valores[2]:,.2f} %% \n')
       print(f'SMOKE AND DUST: {valores[3]:,.2f} pcs/0.01cf \n')
       print(f'CO2: {valores[4]:,.2f} ppm')
       print("-------------------")
"""       
t = Monitoring()
while(1):
    lista = t.getValues()
    t.printValues(lista)"""
    
        