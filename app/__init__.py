from flask import Flask
from flask_migrate import Migrate, MigrateCommand, init, migrate
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from app.main import bp_login, bp_book


app = Flask(__name__)
app.debug = True
app.secret_key = "crweewa42134"
app.register_blueprint(bp_login, url_prefix='/login')
app.register_blueprint(bp_book, url_prefix='/book')


IMAGE_FOLDER = r'C:\Users\lenovo\PycharmProjects\book_manager\app\static\cover'

app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	app.run()
