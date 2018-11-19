#!/usr/bin/env python3

import sys,os



Code_path     = os.path.dirname(os.path.abspath(__file__))
Project_path  = os.path.dirname(Code_path)
PagesPath     = os.path.join(Code_path, "Pages")
serverside    = os.path.join(Code_path, "server")
datafile      = os.path.join(Code_path, "profile.dat")

sys.path.insert(0, PagesPath )
sys.path.insert(0, serverside)


#-------------------------------------------------------------------------------------------
#     create app
import flask
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


app.config['PROFILE_DATA_FILE'] = datafile
app.config['DATA_CONTAINER'] = {}
#-------------------------------------------------------------------------------------------
#      time js
from flask_moment import Moment
moment = Moment(app)







from permission import permission
from FUM        import FUM
app.config['fun_FUM'] = FUM
#-------------------------------------------------------------------------------------------
#  render all the pages
from Pages import *












#--------------------------------------------------------------------------------------------
#    Run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug= True )
