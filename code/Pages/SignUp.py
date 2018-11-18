
from main import app,permission

import flask,flask_wtf
import wtforms
from pydictfileency import PyDictFileEncy


class SignupForm(flask_wtf.FlaskForm):
    password = wtforms.PasswordField('Password')




#---------------------------------------------------------
#   When user create new
def CreateNewData(app,password):
    flask.session['logged'] = True
    #-----------------------------------------
    file = app.config['PROFILE_DATA_FILE']
    container = PyDictFileEncy(file,password)
    app.config['DATA_CONTAINER'] = container
    container.connect()
    #-------------------------------------------------------
    container.CreateTableIfNotExist('PasswordManager')
    g = container.GetTable('PasswordManager')
    g['class'] = {}
    #-------------------------------------------------------
    container.CreateTableIfNotExist('Relations')
    container.CreateTableIfNotExist('Diary')
    container.Save()






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
