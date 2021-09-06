


# IMPORT
import os,sqlite3,json
# ----------------------------------





class EncryptionAPI():

    @classmethod
    def IsUserNew(cls):
        # check if data exists.  return Ture if data is empty
        return not os.path.exists( cls.getDataSource() )

    @staticmethod
    def getDataSource():
        return os.path.join(os.getcwd(), "profile_dir")

    def __init__(self,Password):
        Dir = self.getDataSource()
        if not os.path.exists(Dir):os.mkdir(Dir)

    def ResetPassword(self,Password):
        pass
        # self.container.SetPassword(Password)

    def getPassword(self) -> str:
        # return the current password
        # current password is stored somewhere in db
        #--------------  code below  ---------------
        pass

    def connect(self):
        # connect to the data source
        #--------------  code below  ---------------
        pass

    def IsConnected(self):
        # is connected to the data source.
        # majorly used for check if password is correct
        #--------------  code below  ---------------
        return True

    def Save(self):
        # commit data into data source
        #--------------  code below  ---------------
        pass

    def CreatePartitionIfNotExist(self,partitionName):
        # Partition can store tables
        # A partition can be a single-database
        #--------------  code below  ---------------
        dbPath = os.path.join(self.getDataSource(),partitionName)
        conn = sqlite3.connect(dbPath)
        conn.close()


    def CreateTableIfNotExist(self,partitionName,tableName):
        #--------------  code below  ---------------
        dbPath = os.path.join(self.getDataSource(),partitionName)
        conn = sqlite3.connect(dbPath)
        c    = conn.cursor()
        cmd = "CREATE TABLE IF NOT EXISTS {} ( k TEXT, v TEXT  )".format(tableName)
        c.execute(cmd)
        conn.commit()
        conn.close()


    def getAllTableNames(self,partitionName) -> list:
        # list all tables in a partition
        #--------------  code below  ---------------
        dbPath = os.path.join(self.getDataSource(),partitionName)
        conn = sqlite3.connect(dbPath)
        c    = conn.cursor()
        cmd = "select name from sqlite_master where type='table' order by name"
        c.execute(cmd)
        rows = c.fetchall()
        conn.close()
        return [i[0] for i in rows]


    def getSelectByKey(self,partitionName,tableName,val,key=None): # return dict or none
        # select a item in table where get(key) =  val
        #--------------  code below  ---------------
        dbPath = os.path.join(self.getDataSource(),partitionName)
        conn = sqlite3.connect(dbPath)
        c    = conn.cursor()
        c.execute('select v from {} where k=?;'.format(tableName),(val,))
        rows = c.fetchall()
        conn.close()
        if len(rows) == 0:
            return None
        else:
            return json.loads(rows[0][0])

    def getAllItemsInTable(self,partitionName,tableName) -> dict:
        #--------------  code below  ---------------
        dbPath = os.path.join(self.getDataSource(),partitionName)
        conn = sqlite3.connect(dbPath)
        c    = conn.cursor()
        c.execute('select * from {};'.format(tableName))
        rows = c.fetchall()
        conn.close()
        r = {}
        for pair in rows:
            r[pair[0]]=json.loads(pair[1])
        return r

    def setAllItemsInTable(self,partitionName,tableName,Dict):
        #--------------  code below  ---------------
        for k in Dict:
            self.InsertDictIntoTable(partitionName,tableName,Dict[k],k)

    def InsertDictIntoTable(self,partitionName,tableName,data,key):
        # if key exist, update the item
        #--------------  code below  ---------------
        tmp = self.getSelectByKey(partitionName,tableName,key)
        dbPath = os.path.join(self.getDataSource(),partitionName)
        conn = sqlite3.connect(dbPath)
        c    = conn.cursor()
        if tmp is None:
            c.execute(''' INSERT INTO {} (k,v) VALUES  (?,?)'''.format(tableName), ( key,json.dumps(data) ))
        else:
            c.execute(''' UPDATE {} SET v = ? WHERE k = ?'''.format(tableName), (json.dumps(data), key ))
        conn.commit()
        conn.close()



    def DeleteItemFromTable(self,partitionName,tableName,key):
        #--------------  code below  ---------------
        tmp = self.getSelectByKey(partitionName,tableName,key)
        dbPath = os.path.join(self.getDataSource(),partitionName)
        conn = sqlite3.connect(dbPath)
        c    = conn.cursor()
        c.execute('''DELETE FROM {} WHERE k = ?;'''.format(tableName), ( key, ))
        conn.commit()
        conn.close()
