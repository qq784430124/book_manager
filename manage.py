import os
from app import db, creat_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role, Book, Category, Article

app = creat_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Book=Book, Category=Category, Article=Article)

@manager.command
def test():
	"""运行单元测试"""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=3).run(tests)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
