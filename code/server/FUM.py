
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
