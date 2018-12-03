
from main import app,permission
import flask






@app.route('/Relation')
@permission.ValidForLogged
def Relation():
    
    return flask.render_template('Relation.html/BasePage.html.j2',app=app,)
