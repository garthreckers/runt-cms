import smtplib
import config
from email.mime.text import MIMEText

class RuntMail():
	def __init__(self):
		pass

	def new_user(self, email, username):
		if not config.PRODUCTION: return

		msg = MIMEText("""\
				A new user has been created with the username {uname} and the email {email}
			""".format(uname=username, email=email))

		msg['Subject'] = 'Your account has been created'
		msg['From'] = config.TEMP_EMAIL
		msg['To'] = email

		# Send the message via our own SMTP server, but don't include the
		# envelope header.
		s = smtplib.SMTP('localhost')
		s.sendmail(me, [you], msg.as_string())
		s.quit()

