
from main import app,permission

import os,signal
import flask











#--------------------------------------------------
#shutdown
@app.route('/shutdownserver')
@permission.ValidForLogged
def shutdownserver():
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'
