
import flask,datetime,logging



class FUM():


    @staticmethod
    def gettimeobj(sec):
        try:
            return datetime.datetime.utcfromtimestamp(sec)
        except:
            logging.error("gettimeobj@FUM@server: error with conver dt from seconds = [{}]".format(sec))


    @staticmethod
    def getDatetimeStrWithZone(dtobj):
        import time ,datetime
        dtAtCurrentZone =  dtobj - datetime.timedelta(seconds=time.timezone)
        return dtAtCurrentZone.strftime('%Y-%m-%d')

    @staticmethod
    def Password_getClassName(encObj):
        classList = encObj.getAllItems('PasswordClassNameList')
        return [ i['k'] for i in classList ]


    def Password_getAllItems(encObj,clasName) -> dict:
        #  {  itemName:value }
        items = encObj.selectItems(tableName='PasswordManager', key1=clasName)
        return {   item['itemname']:item for item in items  }
        # return encObj.getAllItemsInTable(partitionName='PasswordManager',tableName="CLASS_"+clasName)


    def ResetTable(encObj,tableName,DictList,key1,key2=None):
        encObj.DropTableIfExist(tableName)
        if key2 is not None:
            isSorted = True
        else:
            isSorted = False
        encObj.CreateTableIfNotExist( tableName, isSorted )
        if isSorted:
            for Dict in DictList:
                encObj.InsertIntoTable(tableName=tableName,data=Dict,key1=Dict[key1],key2=Dict[key2])
        else:
            for Dict in DictList:
                encObj.InsertIntoTable(tableName=tableName,data=Dict,key1=Dict[key1])
