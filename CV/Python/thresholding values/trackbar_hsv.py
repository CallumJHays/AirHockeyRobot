import cv2
import numpy as np
import time
from fractions import Fraction

# Open camera capture device
cap = cv2.VideoCapture(0)

# Kernel for Morphological transformations
kernel = np.ones((3, 3), np.uint8)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h-low', 'result',0,179,nothing)
cv2.createTrackbar('s-low', 'result',0,255,nothing)
cv2.createTrackbar('v-low', 'result',0,255,nothing)

cv2.createTrackbar('h-high', 'result',179,179,nothing)
cv2.createTrackbar('s-high', 'result',255,255,nothing)
cv2.createTrackbar('v-high', 'result',255,255,nothing)

# Defisheye parameters
camera_matrix = np.array([[ 585.90603268, 0., 292.55539555 ], [ 0., 583.54677694, 263.94398364 ], [ 0., 0., 1., ]])
distortion_coefficients =  np.array([-1.31618512,  1.57884866,  0.00767129, -0.00976971, -0.12370269])

while(1):
    ret, frame = cap.read()

    #ROI
    frame = frame[40:200, 35:290]
    # Defisheye
    #h, w = frame.shape[:2]
    #newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (w, h), 1, (w, h))
    #dst = cv2.undistort(frame, camera_matrix, distortion_coefficients, None, newcameramtx)
    #x,y,w,h = roi
    #frame = dst[y:y+h, x:x+w]

    #converting to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h_low = cv2.getTrackbarPos('h-low','result')
    s_low = cv2.getTrackbarPos('s-low','result')
    v_low = cv2.getTrackbarPos('v-low','result')

    h_high = cv2.getTrackbarPos('h-high','result')
    s_high = cv2.getTrackbarPos('s-high','result')
    v_high = cv2.getTrackbarPos('v-high','result')

    # Normal masking algorithm
    lower_blue = np.array([h_low,s_low,v_low])
    upper_blue = np.array([h_high,s_high,v_high])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)
    img_filtered = cv2.bitwise_and(frame,frame,mask = mask)
    img_blur = cv2.GaussianBlur(img_filtered, (15,15), 0)
    _ret, img_otsu = cv2.threshold(cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #img_eroded = cv2.erode(img_otsu, kernel, iterations=1)
    #img_dilated = cv2.dilate(img_eroded, kernel, iterations=1)

    cv2.imshow('original', frame)
    cv2.imshow('result', img_otsu)

    k = cv2.waitKey(5) & 0xFF
    if k == ord('q'):
        break

cv2.destroyAllWindows()

