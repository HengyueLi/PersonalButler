
from main import app,permission
import flask

from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,IntegerField,TextField,validators,SelectField
from wtforms.widgets import TextArea



class DiaryForm(FlaskForm):
    id     = IntegerField()
    time   = FloatField()
    title  = StringField()
    record = StringField('description', widget=TextArea())




class DiaryObj():



    @classmethod
    def GetDiaryObjList( cls ):
        # return [   ]
        container = app.config['DATA_CONTAINER']
        diarylist = container.GetTable('Diary')['list']
        return [ cls(Dict=d) for d in diarylist ]



    # Dict is the item saved in DB directly
    def __init__(self,Dict = None):
        if Dict is not None:
            self.Dict = Dict
            self.initiated = True
            return
        else:
            print('ERROR: no valid input in ini@DiaryObj')















@app.route('/Diary/<int:pageindex>',methods=['get'])
@permission.ValidForLogged
def Diary(pageindex):

    # N_page = 50
    DiaryObjList = DiaryObj.GetDiaryObjList()
    return flask.render_template('Diary.html/Diary.html.j2',app = app,DiaryObjList=DiaryObjList)



@app.route('/Diary_createNew',methods=['get'])
@permission.ValidForLogged
def Diary_createNew():


    return flask.render_template('Diary.html/Diary_CreateNew.html.j2',app = app)
