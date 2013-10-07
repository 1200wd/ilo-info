#!/usr/bin/python

import requests
import json
import sys
import argparse

def get(host, user, passwd, label):
	url = 'https://%s/json/login_session' % host
	post = '{"method":"login","user_login":"%s","password":"%s"}' % (user, passwd)

	s = requests.Session()
	r = s.post(url, data=post, verify=False)

	if r.status_code == 403:
		print >> sys.stderr, '[ERROR] Could not login'
		sys.exit()

	dataurl = 'https://%s/json/health_temperature' % host
	r = s.get(dataurl, verify=False)
	data = json.loads(r.text)

	# loop list to find the value we need
	for item in data['temperature']:
		if item['label'] == label.strip():
			return item['currentreading']


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='iLO-info gets temperature readings from iLO.')
	parser.add_argument('--user', dest='user', required=True, help='iLO user to login with')
	parser.add_argument('--pass', dest='passwd', required=True, help='iLO password')
	parser.add_argument('--label', dest='label', required=True, help='The label for the value to get. For example "01-Inlet Ambient"')
	parser.add_argument('host', help='The iLO host')
	args = parser.parse_args()

	print get(args.host, args.user, args.passwd, args.label)
