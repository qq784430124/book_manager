from flask import Flask, render_template, url_for, request, redirect, g, flash, session, make_response
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = "crweewa42134"

DATABASE = r'C:\Users\lenovo\PycharmProjects\my_flask\db\book.sqlite'
IMAGE_FOLDER = r'C:\Users\lenovo\PycharmProjects\my_flask\static\image'


# 图片验证
def allowed_image(filename):
	_, ext = os.path.splitext(filename)
	return ext.lower() in ['.jpg', '.img', '.jpeg', '.png']


def return_dicts(cursor, row):
	return dict((cursor.description[i][0], value) for i, value in enumerate(row))


def conn_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		db.row_factory = return_dicts
	return db


def excute_sql(sql, prms=()):
	conn_db().cursor().execute(sql, prms)
	conn_db().commit()


def query_sql(sql, prms=()):
	return conn_db().cursor().execute(sql, prms).fetchall()


@app.teardown_appcontext
def close_conn(a):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()


@app.route('/')
def index():
	return redirect(url_for('book_list'))


@app.route('/logout')
def logout():
	resp = make_response(redirect(url_for('book_list')))
	resp.set_cookie('username', '', expires=datetime.now() + timedelta(days=-1))
	return resp


@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.cookies.get('username', None):
		return redirect(url_for('book_list'))
	else:
		if request.method == 'POST':
			username = request.form.get('username')
			password = request.form.get('password')
			sql = 'select count(*) AS [user] from admins WHERE username=?'
			sql2 = 'select count(*) AS [psw] from admins WHERE password=? AND username=?'
			user_count = query_sql(sql, (username,))
			if user_count[0]['user'] == 1:
				psw = query_sql(sql2, (password, username))
				if psw[0]['psw'] == 1:
					if request.form.get('cookies'):
						resp = make_response(redirect(url_for('book_list')))
						resp.set_cookie('username', username, path='/', expires=datetime.now() + timedelta(days=7))
					return resp
				else:
					flash('密码错误')
			else:
				flash('用户名不存在')

		return render_template('login.html')


@app.route('/book-list/')
def book_list():
	if request.cookies.get('username', None):
		title = '图书列表'
		search = request.args.get('key', '')
		sql = 'select b.*,c.category_name from books b INNER JOIN books_category c on b.book_category_id = c.category_id WHERE b.book_title LIKE ? ORDER BY submit_time DESC '
		books = query_sql(sql, ('%{}%'.format(search),))
		sql2 = 'select category_id, category_name from books_category'
		category = query_sql(sql2)
		return render_template('book_list.html', title=title, books=books, category=category)
	else:
		return redirect(url_for('login'))


@app.route('/release-book/')
def release_book():
	if request.cookies.get('username', None):
		title = "图书发布"
		sql = 'select category_id, category_name from books_category'
		category = query_sql(sql)
		return render_template('release_book.html', title=title, category=category)
	else:
		return redirect(url_for('login'))


@app.route('/delete_book/<book_id>')
def delate_book(book_id):
	sql2 = 'select book_cover from books where book_id=?'
	delate_book_cover = query_sql(sql2, (book_id,))
	sql = 'DELETE from books where book_id=?'
	excute_sql(sql, (book_id,))
	os.remove(delate_book_cover[0].get('book_cover', None))
	return redirect(url_for('book_list'))


@app.route('/book_post/', methods=['POST'])
def book_post():
	if request.method == 'POST':
		name = request.form['name']
		publisher = request.form['publisher']
		publish_time = request.form['publish-time']
		author = request.form['author']
		price = request.form['price']
		category_id = request.form['category']
		is_markdown = 1 if request.form.get('markdown', 0) == 'on' else 0
		is_add = 1 if request.form.get('add', 0) == 'on' else 0
		ISBN = request.form['ISBN']
		submit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		cover = request.files.get('bookcover', None)
		image_name = '11'

		if cover and allowed_image(cover.filename):
			image_name = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + os.path.splitext(cover.filename)[1]
			image_path = os.path.join(IMAGE_FOLDER, image_name)
			cover.save(image_path)

		sql = "insert into books (book_id, book_title, book_publisher, book_publish_time, book_author, book_price, book_category_id, book_markdown, book_add, submit_time, book_cover) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		excute_sql(sql,
		           (ISBN, name, publisher, publish_time, author, price, category_id, is_markdown, is_add, submit_time,
		            image_path))
		return redirect(url_for('book_list'))


if __name__ == '__main__':
	app.run(debug=True)
