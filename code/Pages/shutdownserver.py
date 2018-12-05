
from main import app,permission

import flask











#--------------------------------------------------
#shutdown
@app.route('/shutdownserver')
@permission.ValidForLogged
def shutdownserver():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'
