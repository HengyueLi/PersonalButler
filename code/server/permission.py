
import flask
from functools import wraps


class permission():


    @staticmethod
    def ValidForLogged(f):
        @wraps(f)
        def decorated(*args,**kargs):
            IsLogged = flask.session.get('logged',False)
            if IsLogged:
                return f(*args,**kargs)
            else:
                return flask.redirect(flask.url_for('login'))
        return decorated

    @staticmethod
    def ValidForUnLogged(f):
        @wraps(f)
        def decorated(*args,**kargs):
            IsLogged = flask.session.get('logged',False)
            if IsLogged:
                return flask.redirect(flask.url_for('profile'))
            else:
                return f(*args,**kargs)
        return decorated
