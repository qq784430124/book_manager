from flask import Blueprint

bp_book = Blueprint('book', __name__)

from .views import *

bp_book.add_url_rule('/', view_func=BookListView.as_view('book_list'))
bp_book.add_url_rule('/delate/', view_func=BookDelateView.as_view('book_delate'))
bp_book.add_url_rule('/release/', view_func=BookReleaseView.as_view('book_release'))
