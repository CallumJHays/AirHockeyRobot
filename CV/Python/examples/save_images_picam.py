import numpy as np
import cv2
import time
import picamera
import picamera.array

# Calls pi camera module
camera = picamera.PiCamera()
camera.framerate = 90
camera.resolution = (480, 320)

# Setup raspi camera settings
stream = picamera.array.PiRGBArray(camera)

time.sleep(0.25)

# Fix camera parameters
#camera.exposure_mode = 10950
#camera.awb_mode =
#camera.awb_gains = (Fraction(397, 256), Fraction(89, 64))
#print 'camera.exposure_speed: ' + str(camera.exposure_speed)
#print 'camera.awb_gains: ' + str(camera.awb_gains)
#print 'camera.awb_gains: ' + str(camera.awb_mode)

img_no = 0

while True:
    stream.seek(0)
    stream.truncate()
    camera.capture(stream, 'bgr', use_video_port=True)
    img = stream.array

    cv2.imshow('frame', img)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('d'):
        cv2.imwrite('hockey_table_' + str(img_no) + '.jpg', img)
        img_no = img_no + 1

    elif k == ord('q'):
        break

cv2.destroyAllWindows()
