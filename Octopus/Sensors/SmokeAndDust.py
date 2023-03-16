#https://github.com/mauricecyril/pidustsensor/blob/master/python/pidustsensor_v3.py
from __future__ import print_function
from datetime import datetime
import math
import pigpio
import time
# also import writer for writing CSV logs
from csv import writer

class sensor:
    
    def __init__(self, pi, gpio):
       
        
        self.pi = pi
        self.gpio = gpio
        
        self._start_tick = None
        self._last_tick = None
        self._low_ticks = 0
        self._high_ticks = 0

        pi.set_mode(gpio, pigpio.INPUT)

        self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

    # Method for calculating Ratio and Concentration
    def read(self):
        
        interval = self._low_ticks + self._high_ticks

        if interval > 0:
            ratio = float(self._low_ticks)/float(interval)*100.0
            conc = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62;
        else:
            ratio = 0
            conc = 0.0

        self._start_tick = None
        self._last_tick = None
        self._low_ticks = 0
        self._high_ticks = 0

        return (self.gpio, ratio, conc)

    def _cbf(self, gpio, level, tick):

        if self._start_tick is not None:

            ticks = pigpio.tickDiff(self._last_tick, tick)

            self._last_tick = tick

            if level == 0: # Falling edge.
                self._high_ticks = self._high_ticks + ticks

            elif level == 1: # Rising edge.
                self._low_ticks = self._low_ticks + ticks

            else: # timeout level, not used
                pass

        else:
            self._start_tick = tick
            self._last_tick = tick
    """        
pi = pigpio.pi('localhost') 
teste = sensor(pi,4)
values = ()
x= 0
while(1):
    time.sleep(30)
    timestamp = datetime.now()
    values = teste.read()
    print("Concentração",x,": ", values[2], " pcs/0.01cf")
    values = ()
    x += 1"""
