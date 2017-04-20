from flask import Blueprint

bp_login = Blueprint('login', __name__)
bp_book = Blueprint('book', __name__)

from app.main.views import *

bp_login.add_url_rule('/', view_func=LoginView.as_view('login'))
bp_login.add_url_rule('/', view_func=LogoutView.as_view('logout'))

bp_book.add_url_rule('/', view_func=BookListView.as_view('book_list'))
bp_book.add_url_rule('/delate/', view_func=BookDelateView.as_view('book_delate'))
bp_book.add_url_rule('/release/', view_func=BookReleaseView.as_view('book_release'))
