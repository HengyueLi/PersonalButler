

from main import app,permission

import flask,os
import wtforms,flask_wtf





class ChangePasswordForm(flask_wtf.FlaskForm):
    password = wtforms.PasswordField('Password')
    confirm  = wtforms.PasswordField('Confirm password')




@app.route('/ChangePassword')
@permission.ValidForLogged
def ChangePassword():
    cpform = ChangePasswordForm()
    return flask.render_template('ChangePassword.html.j2',app=app,cpform=cpform)



@app.route('/ChangePassword_PostForm' , methods = ['post'] )
@permission.ValidForLogged
def ChangePassword_PostForm():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        confirm  = form.confirm.data
        if password == confirm:
            container = app.config['DATA_CONTAINER']
            container.ResetPassword(password)
            container.Save()
        else:
            flask.flash('The confirmed password is incorrect!')
    else:
        flask.flash('Change password: faild')
    permission.SetLogout()
    return flask.redirect( '/' )
