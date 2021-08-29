


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

    def CreatePartitionIfNotExist(self,partitionName):
        # Partition can store tables
        # A partition can be a single-database
        #--------------  code below  ---------------
        self.container.CreateTableIfNotExist(partitionName)


    def CreateTableIfNotExist(self,partitionName,tableName):
        #--------------  code below  ---------------
        partition = self.container.GetTable(partitionName)
        if tableName not in partition:
            partition[tableName] = {}

    def getAllTableNames(self,partitionName) -> list:
        # list all tables in a partition
        #--------------  code below  ---------------
        pt = self.container.GetTable(partitionName)
        return list(pt.keys())

    def getSelectByKey(self,partitionName,tableName,val,key=None): # return dict or none
        # select a item in table where get(key) =  val
        #--------------  code below  ---------------
        r = self.container.GetTable(partitionName)[tableName].get(val,None)
        # print(r,partitionName,tableName,val,9978)
        return r

    def getAllItemsInTable(self,partitionName,tableName) -> dict:
        #--------------  code below  ---------------
        r = self.container.GetTable(partitionName)[tableName]
        return r

    def setAllItemsInTable(self,partitionName,tableName,Dict):
        #--------------  code below  ---------------
        tb = self.container.GetTable(partitionName)[tableName]
        for key in Dict:
            tb[key] = Dict[key]
            



    def InsertDictIntoTable(self,partitionName,tableName,data,key):
        #--------------  code below  ---------------
        self.container.GetTable(partitionName)[tableName][key] = data

    def getDecryptedData_Dict(self) -> dict:
        # conver all data into python dict
        #--------------  code below  ---------------
        return self.container.getDecryptedData_Dict()

    def setByDecryptedData_Dict(Dict):
        # restore data from a python dict
        #--------------  code below  ---------------
        self.container.setByDecryptedData( Dict )

    #
    # def InsertDataIntoTable(self,tableName,key,pyDict):
    #     # your method to store a python-dict into table with an item key
