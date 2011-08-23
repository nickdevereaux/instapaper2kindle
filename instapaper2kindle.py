#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import cookielib, urllib, urllib2, socket, httplib
import ConfigParser


VERSION = '0.1'
print '\nkindle2instapaper v%s'%VERSION
print 'written by Nick Devereaux (nickjdevereaux',
print '@ gmail.com)\n'

loginurl = 'http://www.instapaper.com/user/login'
sendtokindleurl = 'http://www.instapaper.com/user/kindle_send_now'
kindleurl = 'http://www.instapaper.com/user/kindle'
cookiename = "instapaper.cookie"

try:
	from BeautifulSoup import BeautifulSoup
except ImportError, e:
	print 'ERROR: Please install BeautifulSoup'
	print 'eg: pip install BeautifulSoup'
	quit()
try:
	import requests
except ImportError, e:
	print 'ERROR: Please install requests'
	print 'eg: pip install requests'
	quit()

version_info = tuple([ int(num) for num in requests.__version__.split('.')])
if version_info < (0,6,1):
	print 'ERROR: You\'ll need to update your copy of requests'
	print 'Your version %s is less than the required 0.6.1'%requests.__version__
	quit()

#main app
def sendtokindle():
	readconfig()
	if(username == ""):
		print u'ERROR! \u0ca0_\u0ca0', 
		print " Please set a username in settings.cfg file"
		quit()
	http_args = urllib.urlencode(dict(username=username, password=password))
	print 'Logging in with username %s...'%username,
	r = requests.post(loginurl,data=http_args)
	if(r.cookies is None):
		print 'failed.'
		print 'ERROR: Failed to login. Please check your settings'
		quit()
	print 'success.'
	c = r.cookies
	#get page check if we are logged in
	kindlepage = requests.get(kindleurl,cookies=c)
	http_args = urllib.urlencode(dict(form_key=getformkey(kindlepage.content)))
	print 'Submitting form...',
	formresult = requests.post(sendtokindleurl,data=http_args, cookies=c)
	if(formresult.status_code == 200):
		print 'Success! =D'
	else:
		print 'Failed =('

def readconfig():
	config = ConfigParser.RawConfigParser()
	config.read(os.path.join(sys.path[0],'settings.cfg'))
	global username
	global password
	username = config.get('credentials','username') 
	password = config.get('credentials','password') 

def getformkey(content):
	soup = BeautifulSoup(content)
	search = soup.findAll('input',attrs={'id':'form_key_send_now'})
	if(len(search) != 1):
		print 'ERROR: Page structure changed, couldn\'t find form key'
		print 'Please email me at nickjdevereaux',
		print '@ gmail.com'
		quit()
	return search[0]['value']
	

if __name__ == "__main__":
	sendtokindle()



