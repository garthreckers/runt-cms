import smtplib

class RuntMail():
	def __init__(self):
		pass

	def new_user(self, email, username):
		message = """From: <runt@localhost>
			To: <""" + email + """>
			MIME-Version: 1.0
			Content-type: text/html
			Subject: SMTP HTML e-mail test

			This is an e-mail message to be sent in HTML format

			<b>This is HTML message.</b>
			<h1>This is headline.</h1>
			"""

		try:
			smtpObj = smtplib.SMTP('localhost')
			smtpObj.sendmail("runt@localhost", email, message)         
			print("Successfully sent email")
		except smtplib.SMTPException:
			print("Error: unable to send email")

