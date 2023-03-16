from sensors import Monitoring
from Database import LocalDatabase as ldb
import time

#create a local database
database = ldb()
#inicialize an instance with the sensors
Sensors = Monitoring()
Data = []
averageData = []
counter = 0
#if a database doesn't exist, it creates one
database.createDatabase()

#when called, returns an average of the values, since they are measured every 30s, but only shown once every 5 minuts
def Average(values):
    i = 0
    localAverageData = [0,0,0,0,0]
    while i < 5:
        localAverageData[i] = (values[i]+values[i+5]+values[i+10]+values[i+15]+values[i+20]+values[i+25]+values[i+30]+values[i+35]+values[i+40]+values[i+45])/10
        i += 1
    return (localAverageData)
 
#get data from the sensors
def readSensors():
    time.sleep(30)
    data = Sensors.getValues()
    for iten in data:
        Data.append(iten)
    print(Data)

#main loop
while (1):
    readSensors ()
    counter += 1
    if counter == 10:
        averageData = Average(Data)
        print(averageData)
        database.insertData(averageData)
        print("Salvou")
        counter = 0
        Data = []
        averageData = []
    
    
 
    