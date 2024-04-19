import random
import time
import json
import threading
from time import sleep, time
from levelDB import Database

# Tempo para invalidação de itens no cache em segundos
TInvalidacaoSeg = 60


class Cache():

    def __init__(self):
        self.cacheHashTable = dict()
        self.database = Database()

    def read(self, key):
        if key in self.cacheHashTable:
            elem = self.cacheHashTable[key]
            timestamp = int(time()) - elem['InsertionTime']

            if timestamp < TInvalidacaoSeg:
                return elem['Value']
            else:
                del self.cacheHashTable[key]

                status, response = self.database.getData(key)

                if status == 'OK':
                    self.cacheHashTable[key] = {'InsertionTime': timestamp, 'Value': response}
                    return response
                else:
                    return None
        else:
            status, response = self.database.getData(key)
            if status == 'OK':
                self.cacheHashTable[key] = {'InsertionTime': int(time.time()), 'Value': response}
                return response
                # for k,value in self.cacheHashTable.items:
                #     if k == key:
                #         if value in self.cacheHashTable:
            else:
                return None

    def insert(self, key, value):
        elem = {'InsertionTime': int(time()), 'Value': value}
        self.cacheHashTable[key] = elem
        self.database.insertData(key, value)


if __name__ == "__main__":
    cache = Cache()
    # teste
    key = '4408'
    value = 'teste'

    cache.insert(key, value)

    print(cache.read(key))

    sleep(65)

    print(cache.read(key))



