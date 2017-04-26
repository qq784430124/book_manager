from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(UserMixin, db.Model):
	"""用户表"""
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text, unique=True)
	password_hash = db.Column(db.Text)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))

	def __repr__(self):
		return '<用户；{}>'.format(self.username)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


class Role(db.Model):
	"""用户角色"""
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, unique=True)

	def __repr__(self):
		return '<角色{}：{}>'.format(self.id, self.name)


class Book(db.Model):
	"""图书"""
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	publisher = db.Column(db.Text)
	author = db.Column(db.Text)
	price = db.Column(db.Float)
	cover = db.Column(db.Text)
	ISBN = db.Column(db.Text)
	category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))

	category = db.relationship('Category', backref=db.backref('books', lazy='dynamic'))

	def __repr__(self):
		return '<图书：{}>'.format(self.title)


class Category(db.Model):
	"""图书分类"""
	__tablename__ = 'categorys'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, unique=True)

	def __repr__(self):
		return '<分类：{}>'.format(self.name)
