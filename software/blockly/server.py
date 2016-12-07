import os, os.path
import random
import string
from subprocess import Popen
import subprocess

import cherrypy
import simplejson
import serial

def forward(serialDevice):
	cmd = bytearray(['<',3,100])
	serialDevice.write(cmd)
	waitCmd(serialDevice)

def left(serialDevice):
	cmd = bytearray(['<',1,90])
	serialDevice.write(cmd)
	waitCmd(serialDevice)

def right(serialDevice):
	cmd = bytearray(['<',2,90])
	serialDevice.write(cmd)
	waitCmd(serialDevice)

def beep(serialDevice):
	cmd = bytearray(['<',4,0])
	serialDevice.write(cmd)
	waitCmd(serialDevice)


ser = serial.Serial( '/dev/rfcomm0', 9600 )

ser.flushInput()
ser.flushOutput()	


def waitCmd(serialDevice):
	cmd = []
	count = 0

	while True:
		print 'pong'
		for c in serialDevice.read():
			print 'ping'
			cmd.append(c)
			count = count + 1
			if ( count >= 3 ):
				break
		if ( count >= 3 ):
			break

	print cmd
			

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """
"""

    @cherrypy.expose
    def displaycode(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        cherrypy.log( rawbody )
	
	i = len(rawbody)
	
	for actionnum in range(1,i-1):
		action = rawbody[actionnum]
		cherrypy.log(rawbody[actionnum])
		if action == '0':
			cherrypy.log("forward")
			forward(ser);
		if action == '1':
			cherrypy.log("left" )
			left(ser)
		if action == '2':
			cherrypy.log("right")
			right(ser)
		if action == '3':
			cherrypy.log("beep")
			beep(ser)

        return 'OK'

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

if __name__ == '__main__':
	
	
	conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd()),
	     'tools.staticfile.filename': os.path.abspath(os.getcwd()) + '/code.html'
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './'
         }
     }

	cherrypy.config.update({'log.error_file': 'Web.log',
                'log.access_file': 'Access.log'
               })

	cherrypy.config.update({'server.socket_port': 7077})


	cherrypy.quickstart(StringGenerator(), '/', conf)
