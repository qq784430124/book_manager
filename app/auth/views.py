from . import bp_auth
from .forms import LoginForm, RegisterForm
from flask import render_template, url_for, redirect, request, flash
from ..models import User, db
from flask_login import login_user, logout_user, login_required
from ..mails import send_email


@bp_auth.route('/', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	form2 = RegisterForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('book.book_list'))
		flash('用户名或密码错误')
	return render_template('auth/login.html', form=form, form2=form2)


@bp_auth.route('/register', methods=['POST'])
def register():
	form = RegisterForm(request.form)
	if form.validate_on_submit():
		user = User()
		user.username = form.email.data
		user.password = form.password.data
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('book.book_list'))
	return redirect(url_for('auth.login'))


@bp_auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))
