import cv2
from pyzbar.pyzbar import decode
import time

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



print('start')
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640*1.5)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480*1.5)
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

LastReadTime = 0
cooldown = 1

focusMin = 100
focusMax = 200
step = 10
focus = focusMin
direction = step
while True:
    cap.set(cv2.CAP_PROP_FOCUS, focus)
    focus += direction
    print(focus)

    if direction > 0 and focus >= focusMax:
        direction = -step

    if direction < 0 and focus <= focusMin:
        direction = step

    succes, img = cap.read()
    for barcode in decode(img):
        currentTime = time.time()
        if currentTime - LastReadTime > cooldown:
            print(barcode.data)
            myData = barcode.data.decode('utf-8')
            print(myData)
            LastReadTime = currentTime
            


    # cv2.imshow('Result', img)
    # cv2.waitKey(1)
    

