from app import mail
from flask_mail import Message
from flask import render_template, current_app
from threading import Thread


def async_send_mail(app, msg):
	with app.app_context():
		mail.send(msg)


def send_email(subject):
	app = current_app._get_current_object()
	msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
	              sender=app.config['MAIL_SENDER'], recipients=["qq784430124@gmail.com"]
	              )
	msg.body = 'haha'
	msg.html = render_template('book_list.html')
	thr = Thread(target=async_send_mail, args=[app, msg])
	thr.start()
	return thr
