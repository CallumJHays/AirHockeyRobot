#include <iostream>
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

    // TODO: INSERT KALMAN FILTER STUFF HERE

    // Instantiate variables used by the main loop
    Mat frame, frame_hsv, mask, frame_filtered, frame_blurred, frame_gray, frame_otsu;
    Mat[] contours;
    Mat[][] hierarchy;
    // Endless loop:
    while(true){
        // Get camera frame and convert to HSV
        cap.read(frame);
        cvtColor(frame, frame_hsv, COLOR_BGR2HSV);

        // Threshold the HSV values to find the green puck
        inRange(frame_hsv, 
            Scalar(40, 42, 75), 
            Scalar(90, 90, 180), mask);

        // Bitwise-AND frame to turn it into a binary image
        bitwise_and(frame, frame, frame_filtered, mask);

        // Gaussian blur image (to smoothen out things) then convert to gray
        GaussianBlur(frame_filtered, frame_blurred, Size(5.0, 5.0), 0);
        cvtColor(frame_blurred, frame_gray, COLOR_BGR2GRAY);

        // otsu thresholding
        threshold(frame_gray, frame_otsu, 0, 255, THRESH_BINARY + THRESH_OTSU);

        // Use contour recognition to find the location of the puck
        try {
            // store contour info in contours and hierarchy
            findContours(frame_otsu.copy(), contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE)

            // Store the areas of all contours in the areas array
            double[] areas = double[size(contours)];
            for(int i = 0; i < size(contours); i++){
                areas[i] = contourArea(contours);
            }
            // find the largest area of all the contours
            int largestIndex = 0;
            double largest = 0.0;
            for(int i = 0; i < size(areas); i++){
                if(largest < areas[i])
                    largestIndex = i;
            }
            // save the largest contour in cnt
            Mat cnt = contours[largestIndex];
            // ^ OKAY GUYS I'll admit that was SOO much more easily done in python

            // Metadata of contour
            Rect puck = boundingRect(cnt);
            circle(frame, (puck.x + puck.width/2, puck.y + puck.height/2), puck.width/2, Scalar(0, 0, 255), 2)
            cout << "Puck located! x = " << puck.x << ", y = " << puck.y << endl;
        } catch(int e) {
            cout << "Problem locating puck!" << endl;
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