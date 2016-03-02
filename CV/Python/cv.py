import cv2
import numpy as np
import time
import picamera
import picamera.array
from fractions import Fraction

# Calls pi camera module
camera = picamera.PiCamera()
camera.framerate = 90
camera.resolution = (320, 240)
camera.exposure_mode = 'sports'
camera.awb_mode = 'off'
camera.awb_gains = (Fraction(191, 128), Fraction(441, 256))
camera.brightness = 75
camera.contrast = 75

time.sleep(2.25)

# Setup raspi camera settings
stream = picamera.array.PiRGBArray(camera)

# Kalman filter
kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]], np.float32)
kalman.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
kalman.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.75

pred_coord = np.zeros((2,1), np.float32) # tracked / prediction coordinates

# Kernel for Morphological transformations
kernel = np.ones((5,5), np.uint8)

# Defisheye parameters
camera_matrix = np.array([[ 219.082, 0., 233.462 ], [ 0., 218.093, 141.5 ], [ 0., 0., 1., ]])
distortion_coefficients =  np.array([-0.20511943, -0.01188414,  0.01784919,  0.01238459,  0.02984104])

# Start time (for FPS)
start = time.time()
FRAMES_NO = 0

while True:
    # Get frame from camera
    stream.truncate(0)
    camera.capture(stream, 'bgr', use_video_port=True)
    frame = stream.array

    # Defisheye
    #h, w = frame.shape[:2]
    #newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (w, h), 1, (w, h))
    #dst = cv2.undistort(frame, camera_matrix, distortion_coefficients, None, newcameramtx)
    #x,y,w,h = roi
    #frame = dst[y:y+h, x:x+w]

    # Resize and crop ROI
    #frame = frame[60:205, 11:265]

    # Converts to other formats
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # define range of blue color in BGR
    # B:85-125	    G:120-160   R:80-120
    #lower = np.array([90,115,85])
    #upper = np.array([120,155,115])

    # HSV
    # Increase V value if can't detect red puck
    # H: 125-179      S:85-255    V:0-255
    lower = np.array([125, 53, 75])
    upper = np.array([179, 255, 255])

    # Threshold the RGB/HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND frame to turn it into a binary image
    img_filtered = cv2.bitwise_and(frame, frame, mask= mask)

    # Gaussian blur image (to smoothen out things)
    img_blur = cv2.GaussianBlur(img_filtered, (5,5), 0)

    # otsu thresholding
    _ret, img_otsu = cv2.threshold(cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    ## Morphological transformation
    # Erosion (to further remove dots on in the background)
    #img_eroded = cv2.erode(img_otsu, kernel, iterations=1)

    # Dialation (to make white more prominent)
    #img_dilated = cv2.dilate(img_eroded, kernel, iterations=1)

    # Contour finding (a.k.a location of puck)
    try:
        _, contours, hierarchy = cv2.findContours(img_otsu.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Get index of largest contour
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt = contours[max_index]

        # Metadata of contour
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.circle(frame, (x+w/2, y+h/2), w/2, (0, 0, 255), 2)

        # Kalman predictions
        mp = np.array([[np.float32(x)],[np.float32(y)]])
        kalman.correct(mp)
        pred_coord = kalman.predict()

        pred_x = int(pred_coord[0])
        pred_y = int(pred_coord[1])
        cv2.circle(frame, (pred_x+w/2, pred_y+h/2), w/2, (255, 0, 0), 1)

    except:
        pass


    # Display image
    cv2.imshow('frame', frame)
    cv2.imshow('threshold otsu', img_otsu)
    #cv2.imshow('debug', img_filtered)

    # Get current frames no
    #print(FRAMES_NO)
    FRAMES_NO = FRAMES_NO + 1
    if FRAMES_NO >= 120:
        # fps
        end = time.time()
        seconds = end - start
        fps = FRAMES_NO / seconds
        print('FPS: ', fps)
        FRAMES_NO = 0
        start = time.time()
        #break

    # Key press
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cv2.destroyAllWindows()
