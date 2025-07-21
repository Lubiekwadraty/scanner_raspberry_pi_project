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
import _thread as thread
import os

# 
# -------------------------------------------------
# list_ports 
# optional functionn to check if there is working camera port
# -------------------------------------------------
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

# -------------------------------------------------
# decodeMain
# -------------------------------------------------
def decodeMain(port, mode, client):
    print('start')
    
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(port, mode)
    # https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640*1)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480*1)
    # cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    
    #possible = cap.set(cv2.CAP_PROP_MODE, cv2.CAP_MODE_GRAY)
    #print("CAP_MODE_GRAY: " + possible)    
    
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

    # check if cammera can work in manual focus
    possible = cap.set(cv2.CAP_PROP_FOCUS, focus)
    if not possible:
        print("Manual focus on camera not supported! Going with autofocus mode.")


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
        
        if(succes):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            
            cv2.imwrite("web/tmp/stream1.jpeg", img)
            # os.replace("web/tmp/stream1.tmp.jpeg","web/tmp/stream1.jpeg")

            img2 = img

            # GaussianBlur 
            # https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html
            img2 = cv2.GaussianBlur(img2, (5, 5), 0)
            cv2.imwrite("web/tmp/stream2.jpeg", img2)
            
            
            # AdaptiveThreshold
            # https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html
            # https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
            # _, img2 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # img = cv2.Canny(img, 50, 150)
            # _, img2 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # img2 = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            img2 = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
            cv2.imwrite("web/tmp/stream3.jpeg", img2)
            
            
            # Canny Edge Detection
            # https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
            # https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de
            # todo: return edges!!!!!
            img2 = cv2.Canny(img, 50, 150)
            img2 = cv2.bitwise_not(img2)
            cv2.imwrite("web/tmp/stream4.jpeg", img2)

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
                    if client != None:
                        client.publish("scan/code", myData)
                    LastReadTime = currentTime
        else:
            print("image not captured")

        print(focus, time_cap/time_cap_counter, time_decode/time_decoder_counter)
        # print(focus)
        # cv2.imshow('Result', img)
        # cv2.waitKey(1)


# -------------------------------------------------
# run_http_server
# -------------------------------------------------
def run_http_server():
    PORT 		= 8000
    DIRECTORY 	= "web"
    
    Handler = http.server.SimpleHTTPRequestHandler
    # creating stream folder
    if not os.path.isdir(DIRECTORY+'/tmp'):
        os.mkdir(DIRECTORY+'/tmp')
        
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)
            
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()



# -------------------------------------------------
# main()
# -------------------------------------------------


#commands usefull for mosquitto server 
# mosquitto_sub -h localhost -t skan/kod
# mosquitto_pub.exe -m "123" -t /test/rtu

# main(0, cv2.CAP_DSHOW) #If it's not working use CAP_DSHOW or CAP_V4L2
# main(0, cv2.CAP_DSHOW)

# list_ports()

# Parse CLI arguments
parser = argparse.ArgumentParser(
    description="you can use 3 arguments like --list, --http, --mqtt"
)
parser.add_argument("--list", required=False, type=bool, action=argparse.BooleanOptionalAction)
parser.add_argument("--http", required=False, type=bool, action=argparse.BooleanOptionalAction)
parser.add_argument("--mqtt", required=False, type=str)
args = parser.parse_args()
print(args)
if args.list == True:
    list_ports()
    exit()

if args.http == True:
    thread.start_new_thread(run_http_server, ())

client = None
if args.mqtt != None: 
    #connecting to mqtt protocol
    client = mqtt.Client()
    try:
        client.connect(args.mqtt, 1883, 60)
    except:
        print('cannot connect to mqtt')
        exit()

decodeMain(0, cv2.CAP_DSHOW, client)
