from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

frame = picam2.capture_array()
cv2.imshow("Frame", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()