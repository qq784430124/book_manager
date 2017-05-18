from flask import Blueprint

bp_article = Blueprint('article', __name__)

from . import views