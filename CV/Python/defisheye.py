import numpy as np
import cv2

cap = cv2.VideoCapture(1)

#RMS: 0.14118575295
camera_matrix = np.array([[ 585.90603268, 0., 292.55539555 ], [ 0., 583.54677694, 263.94398364 ], [ 0., 0., 1., ]])
distortion_coefficients =  np.array([-1.31618512,  1.57884866,  0.00767129, -0.00976971, -0.12370269])

while True:
    _, img = cap.read()

    h, w = img.shape[:2]

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (w, h), 1, (w, h))

    dst = cv2.undistort(img, camera_matrix, distortion_coefficients, None, newcameramtx)

    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]

    cv2.imshow('undistorted', dst)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break

cv2.destroyAllWindows()

