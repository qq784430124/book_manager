from flask import Flask
from flask_migrate import Migrate, MigrateCommand, init, migrate
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def creat_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)

	from app.books import bp_book
	app.register_blueprint(bp_book, url_prefix='/book')

	return app


