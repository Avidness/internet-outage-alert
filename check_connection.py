import os
import time
import configparser
import datetime as dt
from dateutil import relativedelta as rd
from mailer import mailer

def generate_msg(lost_at, recovered_at):
	msg = '\nLost connection at {}'.format(lost_at.strftime('%c'))
	msg += '\nRecovered at {}'.format(recovered_at.strftime('%c'))
	msg += '\nDown for {} minutes'.format(rd.relativedelta(recovered_at, lost_at).minutes)
	return msg

def poll_internet(mailer, ip, interval):
	was_connected = True
	lost_at = dt.datetime.now()

	while True:
		response = os.system('ping -c 1 ' + ip)
		is_connected = response == 0

		now = dt.datetime.now()
		if not is_connected and was_connected:
			lost_at = now

		if is_connected and not was_connected:
			msg = generate_msg(lost_at, now)
			mailer.send('Internet Downtime', msg)

		was_connected = is_connected
		time.sleep(interval if is_connected else 5)

config = configparser.ConfigParser()
config.read('config.ini')

mailer = mailer(config)
ip = config.get('POLL', 'ip')
interval = int(config.get('POLL', 'ping_interval_secs'))

poll_internet(mailer, ip, interval)
