from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blog_flask_pkg.config import Config


mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.Login' #for loginrequired decorator
login_manager.login_message_category = 'info'
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from blog_flask_pkg.users.routes import users
    from blog_flask_pkg.posts.routes import posts
    from blog_flask_pkg.main.routes import main
    from blog_flask_pkg.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
