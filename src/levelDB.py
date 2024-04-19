import plyvel
from pysync import SyncObj, replicated
from lvldb import Database

import sys
import socket
import threading
import json


class ReplicaControl():

    def __init__(self,replicaNum):

        if replicaNum == 0:
            self.portaSocket = 55021
            self.replica = Database(self.socketPort,'pair','localhost: 51000',['localhost: 51001','localhost: 51002'])
        if replicaNum == 1:
            self.portaSocket = 55022
            self.replica = Database(self.socketPort,'pair','localhost: 51001',['localhost: 51000','localhost: 51002'])
        if replicaNum == 2:
            self.portaSocket = 55023
            self.replica = Database(self.socketPort,'pair','localhost: 51002',['localhost: 51000','localhost: 51001'])
        
        if replicaNum == 3:
            self.portaSocket = 55024
            self.replica = Database(self.socketPort,'odd','localhost: 51003',['localhost: 51004','localhost: 51005'])
        if replicaNum == 4:
            self.portaSocket = 55025
            self.replica = Database(self.socketPort,'odd','localhost: 51004',['localhost: 51003','localhost: 51005'])
        if replicaNum == 5:
            self.portaSocket = 55026
            self.replica = Database(self.socketPort,'odd','localhost: 51005',['localhost: 51003','localhost: 51004'])


    def startSocket(self):

        s = socket.socket()
        host = socket.gethostnome()
        s.bind((host,self.portaSocket))
        backlog = 50
        s.listen(backlog)

        while True:
            con,end = s.accept()
            print('Connection with' +str(end) +'successfully established')
            threading.Thread(target = self.ReplicaControl, args =(con,end)).start()


    def ReplicaControl(self,con,end):

        msg = None

        while True:
            data = con.recv(4096)
            msg - data.decode()


            if msg:
                jsonResp = json.load(msg)
                functionName = jsonResp['function']
                key = jsonResp['key']
                value = jsonResp['value']

            if functionName == 'read':
                response = self.replica.getData(key)
                
                if response:
                    response = str(response).replace('\'','"')
                    response = json.loads(response)
                resp = json.dumps({'data': response})


            if functionName == 'insert'
                self.replica.insertData(key,value)
                resp = json.dumps({'status': 'OK', 'resposta': 'Inserido' })

            if functionName == 'update':
                self.replica.updateData(key,value)
                resp = json.dumps({'status': 'OK', 'resposta': 'Atualizado' })

            if functionName == 'delete':
                self.replica.deleteData(key)
                resp = json.dumps({'status': 'OK', 'resposta': 'Apagado' })

            con.send(resp.encode())




class Database(SyncObj):

    def __init__(self,port,part,primary,secundary):
        super(Database,self).__init__(primary,secundary)
        self.database = f'./files/{part}/{port}/' 


    @replicated
    def insertData(self,key,value):

        try:

            db = plyvel.DB(self.database,create_if_missing = True)

            bytesKey = bytes(key,'utf-8')
            bytesValue = bytes(value,'utf-8')
            db.put(bytesKey,bytesValue)
            db.close()
            print('create',self.db,key,value,json.dumps({'status':'OK','resposta': 'Inserido'}))
        except BaseException as e:
            print('ERROR','create',self.db,key,value,json.dumps({'status':'ERROR','resposta': str(e)}))

    @replicated
    def deleteData(self,key):

        try:

            db = plyvel.DB(self.database,create_if_missing = True)

            bytesKey = bytes(key, 'utf-8')
            db.delete(bytesKey)
            db.close
            print('delete',self.db,key,json.dumps({'status':'OK','resposta': 'Apagado'}))
        except BaseException as e:
            print('ERROR','delete',self.db,key,json.dumps({'status':'ERROR','resposta': str(e)}))


    def updateData(self,key,value):

        try:

            self.deleteData(key)
            self.insertData(key,value)
            print('update',self.db,key,value,json.dumps({'status':'OK','resposta': 'Atualizado'}))
        except BaseException as e:
            print('ERROR','update',self.db,key,value,json.dumps({'status':'ERROR','resposta': str(e)}))


    def getData(self,key)

        try:
            db = plyvel.DB(self.database,create_if_missing = True)
            bytesKey = bytes(key,'utf-8')

            respBytes = db.get(bytesKey)
            resp = None if not respBytes else respBytes.decode()
            print('get', self.db, key, json.dumps({'status': 'OK', 'resposta': resp }))
            db.close()
            return 'OK',resp

        except BaseException as e:
            return 'ERROR',str(e)


    if __name__ == "__main__":

        if sys.argv and sys.argv[1] and sys.argv[1].isnumeric():
            replicaNum = int(sys.argv[1])

            if replicaNum not in [0,1,2,3,4,5]:
                print("Choose one between 0 and 5")
                sys.exit(-1)
            else :
                print('Initializing replica' + str(replicaNum))
                replica = Database(replicaNum) 
                print('Connecting socket and portal')
                replica.startSocket()

        
