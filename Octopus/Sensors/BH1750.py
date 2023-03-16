import board
import time
import adafruit_bh1750

i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)

while 1:
    print("A quantidade de luz é: ", sensor.lux)
    time.sleep(0.5)
