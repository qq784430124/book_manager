import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hdafhjalh32342'
	SQALCHEMY_COMMIT_ON_TEARDOWN = True
	MAIL_SERVER = 'smtp.qq.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_TO = os.environ.get('MAIL_TO')
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_SENDER = '784430124@qq.com'
	MAIL_SUBJECT_PREFIX = '[HenrryZ]'
	# FLASK_ADMIN = os.environ.get('FLASK_ADMIN')

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_ECHO = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

	COVER_FOLDER = os.path.join(basedir, r'\app\static\cover')


class TestingConfig(Config):
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SQLALCHEMY_ECHO = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
