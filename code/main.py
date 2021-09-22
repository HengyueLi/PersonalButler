#!/usr/bin/env python3

import sys,os



Code_path     = os.path.dirname(os.path.abspath(__file__))
Project_path  = os.path.dirname(Code_path)
serverside    = os.path.join(Code_path, "server")



#-------------------------------------------------------------------------------------------
#     create app
import flask
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS,'templates')
    static_folder = os.path.join(sys._MEIPASS,'static')
    app = flask.Flask(__name__, template_folder = template_folder,static_folder = static_folder)
else:
    app = flask.Flask(__name__)

#-------------------------------------------------------------------------------------------
app.config['SECRET_KEY'] = os.urandom(24)

#------------------  encryption API -------------------------------------------------
from DataAPI.encryptionAPI import EncryptionAPI
# from DataAPI.encryptionAPI_sqlcipher import EncryptionAPI

#----------------------------------------------------------------------



app.config['ENCRYPTION_CLASS'] = EncryptionAPI
app.config['DATA_CONTAINER'] = {}
#-------------------------------------------------------------------------------------------
#      markdown support
import flaskext.markdown
flaskext.markdown.Markdown(app)





from server.permission import permission
from server.FUM        import FUM
app.config['fun_FUM'] = FUM
#-------------------------------------------------------------------------------------------
#  render all the pages
from Pages import *











#--------------------------------------------------------------------------------------------
#    Run
if __name__ == '__main__':
    host = '0.0.0.0'
    port = 4999
    print('''
   ╔═════════════════════════════════════════════════════
   ║ profile={}
   ║┌────────────────────────────┐
   ║   http://localhost:{}
   ║└────────────────────────────┘
   ╚═════════════════════════════════════════════════════
    '''.format(str( EncryptionAPI.getDataSource()  ),port))
    app.run(host=host, port=port, debug= True )
