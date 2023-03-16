import mysql.connector
import sqlite3
from datetime import datetime

class LocalDatabase:
    
    def __init__(self):
        self._cursor = None
        self._conn = None
    
    def connectDb(self):
        "Connect to db"
        self._conn = sqlite3.connect('/home/pi/Octopus/Rasp-Module/Config/CentralModule/Database.db')
        self._cursor = self._conn.cursor()
        
        return self._cursor
    
    def closeDatabase(self):
        
        if self._conn == None:
            return
        
        self._conn.commit()
        self._conn.close()
        self._conn = None
        self._cursor = None
    
    def createDatabase(self):
        if (self._conn == None):
            self.connectDb()
        
        self._cursor.execute('CREATE TABLE octopus(date DATETIME,lux INTERGER, temperature INTERGER, humidity INTERGER, smoke INTERGER, co2 INTERGER)')
        
        self.closeDatabase()
        
    def insertData(self, valores:list):
        if self._conn == None:
            self.connectDb()
        uploadTime = datetime.now()
        uploadTime = uploadTime.strftime("%d/%m/%Y %H:%M")
        self._cursor.execute("INSERT INTO octopus VALUES (datetime('now','localtime'),?, ?, ?, ?, ?)", valores)

        self.closeDatabase()
    
    
            
                
        
        
            