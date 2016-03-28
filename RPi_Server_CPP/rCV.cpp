#include <iostream>
#include "servo.cpp"
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

// Use namespaces to make code easier to read.
using namespace cv;
using namespace std;

int main(){

    // Open the camera object
    VideoCapture cap(0);
    if(!cap.isOpened()){
        cout << "Cannot open the camera" << endl;
        return -1;
    }

    // Camera parameters
    cap.set(CV_CAP_PROP_FRAME_WIDTH, 320);
    cap.set(CV_CAP_PROP_FRAME_HEIGHT, 240);

    // TODO: INSERT KALMAN FILTER STUFF HERE
    // Instantiate variables used by the main loop
    Mat frame, hsv;
    Moments puck;
    double momentArea, dM01, dM10;

    //Mat cMat = (Mat_<double>(3,3) << 575.0, 0, 300.0, 0, 5000, 270, 0, 0, 1);
    //Mat dMat = (Mat_<double>(5,1) << -0.75, -2.75, 0, 0, 8.0);

    // Endless loop:
    while(true){
        // Get camera frame, crop it and convert to HSV
        cap.read(frame);
        frame = frame(Rect(10, 40, 630, 400));
        cvtColor(frame, hsv, CV_BGR2HSV);

        // Threshold the RGB values to find the green puck
        /*inRange(frame, 
            Scalar(70,60,155), 
            Scalar(175,145,255), frame);

        erode(frame, frame, getStructuringElement(MORPH_ELLIPSE, Size(3, 2)) );
        //dilate(frame, frame, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) ); 
        */
        imshow("Threshold", hsv);

        /*
        puck = moments(frame);

        if(puck.m00 > 200){ // if the puck is big enough and not noise
            cout << "Puck detected at (" << puck.m10 / puck.m00 << ", " << puck.m01 / puck.m00 << endl;
        }

        cout << frame.rows << " " << frame.cols << endl;*/

        // Check for program halt
        if(waitKey(30) == 27){
            cout << "esc key is pressed by the user" << endl;
            break;
        }
    }
    destroyAllWindows();
    return 0;
}
