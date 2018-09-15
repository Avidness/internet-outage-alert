import smtplib
import configparser

class mailer:
	server = ""
	port = ""
	username = ""
	password = ""
	from_addr = ""
	to_addr = ""

	def __init__(self, config):
		self.server = config.get('MAIL', 'server')
		self.port = config.get('MAIL', 'port')
		self.username = config.get('MAIL', 'username')
		self.password = config.get('MAIL', 'password')
		self.from_addr = config.get('MAIL', 'from_addr')
		self.to_addr = config.get('MAIL', 'to_addr')

	def send(self, subject, body):
		msg = 'Subject: {}\n\n{}'.format(subject, body)
		server = smtplib.SMTP()
		server.connect(self.server, self.port)
		server.ehlo()
		server.starttls()
		server.login(self.username, self.password)
		server.sendmail(self.from_addr, self.to_addr, msg)
		server.quit()

