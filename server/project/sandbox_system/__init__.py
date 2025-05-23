import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4'.format(**{
        'user': os.getenv('DB_USER', 'hoge'),
        'password': os.getenv('DB_PASSWORD', 'huga'),
        'host': os.getenv('DB_HOST', '172.18.0.1'),
        'database': os.getenv('DB_DATABASE', 'sandbox')
    })
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

def localize_callback(*args, **kwargs):
    return 'このページにアクセスするにはログインが必要です'
login_manager.localize_callback = localize_callback

# from sqlalchemy.engine import Engine
# from sqlalchemy import event

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()

from sandbox_system.users.view import users
from sandbox_system.blogs.view import blogs
from sandbox_system.chats.view import chats
from sandbox_system.events.view import events
from sandbox_system.error_page.error_page import error_pages

app.register_blueprint(users)
app.register_blueprint(blogs)
app.register_blueprint(chats)
app.register_blueprint(events)
app.register_blueprint(error_pages)