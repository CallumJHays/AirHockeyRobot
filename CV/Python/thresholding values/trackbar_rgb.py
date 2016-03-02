import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import numpy as np


cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
r,g,b = 100,100,100

# Creating track bar
cv2.createTrackbar('r-low', 'result',0,255,nothing)
cv2.createTrackbar('g-low', 'result',0,255,nothing)
cv2.createTrackbar('b-low', 'result',0,255,nothing)

cv2.createTrackbar('r-high', 'result',0,255,nothing)
cv2.createTrackbar('g-high', 'result',0,255,nothing)
cv2.createTrackbar('b-high', 'result',0,255,nothing)

while(1):

    _, frame = cap.read()

    #converting to HSV
    #hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    r_low = cv2.getTrackbarPos('r-low','result')
    g_low = cv2.getTrackbarPos('g-low','result')
    b_low = cv2.getTrackbarPos('b-low','result')

    r_high = cv2.getTrackbarPos('r-high','result')
    g_high = cv2.getTrackbarPos('g-high','result')
    b_high = cv2.getTrackbarPos('b-high','result')


    # Normal masking algorithm
    lower_blue = np.array([r_low,g_low,b_low])
    upper_blue = np.array([r_high,g_high,b_high])

    mask = cv2.inRange(frame,lower_blue, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)

    cv2.imshow('result',result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()

