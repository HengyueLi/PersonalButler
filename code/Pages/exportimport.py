

from main import app,permission

import flask,os,tempfile,json
from io import BytesIO



@app.route('/exportData')
@permission.ValidForLogged
def exportData():
    encObj = app.config['DATA_CONTAINER']
    buffer = BytesIO()
    Data = {}
    #---------- CONFIG -----
    Data['CONFIG'] = {'PASSWORD':encObj.getPassword()}
    #----------  password data  ------------
    #
    kwDirct = [ {item['k']:item['v']} for item in encObj.getAllItems(tableName='keywords') ]
    # classNames = [ d['k'] for d in encObj.getAllItems('PasswordClassNameList') ]
    # for clsN in dataDitc:
    #     l = encObj.selectItems(tableName='PasswordManager', key1=clsN, key2=None )
    #     dataDitc[clsN] = {  d['itemname']:d for d in l }
    Data['PasswordManager'] = {
        # 'classNames' : classNames,
        'keywords': kwDirct,
        'data': encObj.getAllItems(tableName='PasswordManager'),
    }
    #----------  relation  ------------
    Data['Relations'] = encObj.getAllItems(tableName='Relations')
    #----------  diary  ------------
    Data['Diary'] = encObj.getAllItems(tableName='Diary')
    buffer.write(   json.dumps(Data,indent = 4)  .encode('utf-8') )
    buffer.seek(0)
    return flask.send_file(buffer, as_attachment=True,attachment_filename='export.json')#,mimetype='text/csv')





@app.route("/importData", methods=["POST"])
@permission.ValidForLogged
def importData():
    if flask.request.files:
        encObj = app.config['DATA_CONTAINER']
        importedFile = flask.request.files["file"]
        Data = json.loads(importedFile.read().decode())
        #-------  config --------
        password = Data['CONFIG']['PASSWORD']
        encObj.ResetPassword(password)
        #------- PasswordManager ------
        # classNames = Data['PasswordManager']['classNames']
        kwDict = Data['PasswordManager']['keywords']
        clsDict = Data['PasswordManager']['data']
        RelDict = Data['Relations']
        # app.config['fun_FUM'].ResetTable(encObj,tableName='PasswordClassNameList',DictList= [ {"k":i,"v":""}  for i in classNames] ,key1='k',key2=None)
        app.config['fun_FUM'].ResetTable(encObj,tableName='keywords',DictList=kwDict,key1='k',key2=None)
        app.config['fun_FUM'].ResetTable(encObj,tableName='PasswordManager',DictList=clsDict,key1='class',key2='itemname')
        app.config['fun_FUM'].ResetTable(encObj,tableName='Relations',DictList=RelDict,key1='id',key2=None)
        app.config['fun_FUM'].ResetTable(encObj,tableName='Diary',DictList=Data['Diary'],key1='id',key2=None)


        #
        # encObj.CreatePartitionIfNotExist('PasswordManager')
        # encObj.CreateTableIfNotExist(partitionName='PasswordManager',tableName='keywords')
        # encObj.setAllItemsInTable(partitionName='PasswordManager',tableName='keywords',Dict=kwDict)
        # for cls in clsDict:
        #     tb = 'CLASS_' + cls
        #     encObj.CreateTableIfNotExist(partitionName='PasswordManager',tableName=tb)
        #     encObj.setAllItemsInTable(partitionName='PasswordManager',tableName=tb,Dict=clsDict[cls])
        # #-------- Relation  --------------
        # encObj.CreatePartitionIfNotExist('Relations')
        # encObj.CreateTableIfNotExist(partitionName='Relations',tableName='people')
        # encObj.setAllItemsInTable(partitionName='Relations',tableName='people',Dict=Data['Relations'])
        # #-------- Diary  --------------
        # encObj.CreatePartitionIfNotExist('Diary')
        # encObj.CreateTableIfNotExist(partitionName='Diary',tableName='list')
        # encObj.setAllItemsInTable(partitionName='Diary',tableName='list',Dict=Data['Diary'])
        #---------------------
        encObj.Save()
        #---------------------
        permission.SetLogout()
        return flask.redirect(flask.url_for('index'))
