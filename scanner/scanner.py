#!/usr/bin/python3
import cv2
from pyzbar.pyzbar import decode
import time
import paho.mqtt.client as mqtt
from matplotlib import pyplot as plt
import http.server
import socketserver
import argparse
import threading


# optional functionn to check if there is working camera port
def list_ports():
    """
    Test the ports and returns a tuple with the available ports 
    and the ones that are working.
    """
    is_working = True
    dev_port = 0
    working_ports = []
    available_ports = []
    while is_working:
        print('opening port %s' %dev_port)
        camera = cv2.VideoCapture(dev_port, cv2.CAP_DSHOW)
        print('opened port %s' %dev_port)
        if not camera.isOpened():
            is_working = False
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports



# Project using external usb webcam
def main(port, mode):
    print('start')
    #connecting to mqtt protocol
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(port, mode)
    # https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640*1)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480*1)
    # cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    print(cap)
    LastReadTime = 0
    cooldown = 1

# variables for changing focus
    focusMin = 50
    focusMax = 200
    step = 10
    focus = focusMin
    direction = step

    time_cap = 0
    time_cap_counter = 0
    time_decode = 0
    time_decoder_counter = 0

    while True:
        cap.set(cv2.CAP_PROP_FOCUS, focus)
        focus += direction
        

        if direction > 0 and focus >= focusMax:
            direction = -step

        if direction < 0 and focus <= focusMin:
            direction = step

        t = time.time()
        succes, img = cap.read()

       
        
        
        time_cap += time.time() - t
        time_cap_counter += 1
        # print(succes)
        # print(img)
        if(succes):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # img = cv2.GaussianBlur(img, (5, 5), 0)
            
            cv2.imwrite("stream/image1.jpeg", img)

            # decoding
            t = time.time()
            barcodes = decode(img)
            time_decode += time.time() - t
            time_decoder_counter += 1
            for barcode in barcodes:
                currentTime = time.time()
                if currentTime - LastReadTime > cooldown:
                    print(barcode.data)
                    myData = barcode.data.decode('utf-8')
                    print(myData)
                    client.publish("scan/code", myData)
                    LastReadTime = currentTime
        else:
            print("image not captured")

        print(focus, time_cap/time_cap_counter, time_decode/time_decoder_counter)
        # print(focus)
        # cv2.imshow('Result', img)
        # cv2.waitKey(1)

    


#commands usefull for mosquitto server 
# mosquitto_sub -h localhost -t skan/kod
# mosquitto_pub.exe -m "123" -t /test/rtu

# main(0, cv2.CAP_DSHOW) #If it's not working use CAP_DSHOW or CAP_V4L2
# main(0, cv2.CAP_DSHOW)

# list_ports()

def run_http_server():

	PORT 		= 8000
	DIRECTORY 	= "web"
	
	# Handler = http.server.SimpleHTTPRequestHandler
	
	class Handler(http.server.SimpleHTTPRequestHandler):
	    def __init__(self, *args, **kwargs):
	        super().__init__(*args, directory=DIRECTORY, **kwargs)
	
	with socketserver.TCPServer(("", PORT), Handler) as httpd:
	    print("Serving at port", PORT)
	    httpd.serve_forever()

# parse CLI arguments
parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument("foo", ..., required=True)
# parser.add_argument('--http.server',action=argparse.BooleanOptionalAction)
# parser.set_defaults(http=False)
parser.add_argument('--http',action='store_true')
args = parser.parse_args()

print(args)

#if args.http == True :
	# run_http_server()
	thread = threading.Thread(None, run_http_server)
	thread.start()
	

# ... do things ...

# Shutdown server
server.shutdown()
thread.join()
	
	    