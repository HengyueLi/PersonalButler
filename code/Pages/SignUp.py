
from main import app,permission

import flask,flask_wtf
import wtforms


class SignupForm(flask_wtf.FlaskForm):
    password = wtforms.PasswordField('Password')


PyDictFileEncy = app.config['ENCRYPTION_CLASS']

# #---------------------------------------------------------
# #   When user create new
# def CreateNewData(app,password):
#     flask.session['logged'] = True
#     #-----------------------------------------
#     file = app.config['PROFILE_DATA_FILE']
#     container = PyDictFileEncy(file,password)
#     app.config['DATA_CONTAINER'] = container
#     container.connect()
#     #=======================================================
#     #    PasswordManager
#     container.CreateTableIfNotExist('PasswordManager')
#     PassMan = container.GetTable('PasswordManager')
#     #---------------------------
#     #   set items into classes
#     PassMan['class'] = {}
#     #---------------------------
#     #   remember popular keywords    :   key:number
#     PassMan['keywords'] = {}
#     #=======================================================
#     #    Relations
#     container.CreateTableIfNotExist('Relations')
#     relations = container.GetTable('Relations')
#     relations['people'] = {}
#     #=======================================================
#     #    Diary
#     container.CreateTableIfNotExist('Diary')
#     diary = container.GetTable('Diary')
#     diary['list'] = []      #
#     #-------------------------------------------------------
#     container.Save()

#---------------------------------------------------------
#   When user create new
def CreateNewData(app,password):
    flask.session['logged'] = True
    #-----------------------------------------
    encObj = PyDictFileEncy(password) #container = encObj
    app.config['DATA_CONTAINER'] = encObj
    encObj.connect()
    #=======================================================
    #    PasswordManager
    pName = 'PasswordManager'
    encObj.CreatePartitionIfNotExist(pName)
    #---------------------------
    #   set items into classes
    # 原class下面的dict集合则用"CLASS_"做表的prefix来区分
    # #---------------------------
    # #   remember popular keywords    :   key:number
    encObj.CreateTableIfNotExist(partitionName=pName,tableName='keywords')
    #=======================================================
    #    Relations
    pName = 'Relations'
    encObj.CreatePartitionIfNotExist(pName)
    encObj.CreateTableIfNotExist(partitionName=pName,tableName='people')
    #=======================================================
    #    Diary
    pName = 'Diary'
    encObj.CreatePartitionIfNotExist(pName)
    encObj.CreateTableIfNotExist(partitionName=pName,tableName='list')  #
    #-------------------------------------------------------
    encObj.Save()




@app.route('/SignUp')
@permission.ValidForUnLogged
def SignUp():
    sgform = SignupForm()
    return flask.render_template('SignUp.html.j2',app=app,sgform=sgform)



@app.route('/createnew',methods=['post'])
@permission.ValidForUnLogged
def createnew():
    form = SignupForm()
    if form.validate_on_submit():
        password = form.password.data
        CreateNewData(app,password)
        return flask.redirect('login')
    else:
        return flask.redirect('SignUp')
