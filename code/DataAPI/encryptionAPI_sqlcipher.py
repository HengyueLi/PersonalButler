


# IMPORT
import os,json
from pysqlcipher3 import dbapi2 as sqlite
# ----------------------------------


class EncryptionAPI():

    @classmethod
    def IsUserNew(cls):
        # check if data exists.  return Ture if data is empty
        return not os.path.exists( cls.getDataSource() )

    @staticmethod
    def getDataSource():
        return os.path.join(os.getcwd(), "profile.db")

    def __init__(self,Password):
        self.Password = Password
        self.dataFile = self.getDataSource()


    def ResetPassword(self,Password):
        self.Password = Password
        self.c.execute("PRAGMA rekey='{}'".format(self.Password))

    def getPassword(self) -> str:
        # return the current password
        # current password is stored somewhere in db
        #--------------  code below  ---------------
        return self.Password

    def connect(self):
        # connect to the data source
        #--------------  code below  ---------------
        self.conn = sqlite.connect(self.dataFile,check_same_thread = False)
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA key='{}'".format(self.Password))
        self.c.execute("PRAGMA cipher_compatibility = 3")

    def IsConnected(self):
        # is connected to the data source.
        # majorly used for check if password is correct
        #--------------  code below  ---------------
        try:
            self.c.execute("select * from SQLITE_master")
            return True
        except:
            return False

    def Save(self):
        # commit data into data source
        #--------------  code below  ---------------
        self.conn.commit()


    def CreateTableIfNotExist(self, tableName, isSorted=False ):
        # if isSorted, two keys named "key1" and "key2" is used to identify one item. These like (partition-key and sort-key)
        # if not, one key named "key1" is used to indentify one item, work as a primary-key
        #--------------  code below  ---------------
        if isSorted:
            cmd = "CREATE TABLE IF NOT EXISTS {} ( key1 TEXT, key2 TEXT , v TEXT )".format(tableName)
        else:
            cmd = "CREATE TABLE IF NOT EXISTS {} ( key1 TEXT , v TEXT )".format(tableName)
        self.c.execute(cmd)

    def DropTableIfExist(self,tableName):
        # delete table with all its data
        self.c.execute("drop table if exists "+tableName)

    def InsertIntoTable(self,tableName,data,key1,key2=None):
        # if key exist, update the item
        #--------------  code below  ---------------
        test = self.selectItems(tableName, key1, key2 )
        if len(test) > 0:
            self.DeleteOneItemFromTable(tableName,key1,key2)
        if key2 is None:
            self.c.execute( ''' REPLACE INTO {} (key1,v) VALUES  (?,?)'''.format(tableName), ( key1,json.dumps(data), ) )
        else:
            self.c.execute( ''' REPLACE INTO {} (key1,key2,v) VALUES  (?,?,?)'''.format(tableName), ( key1,key2,json.dumps(data), ) )

    def DeleteOneItemFromTable(self,tableName,key1,key2=None):
        if key2 is None:
            cmd = '''DELETE FROM {} WHERE key1 = '{}';'''.format(tableName,key1)
        else:
            cmd = '''DELETE FROM {} WHERE key1 = '{}' and key2 = '{}';'''.format(tableName, key1, key2)
        self.c.execute(cmd)

    def selectItems(self,tableName, key1, key2=None ) -> list:
        # if only input key1, it is the primarykey, return list should contain only 1 item
        #--------------  code below  ---------------
        if key2 is None:
            cmd = 'select * from ' + tableName + " WHERE key1 = '{}'".format(key1)
        else:
            cmd = 'select * from ' + tableName + " WHERE key1 = '{}' and key2 = '{}'".format(key1,key2)
        self.c.execute(cmd)
        rows = self.c.fetchall()
        r = []
        for pair in rows:
            r.append( json.loads(pair[-1]) )
        return r

    def SelectDistinctKey1(self,tableName) -> list:
        # use key1 (primary key) as filter
        # equally in sql: select DISTINCT key1 from tableName
        #--------------  code below  ---------------
        cmd = 'select DISTINCT key1 from ' +tableName
        self.c.execute(cmd)
        rows = self.c.fetchall()
        return [r[0] for r in rows]

    def getAllItems(self,tableName) -> list:
        # return list of data, data is dictionary
        #--------------  code below  ---------------
        cmd = 'select v from ' + tableName
        self.c.execute(cmd)
        rows = self.c.fetchall()
        return [ json.loads(r[0]) for r in rows]
