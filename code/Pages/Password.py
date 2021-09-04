
from main import app,permission
import flask
import pypinyin



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

    # @classmethod
    # def InserNew(cls,Class,Item,Timesec):
    #     container = app.config['DATA_CONTAINER']
    #     pclass    = container.GetTable('PasswordManager')['class'].get(Class,None)
    #     if pclass is None:
    #         return [ False , 'Class name {} does not exist!'.format(Class)  ]
    #     if Item  in pclass:
    #         return [ False , 'Item name {} exist! Use a different name'.format(Item)  ]
    #     pclass[Item] = {
    #     'createtime': Timesec ,
    #     'actions'   : [ ]     ,
    #     'data'      : {}      ,
    #     }
    #     return [True,   cls(Class = Class,Item = Item)   ]
    @classmethod
    def InserNew(cls,Class,Item,Timesec):
        encObj = app.config['DATA_CONTAINER']
        # pclass    = container.GetTable('PasswordManager')['class'].get(Class,None)
        pclass = app.config['fun_FUM'].Password_getClassName(encObj)
        pName = 'PasswordManager'
        tName = 'CLASS_'+Class
        if Class not in pclass:
            return [ False , 'Class name {} does not exist!'.format(Class)  ]
        q = encObj.getSelectByKey(partitionName=pName,tableName=tName,val=Item)
        if q is not None:
            return [ False , 'Item name {} exist! Use a different name'.format(Item)  ]
        data =   {
        'createtime': Timesec ,
        'actions'   : [ ]     ,
        'data'      : {}      ,
        }
        encObj.InsertDictIntoTable(partitionName=pName,tableName=tName,data=data,key = Item)
        return [True,   cls(Class = Class,Item = Item)   ]




    @staticmethod
    def SearchPass(txt):
        container = app.config['DATA_CONTAINER']
        Allclass  = container.GetTable('PasswordManager')['class']
        r = []
        for classkey in Allclass:
            for itemkey in Allclass[classkey]:
                # consider pinyin
                pinyinIncluded = "".join(pypinyin.lazy_pinyin(itemkey))+itemkey
                if txt.lower() in pinyinIncluded.lower():
                    r.append([  classkey,  itemkey  ])
        return r




    # def __init__(self,Class,Item):
    #     self.container = app.config['DATA_CONTAINER']
    #     self.allclass  = self.container.GetTable('PasswordManager')['class']
    #     self.classdict = self.allclass[Class]
    #     self.itemname  = Item
    #     self.item      = self.classdict.get(Item,None)
    #     if self.item is None:
    #         self.IsInitiated = False
    #     self.data = self.item['data']
    #     self.actRec = self.item['actions']
    #     self.IsInitiated = True
    def __init__(self,Class,Item):
        pName = 'PasswordManager'
        tName = "CLASS_" + Class
        self.encObj = app.config['DATA_CONTAINER']
        self.itemname  = Item
        self.className = Class
        self.item = self.encObj.getSelectByKey(partitionName=pName,tableName=tName,val = self.itemname)
        if self.item is None:
            self.IsInitiated = False
        self.data = self.item['data']
        self.actRec = self.item['actions']
        self.IsInitiated = True

    def Save(self):
        self.encObj.Save()

    def RecordAction(self,actype,actime,actkey,actval):
        # actype = [ 'create' , 'change' , 'delete' ]
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

    def ReSetValue(self,key,val,time):
        if key not in self.item['data']:
            return [False,'key {} does not exist in iterm!'.format(key)]
        self.item['data'][key] = val
        self.RecordAction(actype='change',actime=time,actkey=key,actval=val)
        return [True,0]

    def DeleteKey(self,key,time):
        if key not in self.item['data']:
            return [False,'key {} does not exist in iterm!'.format(key)]
        del self.item['data'][key]
        self.RecordAction(actype='delete',actime=time,actkey=key,actval= '')
        return [True,0]

    def Reclassify(self,newclass):
        pName = 'PasswordManager'
        tName_newcls = "CLASS_"+newclass
        tName_curcls = "CLASS_"+self.className
        DesCls = self.encObj.getAllItemsInTable(partitionName=pName,tableName=tName_newcls)
        check = DesCls.get(self.itemname,None)
        if check is None:
            # DesCls[self.itemname] = dict(self.item)
            self.encObj.InsertDictIntoTable(partitionName=pName,tableName=tName_newcls,data=dict(self.item),key=self.itemname)
            # del self.classdict[self.itemname]
            self.encObj.DeleteItemFromTable(partitionName=pName,tableName=tName_curcls,key=self.itemname)
            return [True,0]
        else:
            return [ False,"item '{}' already exists in the destination class '{}' ".format(self.itemname,newclass)  ]




    # return List1,List2,   List2 contains the less porpular keys
    def GetPopularKeyList(self):
        #   length of List1
        LenL1 = 5
        # kwcounter = self.container.GetTable('PasswordManager')['keywords']
        kwcounter = self.encObj.getAllItemsInTable(partitionName='PasswordManager',tableName='keywords')
        # keys = list(kwcounter.keys())
        L = [kv[0] for kv in sorted(kwcounter.items(), key=lambda x: x[1])]
        L = list(reversed(L))
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




@app.route('/PasswordActionRecord/<string:Class>/<string:item>')
@permission.ValidForLogged
def PasswordActionRecord(Class,item):

    itemobj   = ObjItem( Class=Class , Item=item )

    return flask.render_template('Password.html/PasswordActionRecord.html.j2',
    app = app,
    itemobj = itemobj ,

    )















@app.route('/PasswordAddClass',methods=['post'])
@permission.ValidForLogged
def PasswordAddClass():
    form = AddClassForm()
    if form.validate_on_submit():
        newcls = form.Class.data
        encObj = app.config['DATA_CONTAINER']
        # tbs = encObj.getAllTableNames('PasswordManager')
        # pcls = [ tb.replace('CLASS_','') for tb in tbs if 'CLASS_' in tb]
        pcls = app.config['fun_FUM'].Password_getClassName(encObj)
        if newcls in pcls:
            flask.flash("class name '{}' exists!".format(newcls))
            return flask.redirect(  flask.session.get('SavingUrl','/')   )
        encObj.CreateTableIfNotExist('PasswordManager','CLASS_'+newcls)
        encObj.Save()
        return flask.redirect( flask.url_for('PasswordClass' , Class = newcls)  )
    flask.flash("error! not valid submit")
    return flask.redirect(  flask.session.get('SavingUrl','/')   )

# @app.route('/PasswordAddClass',methods=['post'])
# @permission.ValidForLogged
# def PasswordAddClass():
#     form = AddClassForm()
#     if form.validate_on_submit():
#         newcls = form.Class.data
#         container = app.config['DATA_CONTAINER']
#         pm = container.GetTable('PasswordManager')
#         pcls = pm.get('class')
#         if newcls in pcls:
#             flask.flash("class name '{}' exists!".format(newcls))
#             return flask.redirect(  flask.session.get('SavingUrl','/')   )
#         pcls[newcls] = {}
#         container.Save()
#         return flask.redirect( flask.url_for('PasswordClass' , Class = newcls)  )
#     flask.flash("error! not valid submit")
#     return flask.redirect(  flask.session.get('SavingUrl','/')   )



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
            encObj = app.config['DATA_CONTAINER']
            # kwcounter = container.GetTable('PasswordManager')['keywords']
            kwcounter = encObj.getAllItemsInTable(partitionName='PasswordManager',tableName='keywords')
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


@app.route('/ReviseKeyvalPair/<string:Class>/<string:item>',methods=['post'])
@permission.ValidForLogged
def ReviseKeyvalPair(Class,item):
    form = KeyValPairForm()
    Return = flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = item )  )
    if form.validate_on_submit():
        key  = form.key .data
        val  = form.val .data
        time = form.time.data
        obj  = ObjItem(Class=Class,Item=item)
        if obj.IsInitiated:
            r = obj.ReSetValue(key,val,time)
            if r[0]:
                obj.Save()
            else:
                flask.flash(r[1])
            return Return
        else:
            flask.flash( "(class={},key={}) is not found".foramt(Class,key))
            return Return
    flask.flash("error! not valid submit in ReviseKeyvalPair")
    return Return




@app.route('/DeleteKeyvalPair/<string:Class>/<string:item>',methods=['post'])
@permission.ValidForLogged
def DeleteKeyvalPair(Class,item):
    form = KeyValPairForm()
    Return = flask.redirect( flask.url_for('PasswordItem' , Class = Class , item = item )  )
    if form.validate_on_submit():
        key  = form.key .data
        val  = form.val .data
        time = form.time.data
        obj = ObjItem(Class=Class,Item=item)
        obj.DeleteKey(key=key,time=time)
        obj.Save()
        return Return
    flask.flash("error! not valid submit in DeleteKeyvalPair")
    return Return


@app.route('/ReclassifyItem/<string:Class>/<string:item>/<string:ClassNew>',methods=['get'])
@permission.ValidForLogged
def ReclassifyItem(Class,item,ClassNew):
    if Class != ClassNew:
        itmobj = ObjItem(Class,item)
        r = itmobj.Reclassify( ClassNew )
        if r[0]:
            returncls = ClassNew
            itmobj.Save()
        else:
            flask.flash(r[1])
    else:
        flask.flash("please choose a different class")
        returncls = Class
    return flask.redirect( flask.url_for('PasswordItem' , Class = returncls , item = item )  )


@app.route('/Password_Search/<string:txt>')
@permission.ValidForLogged
def Password_Search(txt):
    List = ObjItem.SearchPass(txt)
    def singleline(clskey,itmkey):
        url = flask.url_for('PasswordItem',Class=clskey,item=itmkey)
        return '''
         <a class="list-group-item list-group-item-action" href="{}" role="button"> {} @ {}</a>'''.format(url,itmkey,clskey)
    return str(' '.join( [ singleline(jc[0],jc[1]) for jc in  List]) )
        #-----------------
