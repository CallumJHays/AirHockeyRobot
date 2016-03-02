#include <iostream>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/opencv.hpp"
#include <string>

using namespace cv;
using namespace std;

int cMat1 = 678;
int cMat3 = 312;
int cMat5 = 678;
int cMat6 = 240;

int dMat1 = 96;
int dMat2 = 100;
int dMat3 = 50;
int dMat4 = 50;
int dMat5 = 69;

Mat mapx;
Mat mapy;

Mat imgOriginal;

int main()
{
  VideoCapture cap(0); //capture the video from web cam

  cap.set(CAP_PROP_FRAME_WIDTH, 360);
  cap.set(CAP_PROP_FRAME_HEIGHT, 240);
  cap.set(CAP_PROP_BRIGHTNESS, 0.2);
  cap.set(CAP_PROP_GAIN, 0.3);

  if ( !cap.isOpened() )  // if not success, exit program
  {
   cout << "Cannot open the web cam" << endl;
   return -1;
  }
  cap.read(imgOriginal);

  namedWindow("Control", CV_WINDOW_AUTOSIZE); //create a window called "Control"


  //Create trackbars in "Control" window
  cvCreateTrackbar("cMat1", "Control", &cMat1, cMat1*2);
  cvCreateTrackbar("cMat3", "Control", &cMat3, cMat3*2);
  cvCreateTrackbar("cMat5", "Control", &cMat5, cMat5*10);
  cvCreateTrackbar("cMat6", "Control", &cMat6, cMat6*2);

  cvCreateTrackbar("dMat1", "Control", &dMat1, dMat1*2);
  cvCreateTrackbar("dMat2", "Control", &dMat2, dMat2*10);
  cvCreateTrackbar("dMat3", "Control", &dMat3, dMat3*2);
  cvCreateTrackbar("dMat4", "Control", &dMat4, dMat4*2);
  cvCreateTrackbar("dMat5", "Control", &dMat5, dMat5*2);
        
  Mat cMat = (Mat_<double>(3,3) << cMat1, 0, cMat3, 0, cMat5, cMat6, 0, 0, 1);
  Mat dMat = (Mat_<double>(5,1) << -dMat1 / 100, -dMat2 / 100, 0, 0, dMat5 / 10);

  while (true)
  {
  	bool bSuccess = cap.read(imgOriginal);

    if (!bSuccess) //if not success, break loop
    {
         cout << "Cannot read a frame from video stream" << endl;
         break;
    }

    cMat = (Mat_<double>(3,3) << cMat1, 0, cMat3, 0, cMat5, cMat6, 0, 0, 1);
    dMat = (Mat_<double>(5,1) << double(-dMat1) / 100.0, double(-dMat2) / 100.0, double(dMat3) / 10.0, double(dMat4) / 10.0, double(dMat5) / 10.0);

    initUndistortRectifyMap(cMat, dMat, Mat(),
      getOptimalNewCameraMatrix(cMat, dMat, imgOriginal.size(),
        1, imgOriginal.size(), 0),
      imgOriginal.size(), CV_16SC2, mapx, mapy);

    remap(imgOriginal, imgOriginal, mapx, mapy, INTER_LINEAR);

    //imgOriginal = imgOriginal(Rect(50, 50, 500, 380));
    
    imshow("Original", imgOriginal); //show the original image

    if (waitKey(30) == 27) //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
    {
      cout << "esc key is pressed by user" << endl;
      break; 
    }
  }

  return 0;

}
