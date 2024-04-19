import random
import time
import json
import threading
from time import sleep, time
from levelDB import Database

# Tempo para invalidação de itens no cache em segundos
TInvalidacaoSeg = 60


class Cache:

    def __init__(self):
        self.cacheHashTable = dict()
        self.database = Database(port=40000, part=1, primary=f'localhost:5000', secundary=[])

    def read(self, key, types):
        if key in self.cacheHashTable:
            elem = self.cacheHashTable[key]
            timestamp = int(time()) - elem['InsertionTime']

            if timestamp < TInvalidacaoSeg:
                return elem['Value']
            else:
                del self.cacheHashTable[key]

                status, response = self.database.getData(key, types)

                if status == 'OK':
                    self.cacheHashTable[key] = {'InsertionTime': timestamp, 'Value': response}
                    return response
                else:
                    return None
        else:
            status, response = self.database.getData(key, types)
            if status == 'OK':
                self.cacheHashTable[key] = {'InsertionTime': int(time.time()), 'Value': response}
                return response
                # for k,value in self.cacheHashTable.items:
                #     if k == key:
                #         if value in self.cacheHashTable:
            else:
                return None

    def insert(self, key, value, types):
        elem = {'InsertionTime': int(time()), 'Value': value}
        self.cacheHashTable[key] = elem
        self.database.insertData(key, value, types)


if __name__ == "__main__":
    cache = Cache()

    # Teste
    key = '4408'
    value = 'teste'

    # Defina o tipo de dado ('aluno', 'professor', 'disciplina', 'turma')
    types = 'aluno'

    # Insere no cache
    cache.insert(key, value, types)

    # Lê do cache
    result = cache.read(key, types)
    print(result)



