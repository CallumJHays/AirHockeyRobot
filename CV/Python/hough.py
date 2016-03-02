import cv2
import numpy as np

cap = cv2.VideoCapture(0)

FRAME_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


while True:
    ret, frame = cap.read()
    frame = cv2.medianBlur(frame, 5)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, FRAME_HEIGHT/4, param1=200, param2=100)

    """
    circles = np.uint16(np.around(circles))
    
    for i in circles[0, :]:
        # outer circle
        cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)

        # Center of circle
        cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
    """

    cv2.imshow('frame', frame)
    
    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break

cap.destroyAllWindows()
