import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 180, 255, 0)
    gray2 = gray.copy()
    mask = np.zeros(gray.shape, np.uint8)

    cv2.imshow('frame', gray)

    _, contours, hierarchy = cv2.findContours(gray2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt = contours[max_index]

    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 255), 2)

    cv2.imshow('frame', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cv2.destroyAllWindows()
