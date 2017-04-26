from app import mail
from flask_mail import Message
from flask import render_template, current_app
from threading import Thread


def async_send_email(app, msg):
	with app.app_context():
		mail.send(msg)


def send_email(to, subject):
	app = current_app._get_current_object()
	msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
	              sender=app.config['MAIL_SENDER'], recipients=[to]
	              )
	msg.body = '账号：henrry 密码：123'
	thr = Thread(target=async_send_email, args=[app, msg])
	thr.start()
	return thr
