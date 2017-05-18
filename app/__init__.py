from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'
login_manager.session_protection = 'strong'


def creat_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)
	mail.init_app(app)
	login_manager.init_app(app)

	from .books import bp_book, errors
	from .auth import bp_auth
	from .articles import bp_article
	app.register_blueprint(bp_auth, url_prefix='/auth')
	app.register_blueprint(bp_book, url_prefix='/book')
	app.register_blueprint(bp_article, url_prefix='/article')

	return app
