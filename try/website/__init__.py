import eventlet
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import login_manager, LoginManager

from flask_socketio import SocketIO

from flask import Blueprint

main = Blueprint('main', __name__)
views = Blueprint('views', __name__)
auth = Blueprint('auth', __name__)


db = SQLAlchemy()
DB_NAME = "database.db"
socketio = SocketIO()


def create_app():
    ''' This function Creates the website application '''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ASAFASAF'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
    db.init_app(app)


    print('running 1')
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note


    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    socketio.init_app(app)
    print('running 2')

    return app

def create_database(app):
    ''' This function checks if the database exists, and creates it '''
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
