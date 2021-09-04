
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
        tbs = encObj.getAllTableNames('PasswordManager')
        pcls = [ tb.replace('CLASS_','') for tb in tbs if 'CLASS_' in tb]
        return pcls


    def Password_getAllItems(encObj,clasName) -> dict:
        tbs = encObj.getAllTableNames('PasswordManager')
        return encObj.getAllItemsInTable(partitionName='PasswordManager',tableName="CLASS_"+clasName)
