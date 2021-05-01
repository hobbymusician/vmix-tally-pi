#!/usr/bin/env python2
import sys 
import time
import pycurl
from io import BytesIO
from colorsys import hsv_to_rgb
from unicornhatmini import UnicornHATMini

brightness=1.0
remotePort="8080"

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

print("""vMix Tally Light
Please make sure that the Web Controller in vMix 
on the host with IP address '{0:s}' is activated under
'Settings | Web Controller' for port '{1:d}'
and that your camera is named '{2:s}'!""".format(ipAddressServer, int(remotePort), cameraName))

unicornhatmini = UnicornHATMini()
unicornhatmini.set_brightness(0)

# Determine key for camera with given name
b_obj=BytesIO()
crl=pycurl.Curl()
crl.setopt(crl.URL, 'http://192.168.77.40:8088/tally')
crl.setopt(crl.WRITEDATA, b_obj)
crl.perform()
crl.close()
get_body = b_obj.getvalue()
print('%s' % get_body.decode('utf8'))
setupstr=get_body.decode('utf8')
b_obj.close()
prefix="\" class=\"tallyLink\">"+cameraName+"</a>"
endpos=setupstr.find(prefix)
print prefix
print endpos
startpos=endpos-36
if startpos>0:
	keystr=setupstr[startpos:endpos]
	urlstr="http://"+ipAddressServer+":"+remotePort+"/tallyupdate/?key="+keystr
	print urlstr
else:
	print "Did not find camera '"+cameraName+"'!"
	exit()
	

unicornhatmini.set_brightness(1)
hue = 1.0
r, g, b = [255, 255, 255]
unicornhatmini.set_all(r, g, b)
unicornhatmini.show()

while True:
	b_obj=BytesIO()
	crl=pycurl.Curl()
	#crl.setopt(crl.URL, 'http://192.168.77.40:8088/tallyupdate/?key=7befea86-01e1-44b0-a332-5c4ad8709f42')
	crl.setopt(crl.URL, urlstr)
	crl.setopt(crl.WRITEDATA, b_obj)
	crl.perform()
	crl.close()
	get_body = b_obj.getvalue()
	#print('%s' % get_body.decode('utf8'))
	changestr=get_body.decode('utf8')
	#changestr="tallyChange(\"#ff8c00\");"
	#changestr="tallyChange(\"#006400\");"
	a, colour, b = changestr.split("\"")
	#colour.removeprefix('#');
	colour=colour[1:]
	#print('%s' % colour)
	redstr=colour[:2]
	greenstr=colour[2:4]
	bluestr=colour[4:]
	r, g, b = [int(redstr, 16), int(greenstr, 16), int(bluestr, 16)]
	unicornhatmini.set_all(r, g, b)
	unicornhatmini.show()
	b_obj.close()
	time.sleep(0.2)
