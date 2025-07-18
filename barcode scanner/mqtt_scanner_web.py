#!/usr/bin/python3
import cv2
from pyzbar.pyzbar import decode
import time
import paho.mqtt.client as mqtt
from matplotlib import pyplot as plt

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
    
    i = 0
    frames = []
    compared = 0
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
            img = cv2.GaussianBlur(img, (5, 5), 0)
            _, simillarity = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # img = cv2.Canny(img, 50, 150)
            if(i > 2):
                frames.append(simillarity)
                frames.pop(0)
                hist1 = cv2.calcHist(frames[0], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist(frames[1], [0], None, [256], [0, 256])
                compared = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)

                imghist = cv2.imread('steam/hist.jpg', cv2.IMREAD_GRAYSCALE)
                assert imghist is not None, "file could not be read, check with os.path.exists()"
                plt.hist(imghist.ravel(),256,[0,256]); 
                plt.show()
                # if(compared != 0):
                #     print("difference", compared) 
            else:
                frames.append(img)
            i += 1
            cv2.imwrite("stream/image.jpeg", img)
            cv2.imwrite("stream/image2.jpeg", simillarity)
            t = time.time()
            barcodes = decode(img)
            time_decode += time.time() - t
            time_decoder_counter += 1
            for barcode in barcodes:
                currentTime = time.time()
                if currentTime - LastReadTime > cooldown:
                    print(barcode.data, compared)
                    myData = barcode.data.decode('utf-8')
                    print(myData)
                    client.publish("scan/code", myData)
                    LastReadTime = currentTime
        else:
            print("image not captured")

        # print(focus, time_cap/time_cap_counter, time_decode/time_decoder_counter)
        # print(focus)
        # cv2.imshow('Result', img)
        # cv2.waitKey(1)

    



main(0, cv2.CAP_DSHOW)

# list_ports()

# main(0, cv2.CAP_DSHOW) #If it's not working use CAP_DSHOW or CAP_V4L2

#commands usefull for mosquitto server 
# mosquitto_sub -h localhost -t skan/kod
# mosquitto_pub.exe -m "123" -t /test/rtu