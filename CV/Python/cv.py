import cv2
import numpy as np

# Open camera capture device
cap = cv2.VideoCapture(0)

# Set camera parameters
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.2)
cap.set(cv2.CAP_PROP_GAIN, 0.3)

"""
#print('Frame width: ' + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
#print('Frame height: '+ str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#print('Capture mode: '+ str(cap.get(cv2.CAP_PROP_MODE)))
#print('Capture brightness: '+ str(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
#print('Capture gain: '+ str(cap.get(cv2.CAP_PROP_GAIN)))
"""

# Kalman filter
kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]], np.float32)
kalman.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
kalman.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.75

pred_coord = np.zeros((2,1), np.float32) # tracked / prediction coordinates

while True:
    # Get frame from camera
    ret, frame = cap.read()

    # Converts to other formats
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # define range of blue color in BGR
    # B:85-125	 G:120-160   R:80-120
    #lower = np.array([90,115,85])
    #upper = np.array([120,155,115])

    # HSV
    # Increase V value if can't detect green puck
    # H: 50-90  S:42-90 V:75-180
    lower = np.array([40, 42, 75])
    upper = np.array([90, 90, 180])

    # Threshold the RGB/HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND frame to turn it into a binary image
    img_filtered = cv2.bitwise_and(frame, frame, mask= mask)

    # Gaussian blur image (to smoothen out things)
    img_blur = cv2.GaussianBlur(img_filtered, (5,5), 0)

    # otsu thresholding
    _ret, img_otsu = cv2.threshold(cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Contour finding (a.k.a location of puck)
    try:
        _, contours, hierarchy = cv2.findContours(img_otsu.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Get index of largest contour
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt = contours[max_index]

        # Metadata of contour
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.circle(frame, (x+w/2, y+h/2), w/2, (0, 0, 255), 2)

    except:
        pass

    # Kalman predictions
    mp = np.array([[np.float32(x)],[np.float32(y)]])
    kalman.correct(mp)
    pred_coord = kalman.predict()

    pred_x = int(pred_coord[0])
    pred_y = int(pred_coord[1])
    cv2.circle(frame, (pred_x, pred_y), w/2, (255, 0, 0), 2)

    # Display image
    cv2.imshow('frame', frame)
    cv2.imshow('threshold otsu', img_otsu)
    #cv2.imshow('debug', img_filtered)

    # Key press
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cv2.destroyAllWindows()
