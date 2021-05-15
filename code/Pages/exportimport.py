

from main import app,permission

import flask,os,tempfile,json
from io import BytesIO



@app.route('/exportData')
@permission.ValidForLogged
def exportData():
    buffer = BytesIO()
    decryptedData = app.config['DATA_CONTAINER'].getDecryptedData_Dict()
    buffer.write(   json.dumps(decryptedData,indent = 4)  .encode('utf-8') )
    buffer.seek(0)
    return flask.send_file(buffer, as_attachment=True,attachment_filename='export.json')#,mimetype='text/csv')





@app.route("/importData", methods=["POST"])
@permission.ValidForLogged
def importData():
    if flask.request.files:
        importedFile = flask.request.files["file"]
        app.config['DATA_CONTAINER'].setByDecryptedData(   json.loads(importedFile.read().decode())   )
        app.config['DATA_CONTAINER'].Save()
        permission.SetLogout()
        return flask.redirect(flask.url_for('index'))
