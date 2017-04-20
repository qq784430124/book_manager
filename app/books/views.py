from datetime import datetime, timedelta
import os
from flask import request, render_template, \
	redirect, url_for, make_response, flash, current_app
from flask.views import MethodView
from .. import db
from ..models import User, Role, Book, Category
from .forms import *


class LogoutView(MethodView):
	def get(self):
		resp = make_response(redirect(url_for('login.login')))
		resp.set_cookie('username', expires=datetime.now() + timedelta(days=-1))
		return resp


class LoginView(MethodView):
	def get(self):
		return render_template('login.html')

	def post(self):
		if request.cookies.get('username', None):
			return redirect(url_for('book.book_list'))
		username = request.form.get('username', None)
		password = request.form.get('password', None)
		user = db.session.query(User).filter_by(username=username).first()
		if user and username == user.username:
			if password and password == user.password:
				if request.form.get('cookies', None):
					resp = make_response(redirect(url_for('book.book_list')))
					resp.set_cookie('username', username, expires=datetime.now() + timedelta(days=7))
					return resp
				else:
					resp = make_response(redirect(url_for('book.book_list')))
					resp.set_cookie('username', username)
					return resp
			else:
				flash('密码错误')
		else:
			flash('用户名不存在')
		return redirect(url_for('login.login'))


class BookListView(MethodView):
	def get(self):
		if request.cookies.get('username'):
			key = request.args.get('key', '')
			items = Book.query.filter(Book.title.like('%{}%'.format(key))).all()
			return render_template('book_list.html', items=items)


class BookDelateView(MethodView):
	def get(self):
		book = Book.query.filter_by(id=request.args.get('book_id')).first()
		db.session.delete(book)
		db.session.commit()
		return redirect(url_for('book.book_list'))


class BookReleaseView(MethodView):
	def get(self):
		# 判断是否存在地址栏参数book_id，是则为修改，否则为新建
		book_id = request.args.get('book_id', None)
		book = Book.query.filter_by(id=book_id).first() if book_id else Book()
		# 将数据填充到前台表单的输入框,参数obj接收一个sqlalchemy实例
		form = UserForm(obj=book)
		form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
		return render_template('release_book.html', form=form, book_id=book_id)

	@staticmethod
	# 图片验证
	def allowed_image(filename):
		_, ext = os.path.splitext(filename)
		return ext.lower() in ['.jpg', '.img', '.jpeg', '.png']

	def post(self):
		# 从前台表单中接收数据
		book_id = request.args.get('book_id', None)
		form = UserForm(request.form)
		form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
		if form.validate_on_submit():
			book = Book.query.filter_by(id=book_id).first() if book_id else Book()
			# 处理文件上传
			cover = request.files.get('cover', None)
			if cover and BookReleaseView.allowed_image(cover.filename):
				covername = form.title.data + '-' + datetime.now().strftime("%Y%m%d%H%M%S") + os.path.splitext(cover.filename)[1]
				cover.save(os.path.join(current_app.config['UPLOAD_FOLDER'], covername))
				form.cover.data = covername
			# 将接收到的表单数据填充到sqlalchemy实例中
			form.populate_obj(book)
			# 同样判断是改动还是新建
			if not book_id:
				db.session.add(book)
			db.session.commit()
			return redirect(url_for('book.book_list'))
		return render_template('release_book.html', form=form)
