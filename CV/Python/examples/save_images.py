import numpy as np
import cv2

cap = cv2.VideoCapture(1)

img_no = 0

while True:
    _, img = cap.read()

    cv2.imshow('frame', img)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('d'):
        cv2.imwrite('hockey_table_' + str(img_no) + '.jpg', img)
        img_no = img_no + 1

    elif k == ord('q'):
        break

cv2.destroyAllWindows()
