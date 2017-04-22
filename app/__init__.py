from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
mail = Mail()


def creat_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)
	mail.init_app(app)

	from .books import bp_book, errors
	app.register_blueprint(bp_book, url_prefix='/book')

	return app
