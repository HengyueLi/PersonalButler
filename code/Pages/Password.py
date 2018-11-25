
from main import app,permission
import flask



from flask_wtf import FlaskForm
from wtforms import StringField,FloatField


class AddClassForm(FlaskForm):
    Class = StringField('class')


class AddItemForm(FlaskForm):
    item = StringField('item')
    time = FloatField('time')

class KeyValPairForm(FlaskForm):
    key  = StringField('key')
    val  = StringField('val')
    time = FloatField('time')







#---------------------------------------
# ObjItem(Class,Item)
class ObjItem():

    @classmethod
    def InserNew(cls,Class,Item,Timesec):
        container = app.config['DATA_CONTAINER']
        pclass    = container.GetTable('PasswordManager')['class'].get(Class,None)
        if pclass is None:
            return [ False , 'Class name {} does not exist!'.format(Class)  ]
        if Item  in pclass:
            return [ False , 'Item name {} exist! Use a different name'.format(Item)  ]
        pclass[Item] = {
        'createtime': Timesec ,
        'actions'   : [ ]     ,
        'data'      : {}      ,
        }
        return [True,   cls(Class = Class,Item = Item)   ]




    def __init__(self,Class,Item):
        self.container = app.config['DATA_CONTAINER']
        self.item = self.container.GetTable('PasswordManager')['class'][Class].get(Item,None)
        if self.item is None:
            self.IsInitiated = False
        self.data = self.item['data']
        self.IsInitiated = True


    def Save(self):
        self.container.Save()

    def RecordAction(self,actype,actime,actkey,actval):
        # actype = [ 'create' , 'change' ]
        al = self.item['actions']
        al.append({
            'actype':actype,
            'actime':actime,
            'actkey':actkey,
            'actval':actval,
        })

    # return [TF,reminder]
    def InserKeyvalPair(self,key,val,time):
        if key in self.item['data']:
            return [False,'key {} exists in iterm!'.format(key)]
        self.item['data'][key] = val
        self.RecordAction(actype='create',actime=time,actkey=key,actval=val)
        return [True,0]


    # def GetKeyValCounter(self):
    #     kwcounter = self.container.GetTable('PasswordManager')['keywords']
    #     return kwcounter


    # return List1,List2,   List2 contains the less porpular keys
    def GetPopularKeyList(self):
        #   length of List1
        LenL1 = 5
        kwcounter = self.container.GetTable('PasswordManager')['keywords']
        # keys = list(kwcounter.keys())
        L = [kv[0] for kv in sorted(kwcounter.items(), key=lambda x: x[1])]
        L1 = L[0:LenL1]
        L2 = L[LenL1:]
        return L1,L2
















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
    kvform    = KeyValPairForm()
    objitem   = ObjItem( Class=Class , Item=item )

    return flask.render_template('Password.html/PasswordItem.html.j2',
    app = app,
    objitem = objitem,
    classform = classform,
    itemform  = itemform ,
    kvform    = kvform   ,)





















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
        newitem    = form.item.data
        createtime = form.time.data
        r = ObjItem.InserNew(Class = Class,Item = newitem,Timesec = createtime)
        if r[0] :
            item = r[1]
            item.Save()
            return flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = newitem )  )
        else:
            flask.flash(r[1])
            return flask.redirect(  flask.session.get('SavingUrl','/')   )
    flask.flash("error! not valid submit in PasswordAddItem")
    return flask.redirect(  flask.session.get('SavingUrl','/')   )




@app.route('/PasswordAddKeyvalPair/<string:Class>/<string:item>',methods=['post'])
@permission.ValidForLogged
def PasswordAddKeyvalPair(Class,item):
    form = KeyValPairForm()
    if form.validate_on_submit():
        key  = form.key .data
        val  = form.val .data
        time = form.time.data
        obj  = ObjItem(Class=Class,Item=item)
        r = obj.InserKeyvalPair(key=key,val=val,time=time)
        if r[0]:
            #---count key frequency
            container = app.config['DATA_CONTAINER']
            kwcounter = container.GetTable('PasswordManager')['keywords']
            if key in kwcounter:
                kwcounter[key] += 1
            else:
                kwcounter[key]  = 1
            obj.Save()
            return flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = item )  )
        else:
            flask.flash(r[1])
            return flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = item )  )
    flask.flash("error! not valid submit in PasswordAddKeyvalPair")
    return flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = item )  )


# @app.route('/ReviseKeyvalPair/<string:Class>/<string:item>',methods=['post'])
# @permission.ValidForLogged
# def ReviseKeyvalPair(Class,item):
#     form = KeyValPairForm()
#     if form.validate_on_submit():
#         key  = form.key .data
#         val  = form.val .data
#         time = form.time.data
#         obj  = ObjItem(Class=Class,Item=item)
#         r = obj.InserKeyvalPair(key=key,val=val,time=time)
#         if r[0]:
#             pass
#             return flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = item )  )
#         else:
#             flask.flash(r[1])
#             return flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = item )  )
#     flask.flash("error! not valid submit in PasswordAddKeyvalPair")
#     return flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = item )  )
