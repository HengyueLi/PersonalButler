

from main import app

import flask,os






@app.route('/')
def index():
    if app.config['ENCRYPTION_CLASS'].IsUserNew():
        return flask.redirect( flask.url_for('SignUp')  )
    else:
        return flask.redirect( flask.url_for('login')  )
