
import flask,datetime



class FUM():


    @staticmethod
    def gettimeobj(sec):
        return datetime.datetime.utcfromtimestamp(sec)

    @staticmethod
    def getDatetimeStrWithZone(dtobj):
        import time ,datetime
        dtAtCurrentZone =  dtobj - datetime.timedelta(seconds=time.timezone)
        return dtAtCurrentZone.strftime('%Y-%m-%d')
