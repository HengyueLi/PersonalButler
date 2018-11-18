
from main import app,permission
import flask



@app.route('/profile')
@permission.ValidForLogged
def profile():
    return flask.render_template('profile.html.j2',app=app)
