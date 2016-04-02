#include "opencv2/highgui/highgui.hpp"
#include "opencv2/opencv.hpp"
#include "servo.cpp"
#include <iostream>
#include <string>
#include <unistd.h>

using namespace cv;
using namespace std;

Servo* baseServo;
Servo* elbowServo;

Mat frameBGR;
Mat frame;

Mat cMat = (Mat_<double>(3,3) << 3.0536803560374517e+02, 0, 3.1950000000000000e+02, 0,
    3.0536803560374517e+02, 2.3950000000000000e+02, 0, 0, 1);
Mat dMat = (Mat_<double>(5,1) << -3.1139559031807340e-01, 8.7512793949182197e-02, 0, 0,
    -4.7615273003388395e-03);
    
Mat mapx;
Mat mapy;

int cnt=0;

int cvHSVTest();
int main(){
	baseServo = new Servo(0);
	elbowServo = new Servo(1);
	return cvHSVTest();
}

int cvHSVTest(){
    VideoCapture cap(0); // open the video camera no. 0

    if (!cap.isOpened())  // if not success, exit program
    {
        cout << "Cannot open the video cam" << endl;
        return -1;
    }
   cap.read(frameBGR); // read a new frame from video

   double dWidth = cap.get(CV_CAP_PROP_FRAME_WIDTH); //get the width of frames of the video
   double dHeight = cap.get(CV_CAP_PROP_FRAME_HEIGHT); //get the height of frames of the video

    cout << "Frame size : " << dWidth << " x " << dHeight << endl;

    namedWindow("HSV",CV_WINDOW_AUTOSIZE); //create a window called "RGB"
    namedWindow("Threshold",CV_WINDOW_AUTOSIZE); //create a window called "RGB"
    //namedWindow("Threshold",CV_WINDOW_AUTOSIZE); //create a window called "MyVideo"
    namedWindow("Keypoints",CV_WINDOW_NORMAL); //create a window called "Keypoints"

    initUndistortRectifyMap(cMat, dMat, Mat(),
			getOptimalNewCameraMatrix(cMat, dMat,frameBGR.size(), 1, frameBGR.size(), 0),
			frameBGR.size(), CV_16SC2, mapx, mapy);

    SimpleBlobDetector::Params params;
    params.minDistBetweenBlobs = 1.0f;
    params.filterByInertia = false;
    params.filterByConvexity = false;
    params.filterByColor = false;
    params.filterByCircularity = false;
    params.filterByArea = true;
    params.minArea = 2.0f;
    params.maxArea = 100.0f;

    cv::Ptr<cv::SimpleBlobDetector> detector = cv::SimpleBlobDetector::create(params);

    Size size(128, 96);

    while (1)
    {
        cap.read(frameBGR); // read a new frame from video
        remap(frameBGR, frameBGR, mapx, mapy, INTER_LINEAR);
	cvtColor(frameBGR, frame, COLOR_BGR2HSV);
	
        Mat output;

        //clock_t begin = clock();
        //==========[Start Timing]==========//
	

        inRange(frame, cv::Scalar(35, 70, 50), cv::Scalar(100, 215, 255), output);
        Mat n;
        imshow("Threshold", output);
        resize(output,n,size);

        std::vector<KeyPoint> keypoints;
        detector->detect( n, keypoints);

		if(keypoints.size()>0 && cnt>1000){
			cout << "Detected!" << endl;
			baseServo->set(0);
			elbowServo->set(0);
			usleep(800000);
			baseServo->set(120);
			elbowServo->set(120);
			usleep(800000);
			baseServo->set(0);
			elbowServo->set(0);

			cnt=0;
		}

        //==========[End Timing]==========//
        //clock_t end = clock();
        //double elapsed_secs =(double(end - begin) / CLOCKS_PER_SEC)*1000;
        // cout << "FPS " << to_string(elapsed_secs) << endl;

        Mat im_with_keypoints;
        drawKeypoints( n, keypoints, im_with_keypoints, Scalar(0,0,255), DrawMatchesFlags::DRAW_RICH_KEYPOINTS );

        imshow("HSV", frameBGR); //show the frame in "MyVideo" window
        imshow("Keypoints", im_with_keypoints);

		cnt++;

        if (waitKey(30) == 27)
       {
            cout << "esc key is pressed by user" << endl;
            break; 
       }
    }
    return 0;
}
