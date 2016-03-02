import numpy as np
import cv2

cap = cv2.VideoCapture(1)

#RMS: 0.14118575295

def nothing(i):
    pass

cv2.namedWindow('undistorted')

cv2.createTrackbar('tl', 'undistorted', 585, 3000, nothing)
cv2.createTrackbar('tr', 'undistorted', 292, 3000, nothing)
cv2.createTrackbar('mm', 'undistorted', 583, 3000, nothing)
cv2.createTrackbar('mr', 'undistorted', 263, 3000, nothing)

while True:
    _, img = cap.read()

    tl = cv2.getTrackbarPos('tl', 'undistorted') 
    tr = cv2.getTrackbarPos('tr', 'undistorted') 
    mm = cv2.getTrackbarPos('mm', 'undistorted') 
    mr = cv2.getTrackbarPos('mr', 'undistorted') 

    camera_matrix = np.array([[ float(tl), 0., float(tr) ], [ 0., float(mm), float(mr)], [ 0., 0., 1., ]])
    distortion_coefficients =  np.array([-1.31618512,  1.57884866,  0.00767129, -0.00976971, -0.12370269])
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (w, h), 1, (w, h))

    dst = cv2.undistort(img, camera_matrix, distortion_coefficients, None, newcameramtx)

    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]

    try:
        cv2.imshow('undistorted', dst)
        cv2.imshow('org', img)
    except:
        pass

    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break

cv2.destroyAllWindows()

