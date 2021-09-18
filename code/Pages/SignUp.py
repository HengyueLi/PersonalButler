
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
    encObj.CreateTableIfNotExist(tableName='PasswordManager', isSorted=True )
    #    store class name list, key1 = keyname, value = {keyname:anything}
    encObj.CreateTableIfNotExist(tableName='PasswordClassNameList' )
    #---------------------------
    # #   remember popular keywords    :   key:number
    encObj.CreateTableIfNotExist(tableName='keywords')
    #=======================================================
    #    Relations
    encObj.CreateTableIfNotExist(tableName='Relations')
    #=======================================================
    #    Diary
    encObj.CreateTableIfNotExist(tableName='Diary')
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
