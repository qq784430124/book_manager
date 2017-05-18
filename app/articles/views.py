from . import bp_article
from flask import request, redirect, render_template
from .forms import ArticleForm
from ..models import Article


@bp_article.route('/')
def article_list():
	key = request.args.get('key', '')
	page = request.args.get('page', 1, int)
	items = Article.query.filter(Article.title.like('%{}%'.format(key))).paginate(page, per_page=10)
	return render_template('article/article_list.html', pagination=items)


@bp_article.route('/edit', methods=['GET', 'POST'])
def article_edit():
	form = ArticleForm()
	if form.validate_on_submit():
		a = request.form.get('text1')
		return str(a)
	return render_template('article/article_edit.html', form=form)
