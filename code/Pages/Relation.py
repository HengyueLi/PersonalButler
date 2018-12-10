
from main import app,permission
import flask,datetime

from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,IntegerField,TextField,validators






class Form1(FlaskForm):
    file1 = StringField()


# class PeopleInforForm(FlaskForm):
#     name = StringField('name',default='')
#     sex  = IntegerField('sex',default=0 )   # 0:none , 1:male , 2:female
#     MBTI = StringField('MBTI',default='0')
#     Birthday_Day   = IntegerField('Birthday_Day',default=0)
#     Birthday_Month = IntegerField('Birthday_Month',default=0)
#     Birthday_Year  = IntegerField('Birthday_Year',default=0)
#     bloodType = StringField('bloodType',default='')
#     HomeTown  = StringField('HomeTown',default='')
#     NationID  = StringField('NationID',default='')
#     Phone     = StringField('Phone',default='')
#     Email     = TextField("Email",[ validators.Email()],default='')
#     Others    = StringField('Others',default='')
class PeopleInforForm(FlaskForm):
    name = StringField(default='')
    sex  = IntegerField(default=0 )   # 0:none , 1:male , 2:female
    MBTI = StringField(default='0')
    Birthday_Day   = IntegerField(default=0)
    Birthday_Month = IntegerField(default=0)
    Birthday_Year  = IntegerField(default=0)
    bloodType = StringField(default='')
    HomeTown  = StringField(default='')
    NationID  = StringField(default='')
    Phone     = StringField(default='')
    Email     = TextField([ validators.Email()],default='')
    Others    = StringField(default='')





class People():
# >>>>>>>>>>>>>> class method >>>>>>>>>>>>>>

    @staticmethod
    def SaveToDB():
        container = app.config['DATA_CONTAINER']
        container.Save()


    @staticmethod
    def getPeoplelist():
        # return {  'ID':dict   }
        container = app.config['DATA_CONTAINER']
        people    = container.GetTable('Relations')['people']
        return people



    @classmethod
    def CreateNew(cls,name):
        uid = datetime.datetime.utcnow().strftime('"%Y%m%d%H%M%S"')
        plist = cls.getPeoplelist()
        plist[uid] = {
           'name'  : name ,
           'id'    : uid  ,
           'Workl' : []   ,
           'Educl' : []   ,
           'Recdl' : []   ,
        }
        return cls(id = uid)


# <<<<<<<<<<<<<< class method <<<<<<<<<<<<<<<<<

    def __init__(self,id=None):
        if id is None:
            self.Initiate = False
        else:
            self.Initiate = True
            self.id       = id
            self.Dict     = self.getPeoplelist()[id]
        #-----------------------
        # attachme forms
        self.form1 = Form1()
        self.iform = PeopleInforForm()

    # auto save to DB
    def setInfo_formToDict(self):
        if self.Initiate:
            for field in self.iform:
                if field.id == 'csrf_token': continue
                self.Dict[field.id] = field.data
            self.SaveToDB()

    def setInfo_DictToform(self):
        if self.Initiate:
            for field in self.iform:
                if field.id == 'csrf_token': continue
                val = self.Dict.get(field.id,None)
                if val is not None:
                    field.default = val
            self.iform.process()














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













@app.route('/Relation_createnew',methods=['post'])
@permission.ValidForLogged
def Relation_createnew():
    form = Form1()
    if form.validate_on_submit():
        Name = form.file1.data
        new = People.CreateNew(Name)
        new.SaveToDB()
    return flask.redirect(flask.url_for('Relation_people',id = new.id))
