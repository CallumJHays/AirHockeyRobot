import cv2
import numpy as np
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
print 'camera.exposure_speed: ' + str(camera.exposure_speed)
print 'camera.shutter_speed: ' + str(camera.exposure_speed)
print 'camera.awb_gains: ' + str(camera.awb_gains)
print 'camera.awb_gains: ' + str(camera.awb_mode)
#camera.shutter_speed = CAMERA_SHUTTER_SPEED
#camera.exposure_mode = CAMERA_EXPOSURE_MODE
#camera.awb_mode = False
#camera.awb_gains =

while True:
    stream.truncate(0)
    camera.capture(stream, 'bgr', use_video_port=True)
    frame = stream.array

    cv2.imshow('frame', frame)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break

cv2.destroyAllWindows()
