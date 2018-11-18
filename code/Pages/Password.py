
from main import app,permission
import flask



from flask_wtf import FlaskForm
from wtforms import StringField


class AddClassForm(FlaskForm):
    Class = StringField('class')


class AddItemForm(FlaskForm):
    item = StringField('item')




@app.route('/Password')
@permission.ValidForLogged
def Password():
    classform = AddClassForm()
    return flask.render_template('Password.html/Password.html.j2',
    app=app,
    classform=classform)



@app.route('/PasswordClass/<string:Class>')
@permission.ValidForLogged
def PasswordClass(Class):
    classform = AddClassForm()
    itemform  = AddItemForm()

    return flask.render_template('Password.html/PasswordClass.html.j2',
    app = app,
    classform = classform,
    itemform  = itemform ,)



@app.route('/PasswordItem/<string:Class>/<string:item>')
@permission.ValidForLogged
def PasswordItem(Class,item):
    classform = AddClassForm()
    itemform  = AddItemForm()

    return flask.render_template('Password.html/PasswordItem.html.j2',
    app = app,
    classform = classform,
    itemform  = itemform ,)





















@app.route('/PasswordAddClass',methods=['post'])
@permission.ValidForLogged
def PasswordAddClass():
    form = AddClassForm()
    if form.validate_on_submit():
        newcls = form.Class.data
        container = app.config['DATA_CONTAINER']
        pm = container.GetTable('PasswordManager')
        pcls = pm.get('class')
        if newcls in pcls:
            flask.flash("class name '{}' exists!".format(newcls))
            return flask.redirect(  flask.session.get('SavingUrl','/')   )
        pcls[newcls] = {}
        container.Save()
        return flask.redirect( flask.url_for('PasswordClass' , Class = newcls)  )
    flask.flash("error! not valid submit")
    return flask.redirect(  flask.session.get('SavingUrl','/')   )



@app.route('/PasswordAddItem/<string:Class>',methods=['post'])
@permission.ValidForLogged
def PasswordAddItem(Class):
    form = AddItemForm()
    if form.validate_on_submit():
        newitem = form.item.data
        container = app.config['DATA_CONTAINER']
        pcls = container.GetTable('PasswordManager')['class'][Class]
        if newitem in pcls:
            flask.flash("iterm name '{}' exists!".format(newitem))
            return flask.redirect(  flask.session.get('SavingUrl','/')   )
        pcls[newitem] = {}
        container.Save()
        return flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = newitem )  )
    flask.flash("error! not valid submit in PasswordAddItem")
    return flask.redirect(  flask.session.get('SavingUrl','/')   )
