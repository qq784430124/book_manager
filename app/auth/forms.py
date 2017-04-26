from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
from ..models import User


class LoginForm(FlaskForm):
	username = StringField([DataRequired('请输入用户名'), Length(1, 20)])
	password = PasswordField([DataRequired('请输入密码'), Length(1, 20)])
	remember_me = BooleanField()


class RegisterForm(FlaskForm):
	email = StringField('邮箱', [DataRequired('必填'), Length(1, 64), Email('格式不正确')])
	password = PasswordField('密码', [DataRequired('必填'), Length(1, 20), EqualTo('password2', message='密码不一致')])
	password2 = PasswordField('确认密码', [DataRequired('必填'), Length(1, 20)])

	def validate_email(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('邮箱已注册')
