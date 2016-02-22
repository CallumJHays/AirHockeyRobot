import cv2
import numpy as np


cap = cv2.VideoCapture(0)

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

cv2.createTrackbar('h-high', 'result',0,197,nothing)
cv2.createTrackbar('s-high', 'result',0,197,nothing)
cv2.createTrackbar('v-high', 'result',0,197,nothing)

while(1):

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

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

    result = cv2.bitwise_and(frame,frame,mask = mask)

    cv2.imshow('result',result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()

