from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '0d3f3c52060e609d524bdaa415ec700c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

login_manager = LoginManager(app)
login_manager.login_view = 'Login' #for loginrequired decorator
login_manager.login_message_category = 'info'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from blog_flask_pkg import routes