#!/usr/bin/env python3

import sys,os



Code_path     = os.path.dirname(os.path.abspath(__file__))
Project_path  = os.path.dirname(Code_path)
serverside    = os.path.join(Code_path, "server")
# datafile      = os.path.join(os.getcwd(), "profile.dat")




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

#----------------------------------------------------------------------
# encryption API
# from rudeencrypt import Encryption as PyDictFileEncy
from server.encryptionAPI import EncryptionAPI
#----------------------------------------------------------------------



app.config['ENCRYPTION_CLASS'] = EncryptionAPI
# app.config['ENCRYPTION_DATA']  = EncryptionAPI.getDataSource()
app.config['DATA_CONTAINER'] = {}
#-------------------------------------------------------------------------------------------
#      time js
# from flask_moment import Moment
# from static_moment.flask_moment import Moment
# moment = Moment(app)
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




    # linux
    # webbrowser.open(url='http://0.0.0.0:4999', new=1)
