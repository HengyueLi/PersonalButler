


# IMPORT
import os
from rudeencrypt import Encryption
# ----------------------------------





class EncryptionAPI():

    @classmethod
    def IsUserNew(cls):
        # check if data exists.  return Ture if data is empty
        return not os.path.exists( cls.getDataSource() )

    @staticmethod
    def getDataSource():
        return os.path.join(os.getcwd(), "profile.dat")

    def __init__(self,Password):
        dataFile = self.getDataSource()
        self.container = Encryption(dataFile,Password)

    def ResetPassword(self,Password):
        self.container.SetPassword(Password)

    def getPassword(self) -> str:
        # return the current password
        # current password is stored somewhere in db
        #--------------  code below  ---------------
        return str(self.container._Encryption__Dict['FILE_DB_CONFIG']['password'])

    def connect(self):
        # connect to the data source
        #--------------  code below  ---------------
        self.container.connect()

    def IsConnected(self):
        # is connected to the data source.
        # majorly used for check if password is correct
        #--------------  code below  ---------------
        return self.container.IsConnected()

    def Save(self):
        # commit data into data source
        #--------------  code below  ---------------
        self.container.Save()


    def CreateTableIfNotExist(self, tableName, isSorted=False ):
        # if isSorted, two keys named "key1" and "key2" is used to identify one item. These like (partition-key and sort-key)
        # if not, one key named "key1" is used to indentify one item, work as a primary-key
        #--------------  code below  ---------------
        self.container.CreateTableIfNotExist(tableName)
        tb = self.container.GetTable(tableName)
        tb['isSorted'] = isSorted
        tb['data'] = {}

    def DropTableIfExist(self,tableName):
        # delete table with all its data
        self.container.DropTable(tableName)

    def InsertIntoTable(self,tableName,data,key1,key2=None):
        # if key exist, update the item
        #--------------  code below  ---------------
        tbDict = self.container.GetTable(tableName)
        isSorted = tbDict['isSorted']
        db = tbDict['data']
        if key2 is None:
            db[key1] = data
        else:
            if key1 not in db:
                db[key1] = {}
            db[key1][key2] = data

    def DeleteOneItemFromTable(self,tableName,key1,key2=None):
        tbDict = self.container.GetTable(tableName)
        isSorted = tbDict['isSorted']
        db = tbDict['data']
        if isSorted:
            del db[key1][key2]
        else:
            del db[key1]



    def selectItems(self,tableName, key1, key2=None ) -> list:
        # if only input key1, it is the primarykey, return list should contain only 1 item
        #--------------  code below  ---------------
        tbDict = self.container.GetTable(tableName)
        isSorted = tbDict['isSorted']
        db = tbDict['data']
        if isSorted:
            if key2 is None:
                partition = db.get(key1,{})
                return [ partition[key2] for key2 in partition ]
            else:
                g = db.get(key1,{}).get(key2,None)
                return [g] if g is not None else []
        else:
            return  [ db[key1] ]

    def getAllItems(self,tableName) -> list:
        # return list of data, data is dictionary
        #--------------  code below  ---------------
        tbDict = self.container.GetTable(tableName)
        isSorted = tbDict['isSorted']
        db = tbDict['data']
        if isSorted:
            r = []
            for key1 in db:
                r += [ db[key1][key2] for key2 in db[key1] ]
            return r
        else:
            return [ db[k] for k in db ]












#----------------------------------------------------------------
# # 因为butler中的存储结构变化了，以下脚本可以将旧版本dat转换成新版本
# import json
# from rudeencrypt import Encryption
# import getpass
#
#
# dataFilePath = 'profile.dat'
#
# password = getpass. getpass()
# enDB = Encryption(dataFilePath,password)
# enDB.connect()
# r = enDB.getDecryptedData_Dict()
# d = r['FILE_DB_TABLE']['PasswordManager']['class']
# newPass = {}
# for key in d:
#     tn = "CLASS_" + key
#     newPass[tn] = dict(  d[key]   )
# newPass['keywords'] = dict(r['FILE_DB_TABLE']['PasswordManager']['keywords'])
# r['FILE_DB_TABLE']['PasswordManager'] = newPass
# newDiary = {}
# def f(item):
#     item['id'] = str(item['id'])
#     return item
# newDiraryList = {str(item['id']):f(item) for item in r['FILE_DB_TABLE']['Diary']['list']}
# r['FILE_DB_TABLE']['Diary']['list'] = newDiraryList
# enDB.path = dataFilePath + ".newVersion"
# enDB.setByDecryptedData(r)
# enDB.Save()
# print('finished')
