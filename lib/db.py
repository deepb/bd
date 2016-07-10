#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
file: db.py $Id$
date: $Date$
"""

# Importar print como funcion
from __future__ import print_function

import MySQLdb as db

from locals import *

class miDB():

    def __init__(self, *args):
        self.initDB(*args)
    
    def setDB(self, db, *args):
        self._db = db
    
    def getDB(self, *args):
        return self._db

    def commitDB(self, *args):
        return self._db.commit()
    
    def cursorDB(self, *args):
        return self._db.cursor()
    
    def initDB(self, *args):
        try:
            self.setDB(db.connect(db_host, db_user, db_pass, db_data))
        except:
            self.setDB(None)
            print("No hay conexion con la base de datos")
    
    def talkDB(self, query, many=False):
        cursor = self.cursorDB()
        try:
            cursor.execute(query)
            if many:
                data = cursor.fetchall()
            else:
                data = cursor.fetchone()
            cursor.close()
            self.commitDB()
            return data
        except:
            print("Error: %s" % query)
    
    def populateDB(self, *args):
        if self.getDB() is not None:
            for a in range(5):
                self.talkDB("INSERT INTO Top (Nombre, Puntos) \
                    VALUES ('Play%s', %d);" % 
                    (str(a), int(a)))
        else:
            print("Error: BBDD no populada")
            
    def createDB(self, *args):
        query = "CREATE TABLE Top ( \
                    id INT NOT NULL AUTO_INCREMENT, \
                    Nombre VARCHAR(5) NOT NULL, \
                    Puntos INT NOT NULL, \
                    TimeStamp DATETIME NOT NULL DEFAULT NOW(), \
                    PRIMARY KEY (id) \
                );"
        try:
            self.talkDB(query)
        except:
            print("Error: BBDD no creada")

    def removeDB(self, *args):
        if self.getDB() is not None:
            query = "DROP TABLE Top"
            self.talkDB(query)
        else:
            print("Error: BBDD no eliminada")
    
    def truncateDB(self, *args):
        if self.getDB() is not None:
            query = "TRUNCATE TABLE Top"
            self.talkDB(query)
        else:
            print("Error: BBDD no truncada")
    
    def getTop(self, limit=5, *args):
        if self.getDB() is not None:
            query = "SELECT Nombre, Puntos FROM Top \
                    ORDER BY Puntos DESC LIMIT %d;" % limit
            data = self.talkDB(query, True)
            return data
        else:
            print("No hay base de datos. Comprueba la conexion.")
    
    def addTop(self, player, points, *args):
        if self.getDB() is not None:
            self.talkDB("INSERT INTO Top (Nombre, Puntos) VALUES ('%s', %d);" %\
                    (str(player), int(points)))

