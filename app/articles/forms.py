from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
	title = StringField('标题', [DataRequired('请输入标题')])
	body = StringField('正文', [DataRequired('请输入正文')])

