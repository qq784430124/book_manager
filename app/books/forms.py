from flask_wtf import FlaskForm
from wtforms.validators import *
import wtforms


class BookForm(FlaskForm):
	title = wtforms.StringField('书名', [DataRequired('请输入标题')])
	publisher = wtforms.StringField('出版社', [DataRequired('请输入出版社')])
	author = wtforms.StringField('作者', [DataRequired('请输入作者')])
	price = wtforms.DecimalField('售价', [DataRequired('请输入售价')])
	cover = wtforms.FileField('封面')
	ISBN = wtforms.StringField('ISBN', [DataRequired('请输入ISBN号')])
	category_id = wtforms.SelectField('分类', coerce=int)
