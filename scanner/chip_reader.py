# import RPi.GPIO as GPIO #if you are using raspberry pi uncomment this
# import MFRC522 #and this
import signal
import time
import _thread as thread
import queue
# Create an object of the class MFRC522



def chip_reader(result_queue):
    reader = MFRC522.MFRC522()
    status =  None
    while True:
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
        (status, uid) = reader.MFRC522_Anticoll()
        code = ''.join(str(e) for e in uid)
        if code != '':
            result_queue.put(code)
            time.sleep(1)


 