#!/usr/bin/env python

import serial
import os
import subprocess
import sys
import time

debug = False

ser = serial.Serial(
               port='/dev/serial0',
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1
           )

def checkTVstatus():
       status=False
       output = subprocess.check_output("echo 'pow 0' | cec-client -s| tail -n12 | grep 'power status:' | awk '{print $3}'", shell=True)
       if output[:2] == "in" or output[:2] == "on":
          status =True
          return status
       if output[:2] == 'st':
          status = False
          return status
       if debug:
          print output, '\n',output[:2],'unknown value'
	  print ":".join("{:02x}".format(ord(c)) for c in output)
       return status

def writeBack(s):
	txt='\x02'+s+'\x03'
	ser.write(txt.encode())

# Switch to HDMI 1 on boot
os.system('echo "tx 4F:82:10:00" | cec-client -s> null')

while 1:
	       x=ser.readline()
               if debug:
		print ":".join("{:02x}".format(ord(c)) for c in x)
                print x
               if "\x02PON\x03" in x:
		if debug:
		  print "Power ON"
		writeBack("PON")
      		os.system('echo "on 0"| cec-client -s > null')
		counter=0
		active = True
                while not checkTVstatus() and counter <5:
      		  os.system('echo "on 0"| cec-client -s > null')
		  if debug:
			print "Retrying ON..."
		  counter = counter+1
	        # Switch to HDMI 1
      	        time.sleep(1)
		os.system('echo "tx 4F:82:10:00" | cec-client -s > null')
	       if "\x02POF\x03" in x:
		if debug:
		  print "Power OFF"
                os.system('echo "standby 0"| cec-client -s > null')
		writeBack("POF")
		counter=0
		while checkTVstatus() and counter <5:
                  os.system('echo "standby 0"| cec-client -s > null')
		  if debug:
			print "Retrying OFF..."
		  counter = counter+1
