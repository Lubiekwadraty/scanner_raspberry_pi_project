#!/usr/bin/python3
import cv2
from pyzbar.pyzbar import decode
import time
import paho.mqtt.client as mqtt
from picamera2 import Picamera2
from picamera2.controls import Controls

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

# list_ports()


# Project using Raspberry pi camera, this project doesn't have manually set focus
def main():
    print('start')
    #connecting to mqtt protocol
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    # https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH,640*1.5)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480*1.5)
    # cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    cap = Picamera2()
    cap.preview_configuration.main.size = (640, 480)
    cap.preview_configuration.main.format = "RGB888"
    cap.configure("preview")
    cap.start()
    LastReadTime = 0
    cooldown = 1
    while True:
        img = cap.capture_array()
        # print('decoding')
        for barcode in decode(img):
            currentTime = time.time()
            if currentTime - LastReadTime > cooldown:
                print(barcode.data)
                myData = barcode.data.decode('utf-8')
                print(myData)
                client.publish("scan/code", myData)
                LastReadTime = currentTime
            


        # cv2.imshow('Result', img)
        # cv2.waitKey(1)
    
main()

#commands usefull for mosquitto server 
# mosquitto_sub -h localhost -t scan/code
# mosquitto_pub.exe -m "123" -t /test/rtu
