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

    // Set custom camera properties for efficiency and effectiveness
    cap.set(CAP_PROP_FRAME_WIDTH, 360);
    cap.set(CAP_PROP_FRAME_HEIGHT, 240);
    cap.set(CAP_PROP_BRIGHTNESS, 0.2);
    cap.set(CAP_PROP_GAIN, 0.3);

    // initiate servos
    Servo* elbowServo = new Servo(1);

    // TODO: INSERT KALMAN FILTER STUFF HERE
    // Instantiate variables used by the main loop
    Mat frame, frame_hsv;
    vector< vector<Point> > contours;
    vector<Vec4i> hierarchy;
    vector<Point2f> puck(1);

    int largestIndex;
    double largest;

    Mat cMat = (Mat_<double>(3,3) << 575.0, 0, 300.0, 0, 5000, 270, 0, 0, 1);
    Mat dMat = (Mat_<double>(5,1) << -0.75, -2.75, 0, 0, 8.0);
    Mat mapx;
    Mat mapy;

    cap.read(frame);
    frame = frame(Rect(10, 50, 265, 175));

    initUndistortRectifyMap(cMat, dMat, Mat(),
        getOptimalNewCameraMatrix(cMat, dMat, frame.size(), 1, frame.size(), 0),
        frame.size(), CV_16SC2, mapx, mapy);

    // Endless loop:
    while(true){
        Mat frame_otsu, mask, frame_filtered, frame_blurred, frame_gray;

        // Get camera frame, crop it and convert to HSV
        cap.read(frame);
        frame = frame(Rect(10, 50, 265, 175));
        remap(frame, frame, mapx, mapy, INTER_LINEAR);
        // cvtColor(frame, frame_hsv, COLOR_BGR2HSV);

        // Threshold the HSV values to find the green puck
        inRange(frame, 
            Scalar(72,85,166), 
            Scalar(154,126,191), mask);

        // Bitwise-AND frame to turn it into a binary image
        bitwise_and(frame, frame, frame_filtered, mask);

        // Gaussian blur image (to smoothen out things) then convert to gray
        GaussianBlur(frame_filtered, frame_blurred, Size(5.0, 5.0), 0);
        cvtColor(frame_blurred, frame_gray, COLOR_BGR2GRAY);

        // otsu thresholding
        threshold(frame_gray, frame_otsu, 0, 255, THRESH_BINARY + THRESH_OTSU);

        // Use contour recognition to find the location of the puck
        // store contour info in contours and hierarchy
        findContours(frame_otsu, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);

        // Store the areas of all contours in the areas array
        if(contours.size() > 0){
            double areas[contours.size()];
            for(int i = 0; i < contours.size(); i++){
                areas[i] = contourArea(contours[i]);
            }
            // find the largest area of all the contours
            int largestIndex = 0;
            double largest = 0.0;
            for(int i = 0; i < contours.size(); i++){
                if(largest < areas[i])
                    largestIndex = i;
            }
            // save the largest contour in cnt
            vector<Point> cnt = contours[largestIndex];
            // ^ OKAY GUYS I'll admit that was SOO much more easily done in python

            // report location of largest contour 
            Rect puckRect = boundingRect(cnt);
            circle(frame, Point(puckRect.x + puckRect.width/2, puckRect.y + puckRect.height/2), puckRect.width/2, Scalar(0, 0, 255), 2);

            puck[0].x = puckRect.x + puckRect.width / 2;
            puck[0].y = puckRect.y + puckRect.height / 2;

            cout << "Puck located! x = " << puck[0].x << ", y = " << puck[0].y << endl;

            // Run puck through fisheye calibration
            undistortPoints(puck, puck, cMat, dMat);

            // make servo actions based on puck location
            if(puck[0].x >= 100){
                elbowServo->set(0);
            } else {
                elbowServo->set(90);
            }
            // TODO: perform matrix transformation on puck x and puck y to get cartesian values
        } else {
            cout << "Problem locating puck!" << endl;
            elbowServo->set(90);
        }

        // TODO: Kalman predictions go here

        // Display image for debugging
        imshow("Frame", frame);
        imshow("otsu Threshold", frame_otsu);

        // Check for program halt
        if(waitKey(30) == 27){
            cout << "esc key is pressed by the user" << endl;
            break;
        }
    }
    destroyAllWindows();
    return 0;
}
