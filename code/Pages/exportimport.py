

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
    kwDirct = encObj.getAllItemsInTable(partitionName='PasswordManager',tableName='keywords')
    tbNames = encObj.getAllTableNames('PasswordManager')
    dataDitc = {}
    for tb in tbNames:
        if tb[0:6] == "CLASS_":
            dataDitc[tb[6:]] = encObj.getAllItemsInTable(partitionName='PasswordManager',tableName=tb)
    Data['PasswordManager'] = {
        'keywords': kwDirct,
        'class': dataDitc,
    }
    #----------  relation  ------------
    Data['Relations'] = encObj.getAllItemsInTable(partitionName='Relations',tableName='people')
    #----------  diary  ------------
    Data['Diary'] = encObj.getAllItemsInTable(partitionName='Diary',tableName='list')
    buffer.write(   json.dumps(Data,indent = 4)  .encode('utf-8') )
    buffer.seek(0)
    # import pprint as pp
    # pp.pprint(Data,indent=4)
    # pp.pprint(app.config['DATA_CONTAINER'].container._Encryption__Dict,indent=4)
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
        kwDict = Data['PasswordManager']['keywords']
        clsDict = Data['PasswordManager']['class']
        encObj.CreatePartitionIfNotExist('PasswordManager')
        encObj.CreateTableIfNotExist(partitionName='PasswordManager',tableName='keywords')
        encObj.setAllItemsInTable(partitionName='PasswordManager',tableName='keywords',Dict=kwDict)
        for cls in clsDict:
            tb = 'CLASS_' + cls
            encObj.CreateTableIfNotExist(partitionName='PasswordManager',tableName=tb)
            encObj.setAllItemsInTable(partitionName='PasswordManager',tableName=tb,Dict=clsDict[cls])
        #-------- Diary  --------------
        encObj.CreatePartitionIfNotExist('Diary')
        encObj.CreateTableIfNotExist(partitionName='Diary',tableName='list')
        encObj.setAllItemsInTable(partitionName='Diary',tableName='list',Dict=Data['Diary'])
        #---------------------
        encObj.Save()
        #---------------------
        permission.SetLogout()
        return flask.redirect(flask.url_for('index'))
