
import flask,datetime



class FUM():


    @staticmethod
    def gettimeobj(sec):
        return datetime.datetime.utcfromtimestamp(sec)
