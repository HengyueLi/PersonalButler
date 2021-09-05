
from main import app,permission
import flask,datetime,time

from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,IntegerField,TextField,validators,SelectField
from wtforms.widgets import TextArea



def GetSecId():
    return int(datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"))




class SeperatePage():

    def __init__(self,List,N_per_page):
        self.List = List
        self.M    = N_per_page

    def MathStartAndEndIndexOfPage(self,pageindex):
        start = ( pageindex - 1 ) * self.M + 1
        end   = ( start + self.M - 1)
        return  start,end

    def IsPageIndexValid(self,pageindex):
        s = ( pageindex - 1 ) * self.M + 1
        return s >=1 and s <= len(self.List)



    def GetStartEnd(self,index):
        ms,me = self.MathStartAndEndIndexOfPage(pageindex=index)
        start =  max( 1 , ms )
        end   =  min( len(self.List) ,  me )
        return start , end

    def GetListSegmentByIndex(self,index):
        start,end =  self.GetStartEnd(index)
        return list(self.List[start-1:end])

    def IsLeftHave(self,index): # iterm index , not page index
        if index>1:
            return True
        else:
            return False

    def IsRightHave(self,index):# iterm index , not page index
        if index * self.M < len(self.List):
            return True
        else:
            return False

    def GetIndexRangeList(self,index):
        start,end =  self.GetStartEnd(index)
        return [jc for jc in range(start,end+1)]

    # return a list [ index , [  "<" , ">" , integer ] ]
    # here index is the page index
    def GetMutipleIndexList(self,index,Range):
        r2 = []
        if ( self.IsPageIndexValid( index - Range - 1 ) ): r2.append('<')
        for testi in range( index - Range , index + Range + 1 ):
            if self.IsPageIndexValid(testi):
                r2.append(testi)
        if ( self.IsPageIndexValid( index + Range + 1 ) ): r2.append('>')
        return [ index , r2 ]




















class DiaryForm(FlaskForm):
    id     = IntegerField()
    time   = FloatField()
    title  = StringField()
    record = StringField('description', widget=TextArea())




class DiaryObj():


    @staticmethod
    def SaveToDB():
        container = app.config['DATA_CONTAINER']
        container.Save()
        # self.encObj.Save()


    def SetEditeFormToContainer(form):
        Dict = {}
        for field in form:
            if field.id == 'csrf_token': continue
            Dict[field.id] = field.data
        encObj = app.config['DATA_CONTAINER']
        encObj.InsertDictIntoTable(partitionName='Diary',tableName='list',data=Dict,key=Dict['id'])
        encObj.Save()
        # container = app.config['DATA_CONTAINER']
        # diarylist = container.GetTable('Diary')['list']
        # for jc in range(len(diarylist)):
        #     if diarylist[jc]['id'] == Dict['id']:
        #         diarylist[jc] = Dict
        #         return
        # print('ERROR: @SetEditeFormToContainer, id={} is not fond in diarylist'.format(['id']))

    @classmethod
    def RerangeListbyTime(cls):
        encObj = app.config['DATA_CONTAINER']
        diarylist = cls.getDiaryDict()
        td = {}
        for item in diarylist:
            td[item['time']] = item
        times = list(td.keys())
        times.sort(reverse=True,key=float)
        diarylist = { td[time]['id']:td[time] for time in times }
        encObj.setAllItemsInTable(partitionName='Diary',tableName='list',Dict=diarylist)

    # @staticmethod
    # def RerangeListbyTime():
    #     container = app.config['DATA_CONTAINER']
    #     Diary     = container.GetTable('Diary')
    #     diarylist = Diary['list']
    #     td = {}
    #     for item in diarylist:
    #         td[item['time']] = item
    #     times = list(td.keys())
    #     times.sort(reverse=True,key=float)
    #     Diary['list'] = [ td[time] for time in times ]






    @staticmethod
    def getDiaryDict():
        encObj = app.config['DATA_CONTAINER']
        diaryDict = encObj.getAllItemsInTable(partitionName='Diary',tableName='list')
        diarylist = [diaryDict[k] for k in diaryDict]
        return diarylist



    @classmethod
    def GetDiaryObjList( cls ):
        diarylist = cls.getDiaryDict()
        return [ cls(Dict=d) for d in diarylist ]


    @classmethod
    def GetNew(cls):
        Dict = {
                'id':GetSecId() ,
                'time':datetime.datetime.now().timestamp(), # can not use utcnow! Timezone lost ! why? I do not know!
                'title':'',
                'record':'',}
        encObj = app.config['DATA_CONTAINER']
        encObj.InsertDictIntoTable(partitionName='Diary',tableName='list',data=Dict,key=Dict['id'])
        encObj.Save()
        return cls(Dict=Dict)

    @classmethod
    def SearchId(cls,id):
        encObj = app.config['DATA_CONTAINER']
        r = encObj.getSelectByKey(partitionName='Diary',tableName='list',val = id)
        if r is None:
            print('ERROR: id = {} is not found in diarylist @SearchId'.format(id))
        else:
            return cls(Dict = r)

        # container = app.config['DATA_CONTAINER']
        # diarylist = container.GetTable('Diary')['list']
        # for jc in range(len(diarylist)):
        #     if diarylist[jc]['id'] == id:
        #         return cls(Dict = diarylist[jc])
        # print('ERROR: id = {} is not found in diarylist @SearchId'.format(id))





    # def setInfo_formToDict(self,iform):
    #     if self.Initiate:
    #         for field in iform:
    #             if field.id == 'csrf_token': continue
    #             self.Dict[field.id] = field.data
    #         self.SaveToDB()


    # Dict is the item saved in DB directly
    def __init__(self,Dict = None):
        if Dict is not None:
            self.encObj = app.config['DATA_CONTAINER']
            self.Dict = Dict
            self.form = DiaryForm()
            self.initiated = True
            return
        else:
            print('ERROR: no valid input in ini@DiaryObj')


    def SetFormbyDict(self):
        if self.initiated:
            for field in self.form:
                if field.id == 'csrf_token': continue
                val = self.Dict.get(field.id,None)
                if val is not None:
                    field.default = val
            self.form.process()



















@app.route('/Diary/<int:pageindex>',methods=['get'])
@permission.ValidForLogged
def Diary(pageindex):

    N_per_page = 30
    indexrange = 4


    sp = SeperatePage(List = DiaryObj.GetDiaryObjList(),N_per_page = N_per_page)
    DiaryObjList = sp.GetListSegmentByIndex(pageindex)
    pagelist = sp.GetMutipleIndexList(index=pageindex,Range=indexrange)
    # return a list [ index , [  "<" , ">" , integer ] ]

    return flask.render_template('Diary.html/Diary.html.j2',
    app = app,
    DiaryObjList=DiaryObjList,
    pagelist=pagelist)



@app.route('/Diary_createNew',methods=['get'])
@permission.ValidForLogged
def Diary_createNew():
    Diary = DiaryObj.GetNew()
    Diary.SetFormbyDict()
    return flask.render_template('Diary.html/Diary_Edite.html.j2',app = app,Diary=Diary)



@app.route('/Diary_EditeDiary/<int:id>',methods=['get'])
@permission.ValidForLogged
def Diary_EditeDiary(id):
    Diary = DiaryObj.SearchId(id)
    Diary.SetFormbyDict()
    return flask.render_template('Diary.html/Diary_Edite.html.j2',app = app,Diary=Diary)





@app.route('/Diary_submit',methods=['POST'])
@permission.ValidForLogged
def Diary_submit():
    form = DiaryForm()
    if form.validate_on_submit():
        DiaryObj.SetEditeFormToContainer(form)
        DiaryObj.RerangeListbyTime()
        DiaryObj.SaveToDB()
        return 'sucess'
    else:
        return 'error'
