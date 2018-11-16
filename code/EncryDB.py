#!/usr/bin/env python3

#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# Class:   EncryDB
#──────────────────────────
# Author:  Hengyue Li
#──────────────────────────
# Version: 2018/10/19
#──────────────────────────
# discription:
#         The Dict MUST contains a element of FILE_DB_CONFIG (dict)
#         FILE_DB_CONFIG:{password: }
#         FILE_DB_TABLE:{ }
#
#──────────────────────────
# Used :
import json,hashlib,base64,os,inspect
from Crypto import Random
from Crypto.Cipher import AES
#──────────────────────────
# Interface:
#
#        [ini] file,key
#
#        [sub] CreateTableIfNotExist(TableName)
#              if it is already existed, do nonthing
#
#        [cls,sub] InitiateFile(filepath,key):
#                  initiate a data file
#
#        [cls,fun] LoadFileToDict(filepath,key = '')
#                  read a file to dict
#
#        [cls,sub] SaveDictToFile(filepath,Dict)
#                  save a dict to file.
#
#        [cls,fun] GetFolderPath()
#
#        [cls,fun] GetFilePath()
#
#
#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════



class EncryDB():


    class AESCipher(object):
    #-------------------------------------
    #https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
        def __init__(self, key):
            self.bs = 32
            self.key = hashlib.sha256(key.encode()).digest()

        def encrypt(self, raw):
            raw = self._pad(raw)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw))

        def decrypt(self, enc):
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

        def _pad(self, s):
            return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

        @staticmethod
        def _unpad(s):
            return s[:-ord(s[len(s)-1:])]

    @staticmethod
    def GetFilePath():
        return os.path.realpath(__file__)

    @classmethod
    def GetFolderPath(cls):
        f = cls.GetFilePath()
        return os.path.dirname(f)


    def __init__(self,path,key=''):
        self.path = path
        self.key  = key
        if os.path.isfile(self.path):
            self.Dict = self.LoadFileToDict(self.path,key)
            if self.Dict is None:
                # raise Exception('Invalid DB file or key error!')
                self.isconnected = False
            else:
                self.isconnected = True
        else:
            self.isconnected = False
            self.InitiateFile(self.path,key)


    def CreateTableIfNotExist(self,TableName):
        if TableName not in self.Dict['FILE_DB_TABLE']:
            self.Dict['FILE_DB_TABLE'][TableName] = {}

    def SaveToDB(self):
        self.SaveDictToFile(self.path,self.Dict)



    def NotConnectedError(self):
        if not self.isconnected:
            print("DB is not connected, function '{}' is not callable".format(inspect.stack()[1][3]))

    def Save(self):
        self.NotConnectedError()
        self.SaveDictToFile( self.path , self.Dict )



    def CreateTable(self,TableName):
        self.NotConnectedError()
        if TableName in self.Dict:
            print('{} is existed in DB'.format(TableName))
            exit()
        else:
            self.Dict[TableName] = {}



    @classmethod
    def LoadFileToDict(cls,filepath,key = ''):
        reader = cls.AESCipher(key)
        f = open(filepath,'rb')
        Estr = f.read()
        f.close()
        getString = reader.decrypt(Estr)
        try:
            d = json.loads(getString)
            if d['FILE_DB_CONFIG']['password'] == key:
                return d
        except:
            return None
        return None


    @classmethod
    def SaveDictToFile(cls,filepath,Dict):
        jStr   = json.dumps(Dict)
        key    = Dict['FILE_DB_CONFIG']['password']
        reader = cls.AESCipher(key)
        Estr   = reader.encrypt(jStr)
        tpfile =  filepath+'.temp'
        f = open(tpfile,'wb')
        f.write(Estr)
        f.close()
        os.rename(tpfile,filepath)



    @classmethod
    def InitiateFile(cls,filepath,key=''):
        d = {  'FILE_DB_CONFIG':{ 'password':key    }  , 'FILE_DB_TABLE':{}   }
        cls.SaveDictToFile(filepath,d)



#
# f= EncryDB('test.dat','65')
# print(f.GetFolderPath())
#
#
#
# print(f.Dict)
#

# f.CreateTableIfNotExist('MyPasswordManeger')
#
# f.SaveToDB()
