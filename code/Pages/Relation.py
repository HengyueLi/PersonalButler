
from main import app,permission
import flask,datetime
import pypinyin

from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,IntegerField,TextField,validators,SelectField
from wtforms.widgets import TextArea



def GetSecId():
    return int(datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"))



def choiceList(li):
    return [('Notset','Choose')] + [(jc,jc) for jc in li]



class Form1(FlaskForm):
    file1 = StringField()

class RecordForm(FlaskForm):
    time   = FloatField()
    record = StringField('description', widget=TextArea())

class Expform(FlaskForm):
    when  = StringField()
    where = StringField()
    what  = StringField()



class PeopleInforForm(FlaskForm):
    name = StringField(default='')
    sex  = SelectField(coerce = str ,choices = choiceList(['male','female']) )
    MBTI = SelectField(coerce = str ,choices = choiceList(['INTJ','INTP','INFJ','INFP',
                                                           'ISTJ','ISTP','ISFJ','ISFP',
                                                           'ENTJ','ENTP','ENFJ','ENFP',
                                                           'ESTJ','ESTP','ESFJ','ESFP',]))

    Birthday_Day   = SelectField(coerce = int ,choices = [(0,'Day')] + [(int(jc),str(jc)) for jc in range(1,32) ] )
    Birthday_Month = SelectField(coerce = int ,choices = [
                                                          (0 ,'Month'),
                                                          (1 ,'January'),
                                                          (2 ,'February'),
                                                          (3 ,'March'),
                                                          (4 ,'April'),
                                                          (5 ,'May'),
                                                          (6 ,'June'),
                                                          (7 ,'July'),
                                                          (8 ,'August'),
                                                          (9 ,'September'),
                                                          (10,'October'),
                                                          (11,'November'),
                                                          (12,'December'),    ] )
    Birthday_Year  = SelectField(coerce = int ,choices = [(0,'Year')] + [ (y,str(y)) for y in range(datetime.datetime.now().year,datetime.datetime.now().year-100,-1)] )
    bloodType = SelectField(coerce = str , choices = choiceList(['A','B','AB','O']) )
    HomeTown  = StringField(default='')
    NationID  = StringField(default='')

    Phone     = StringField(default='')
    Email     = TextField([ validators.Email()],default='')
    Address   = StringField(default='')
    Others    = StringField(default='')





class People():


# >>>>>>>>>>>>>> class method >>>>>>>>>>>>>>

    def SaveToDB(self):
        self.encObj.InsertDictIntoTable(partitionName='Relations',tableName='people',data=self.Dict,key=self.id)
        self.encObj.Save()
        # container = app.config['DATA_CONTAINER']
        # container.Save()

    # @staticmethod
    # def getPeoplelist():
    #     # return {  'id':dict   }
    #     container = app.config['DATA_CONTAINER']
    #     people    = container.GetTable('Relations')['people']
    #     return people
    @staticmethod
    def getPeoplelist():
        # return {  'id':dict   }
        encObj = app.config['DATA_CONTAINER']
        return encObj.getAllItemsInTable(partitionName='Relations',tableName='people')


    # @classmethod
    # def CreateNew(cls,name):
    #     uid = str(GetSecId())
    #     plist = cls.getPeoplelist()
    #     plist[uid] = {
    #        'name'  : name ,
    #        'id'    : uid  ,
    #        'Workl' : []   ,        # element:  {'itemid':int,  'when':str, 'where':str, 'what':str  }
    #        'Educl' : []   ,
    #        'Recdl' : []   ,        # element:  {'time':float,  'text':str,  'itemid':int  }
    #     }
    #     return cls(id = uid)
    @classmethod
    def CreateNew(cls,name):
        uid = str(GetSecId())
        Dict = {
           'name'  : name ,
           'id'    : uid  ,
           'Workl' : []   ,        # element:  {'itemid':int,  'when':str, 'where':str, 'what':str  }
           'Educl' : []   ,
           'Recdl' : []   ,        # element:  {'time':float,  'text':str,  'itemid':int  }
        }
        encObj = app.config['DATA_CONTAINER']
        encObj.InsertDictIntoTable(partitionName='Relations',tableName='people',data=Dict,key=uid)
        encObj.Save()
        return cls(id = uid)






    @staticmethod
    def calculateAge(born):
        if born is None: return 'X'
        if born.year>0 and born.month > 0 and born.day > 0:
            today = datetime.date.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        else:
            return 'X'

    @staticmethod
    def getZodiac(born):
        if born is None: return 'X'
        year = born.year
        Zodiac = u'猴鸡狗猪鼠牛虎兔龙蛇马羊'
        return Zodiac[year%12]


    @classmethod
    def SearchPeople(cls,txt):
        List = cls.getPeoplelist()
        r = []
        for id in List:
            Name = List[id]['name']
            NamePinyinIncluded = "".join(pypinyin.lazy_pinyin(Name))+Name
            if txt in NamePinyinIncluded:
                r.append([List[id]['name'],List[id]['id']])
        return r









# <<<<<<<<<<<<<< class method <<<<<<<<<<<<<<<<<
    def __init__(self,id=None):
        if id is None:
            self.Initiate = False
        else:
            self.encObj = app.config['DATA_CONTAINER']
            self.Initiate = True
            self.id       = id
            self.Dict     = self.encObj.getSelectByKey(partitionName='Relations',tableName='people',val=str(id))
            self.born     = self.GetBornByDict(self.Dict)
            self.age      = self.calculateAge(self.born)
            self.zodiac   = self.getZodiac(self.born)
        #-----------------------
        # attachme forms
        self.form1   = Form1()
        self.iform   = PeopleInforForm()
        self.expform = Expform()
        self.recform = RecordForm()


    @staticmethod
    def GetBornByDict(Dict):
        year  = Dict.get('Birthday_Year',0)
        month = Dict.get('Birthday_Month',0)
        day   = Dict.get('Birthday_Day',0)
        if year == 0 or month == 0 or day == 0 :
            return None
        else:
            return datetime.date(year, month, day)




    # form --> dict
    # auto save to DB
    def setInfo_formToDict(self,iform):
        if self.Initiate:
            for field in iform:
                if field.id == 'csrf_token': continue
                self.Dict[field.id] = field.data
            self.SaveToDB()

    #  dict  -->  form
    def setInfo_DictToform(self):
        if self.Initiate:
            for field in self.iform:
                if field.id == 'csrf_token': continue
                val = self.Dict.get(field.id,None)
                if val is not None:
                    field.default = val
            self.iform.process()



    def RerangeRecordByTime(self):
        td = { item['time']:item for item in self.Dict['Recdl'] }
        keys = list(td.keys())
        keys.sort()
        self.Dict['Recdl'] = [ td[key] for key in keys ]

    def GetRecordOBJ(self,itemid):
        for item in self.Dict['Recdl']:
            if item['itemid'] == itemid:
                return item
        return None

    def deleteRecored(self,itemid):
        for jc in range(len(self.Dict['Recdl'])):
            if self.Dict['Recdl'][jc]['itemid'] == itemid:
                del self.Dict['Recdl'][jc]






    #----------- used for both work and education
    def WriteExpItem(self,ExpDictKey,item):    # ExpDictKey = 'Workl' /  'Educl'
        listdict = self.Dict[ExpDictKey]
        if self.Initiate:
            if item['itemid'] == 0:
                item['itemid'] = GetSecId()
                listdict.append(item)
            else:
                targetjc = -1
                for jc in range(len(listdict)):
                    if listdict[jc]['itemid'] == item['itemid']:
                        targetjc = jc
                        break
                if targetjc == -1:print('ERROR: itemid = {} is not found in {}'.format(item['itemid'],listdict))
                listdict[targetjc] = item
            self.SaveToDB()



















@app.route('/Relation_list')
@permission.ValidForLogged
def Relation_list():
    people = People()

    return flask.render_template('Relation.html/Relation_list.html.j2',app=app,people=people)




@app.route('/Relation_people/<string:id>')
@permission.ValidForLogged
def Relation_people(id):
    people = People(id)
    people.setInfo_DictToform()
    return flask.render_template('Relation.html/Relation_people.html.j2',app=app,people=people)









# =======================
# action


@app.route('/Relation_createnew',methods=['post'])
@permission.ValidForLogged
def Relation_createnew():
    form = Form1()
    if form.validate_on_submit():
        Name = form.file1.data
        new = People.CreateNew(Name)
        new.SaveToDB()
    return flask.redirect(flask.url_for('Relation_people',id = new.id))



@app.route('/Relation_SavePersonInfor/<string:id>',methods=['post'])
@permission.ValidForLogged
def Relation_SavePersonInfor(id):
    form = PeopleInforForm()
    if form.validate_on_submit():
        people = People(id=id)
        people.setInfo_formToDict(form)
    return flask.redirect(flask.url_for('Relation_people',id = id))






@app.route('/Relation_WriteExperience/<string:id>/<string:category>/<int:itemid>',methods=['post'])
@permission.ValidForLogged
def Relation_WriteExperience(id,category,itemid):
    form = Expform()
    if form.validate_on_submit():
        people = People(id=id)
        people.WriteExpItem( ExpDictKey = category,
                             item = { 'itemid':itemid ,
                                       'when' :form.when.data  ,
                                       'where':form.where.data ,
                                       'what' :form.what.data  ,})
    return flask.redirect(flask.url_for('Relation_people',id = id))


@app.route('/Relation_Experience_MoveItem/<string:id>/<string:category>/<int:itemid>/<int:DeltaStep>')
@permission.ValidForLogged
def Relation_Experience_MoveItem(id,category,itemid,DeltaStep):
    DeltaStep -= 1 # -1 is illegal in link, seems so
    people = People(id=id)
    List = people.Dict[category]
    for jc in range(len(List)):
        if List[jc]['itemid'] == itemid:
            curr = jc;break
    if curr is None: print('itemid={} is not found in {}'.format(itemid,List))
    targ = curr + DeltaStep
    if targ in range(len(List)):
        List[curr],List[targ] = List[targ],List[curr]
    people.SaveToDB()
    return flask.redirect(flask.url_for('Relation_people',id = id))


@app.route('/Relation_Experience_DeleteItem/<string:id>/<string:category>/<int:itemid>')
@permission.ValidForLogged
def Relation_Experience_DeleteItem(id,category,itemid):
    people = People(id=id)
    List = people.Dict[category]
    for jc in range(len(List)):
        if List[jc]['itemid'] == itemid:
            target = jc;break
    if target is None: print('itemid={} is not found in {}'.format(itemid,List))
    del List[target]
    people.SaveToDB()
    return flask.redirect(flask.url_for('Relation_people',id = id))


@app.route('/Relation_AppendNewRecord/<string:id>', methods=['post'])
@permission.ValidForLogged
def Relation_AppendNewRecord(id):
    people = People(id=id)
    form = RecordForm()
    Recordlist = people.Dict['Recdl']
    if form.validate_on_submit():
        time = datetime.datetime.fromtimestamp(form.time.data)
        text = form.record.data
        #-----------------
        # check if the the text belongs to the same day
        Existjc = None
        for jc in range(len(Recordlist)):
            record_time = Recordlist[jc]['time']
            recordDate  = datetime.datetime.fromtimestamp(record_time)
            if recordDate.year == time.year and recordDate.month == time.month and recordDate.day == time.day:
                Existjc = jc
                break
        if Existjc is None: # new one
            Recordlist.append({ 'time':form.time.data, 'text':text, 'itemid':GetSecId()  })
            people.RerangeRecordByTime()
        else: # append
            Recordlist[Existjc]['text'] = Recordlist[Existjc]['text'] + "\n" + text
        people.SaveToDB()
    return flask.redirect(flask.url_for('Relation_people',id = id))


@app.route('/Relation_EditeRecord/<string:id>/<int:itemid>', methods=['post'])
@permission.ValidForLogged
def Relation_EditeRecord(id,itemid):
    people = People(id=id)
    form = RecordForm()
    Recordlist = people.Dict['Recdl']
    if form.validate_on_submit():
        record = people.GetRecordOBJ(itemid=itemid)
        if record is None:
            print('ERROR: itemid ={} is not found in {}'.format(itemid,people.Dict['Recdl']))
            return 'error'
        record['time'] = form.time.data
        record['text'] = form.record.data
        people.RerangeRecordByTime()
        people.SaveToDB()
    return flask.redirect(flask.url_for('Relation_people',id = id))


@app.route('/Relation_DeleteRecord/<string:id>/<int:itemid>')
@permission.ValidForLogged
def Relation_DeleteRecord(id,itemid):
    people = People(id=id)
    people.deleteRecored( itemid = itemid )
    people.SaveToDB()
    return flask.redirect(flask.url_for('Relation_people',id = id))
        #-----------------



@app.route('/Relation_SearchRecord/<string:txt>')
@permission.ValidForLogged
def Relation_SearchRecord(txt):
    List = People.SearchPeople(txt)
    def singleline(name,id):
        url = flask.url_for('Relation_people',id = id)
        return '''
             <a class="list-group-item list-group-item-action" href="{}" role="button">{}</a>'''.format(url,name)
    return str(' '.join( [ singleline(jc[0],jc[1]) for jc in  List]) )
        #-----------------
