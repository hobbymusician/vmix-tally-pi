#!/usr/bin/env python2
import time
import sys
from enum import Enum

from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
from unicornhatmini import UnicornHATMini

import pycurl
from io import BytesIO

class tallyState(Enum):
	SEARCHING_CAM = 1
	CAM_FOUND = 2
	
def displayError(text):
	unicornhatmini.set_brightness(0.1)
	hue = 1.0
	r, g, b = [255, 255, 255]
	unicornhatmini.set_all(0, 0, 0)
	unicornhatmini.show()
	
	text_width, text_height = font.getsize(text)
	image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
	draw = ImageDraw.Draw(image)
	draw.text((display_width, -1), text, font=font, fill=255)
	offset_x = 0

	while True:
		for y in range(display_height):
			for x in range(display_width):
				hue = 1
				r, g, b = [255, 255, 255]
				if image.getpixel((x + offset_x, y)) == 255:
					unicornhatmini.set_pixel(x, y, r, g, b)
				else:
					unicornhatmini.set_pixel(x, y, 0, 0, 0)

		offset_x += 1
		if offset_x + display_width > image.size[0]:
			return

		unicornhatmini.show()
		time.sleep(0.05)

def searchCam():
	# Determine key for camera with given name
	b_obj=BytesIO()
	try: 
		crl=pycurl.Curl()
		urlstr="http://"+ipAddressServer+":"+remotePort+"/tally"
		crl.setopt(crl.URL, urlstr)
		crl.setopt(crl.WRITEDATA, b_obj)
		crl.perform()
		crl.close()
	except pycurl.error as exc:
		errstr="Unable to reach %s (%s)" % (urlstr , exc)
		print (errstr)
		displayError(errstr)
		return ""			
	get_body = b_obj.getvalue()
	setupstr=get_body.decode('utf8')
	b_obj.close()
	prefix="\" class=\"tallyLink\">"+cameraName+"</a>"
	endpos=setupstr.find(prefix)
	startpos=endpos-36
	if startpos>0:
		keystr=setupstr[startpos:endpos]
		urlstr="http://"+ipAddressServer+":"+remotePort+"/tallyupdate/?key="+keystr
		print ("Trying to fetch tally status from '"+urlstr+"'")
		return urlstr
	else:
		print ("Did not find camera '"+cameraName+"'!")
		displayError("Did not find camera '"+cameraName+"'!")
		return ""
	
	
def readColor(urlstr):
	b_obj=BytesIO()
	try: 
		crl=pycurl.Curl()
		crl.setopt(crl.URL, urlstr)
		crl.setopt(crl.WRITEDATA, b_obj)
		crl.perform()
		crl.close()
	except pycurl.error as exc:
		errstr="Unable to reach %s (%s)" % (urlstr , exc)
		print (errstr)
		displayError(errstr)		
		return False	
	get_body = b_obj.getvalue()
	changestr=get_body.decode('utf8')
	a, colour, b = changestr.split("\"")
	colour=colour[1:]
	#print('%s' % colour)
	redstr=colour[:2]
	greenstr=colour[2:4]
	bluestr=colour[4:]
	r, g, b = [int(redstr, 16), int(greenstr, 16), int(bluestr, 16)]
	unicornhatmini.set_all(r, g, b)
	unicornhatmini.show()
	b_obj.close()
	return True

	
count=0
for argument in sys.argv:
	if (count==1):
		cameraName=argument
	if (count==2):
		ipAddressServer=argument
	if (count==3):
		remotePort=argument
	count=count+1

if (count<3 or count >=5):
	print("Usage: tally.p ""<Kamera Name>"" <ip_address> [<port>] ")
	exit()

remotePort="8088"


print("""vMix Tally Light
================
Please make sure that the Web Controller in vMix 
on the host with IP address '{0:s}' is activated under
'Settings | Web Controller' for port '{1:d}'
and that your camera is named '{2:s}'!
""".format(ipAddressServer, int(remotePort), cameraName))

# Initialize Unicorn Hat Mini
brightness=1.0
unicornhatmini = UnicornHATMini()
rotation = 0
unicornhatmini.set_rotation(rotation)
display_width, display_height = unicornhatmini.get_shape()
font = ImageFont.truetype("MiniFont.ttf", 8)

# Initial state within the infinite loop
state=tallyState.SEARCHING_CAM

while True:
	if state == tallyState.SEARCHING_CAM:
		unicornhatmini.set_brightness(0)
		camUrlStr=searchCam()
		if camUrlStr != "":
			state=tallyState.CAM_FOUND
			unicornhatmini.set_brightness(0.5)
			hue = 1.0
	elif state == tallyState.CAM_FOUND:
		if not readColor(camUrlStr):
			state=tallyState.SEARCHING_CAM
	time.sleep(0.2)
		
