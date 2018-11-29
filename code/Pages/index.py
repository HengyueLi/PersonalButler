

from main import app

import flask,os






@app.route('/')
def index():
    if os.path.exists(app.config['PROFILE_DATA_FILE']):
        return flask.redirect( flask.url_for('login')  )
    else:
        return flask.redirect( flask.url_for('SignUp')  )
