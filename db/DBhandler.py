import sqlite3
from flask import g


class DBhandler:
	def __init__(self, database):
		self.database = database

	def return_dicts(self, cursor, row):
		return dict((cursor.description[i][0], value) for i, value in enumerate(row))

	def conn_db(self):
		db = getattr(g, '_database', None)
		if db is None:
			db = g._database = sqlite3.connect(self.database)
			db.row_factory = self.return_dicts
		return db

	def excute_sql(self, sql, prms=()):
		self.conn_db().cursor().execute(sql, prms)
		self.conn_db().commit()

	def query_sql(self, sql, prms=()):
		return self.conn_db().cursor().execute(sql, prms).fetchall()

DATABASE = r'C:\Users\lenovo\PycharmProjects\book_manager\db\book.sqlite'
DB = DBhandler(DATABASE)