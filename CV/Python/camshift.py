import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Take first frame of the video
ret, frame = cap.read()

# setup initial location of window

FRAME_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

x,w,y,h = int(FRAME_WIDTH/2)-30,60,int(FRAME_HEIGHT/2)-30,60
track_window = (x,y,w,h)

# Termination criteria
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

lower = np.array([40, 42, 75])
upper = np.array([90, 90, 180])

while True:
    ret, frame = cap.read()

    # Setup ROI
    roi = frame[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, lower, upper)
    mask_full = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), lower, upper)
    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0,180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('img', frame)
    cv2.imshow('hsv', mask_full)
    cv2.imshow('mask', mask)
    cv2.imshow('roi', roi)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break

while True:
    ret, frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # Apply meanshift to get the new location
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # Draw it on image
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame, [pts], True, 255, 2)
        cv2.imshow('img', img2)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('q'):
            break

cv2.destroyAllWindows()
cap.release()
