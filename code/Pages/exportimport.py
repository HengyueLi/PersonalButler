

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
    Data['PasswordManager'] = {
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
        kwDict = [ {'k':list(d.keys())[0],'v':list(d.values())[0]} for d in Data['PasswordManager']['keywords'] ]
        clsDict = Data['PasswordManager']['data']
        RelDict = Data['Relations']
        app.config['fun_FUM'].ResetTable(encObj,tableName='keywords',DictList=kwDict,key1='k',key2=None)
        app.config['fun_FUM'].ResetTable(encObj,tableName='PasswordManager',DictList=clsDict,key1='class',key2='itemname')
        app.config['fun_FUM'].ResetTable(encObj,tableName='Relations',DictList=RelDict,key1='id',key2=None)
        app.config['fun_FUM'].ResetTable(encObj,tableName='Diary',DictList=Data['Diary'],key1='id',key2=None)
        #---------------------
        encObj.Save()
        #---------------------
        permission.SetLogout()
        return flask.redirect(flask.url_for('index'))
