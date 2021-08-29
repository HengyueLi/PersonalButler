
from main import app,permission

import os,flask,flask_wtf


import wtforms


PyDictFileEncy = app.config['ENCRYPTION_CLASS']


class LoginForm(flask_wtf.FlaskForm):
    password = wtforms.PasswordField('Password')






@app.route('/login')
@permission.ValidForUnLogged
def login():
    if app.config['ENCRYPTION_CLASS'].IsUserNew():
        return flask.redirect('SignUp')
    lgiform = LoginForm()
    return flask.render_template('login.html.j2',app=app,lgiform=lgiform)







@app.route('/loginCheckpassword',methods=['post'])
@permission.ValidForUnLogged
def loginCheckpassword():
    if app.config['ENCRYPTION_CLASS'].IsUserNew():
        return flask.redirect('SignUp')
    form = LoginForm()
    if form.validate_on_submit():
        encObj = PyDictFileEncy(form.password.data)
        encObj.connect()
        if encObj.IsConnected():
            app.config['DATA_CONTAINER'] = encObj
            permission.SetLogin()

            return flask.redirect( flask.url_for('profile') )
        else:
            return 'error'
    
# @app.route('/loginCheckpassword',methods=['post'])
# @permission.ValidForUnLogged
# def loginCheckpassword():
#     db = app.config['PROFILE_DATA_FILE']
#     if not os.path.exists(db):
#         return flask.redirect('SignUp')
#     form = LoginForm()
#     if form.validate_on_submit():
#         container = PyDictFileEncy(db,form.password.data)
#         container.connect()
#         if container.IsConnected():
#             app.config['DATA_CONTAINER'] = container
#             # flask.session['logged'] = True
#             permission.SetLogin()
#             return flask.redirect( flask.url_for('profile') )
#         else:
#             return 'error'
