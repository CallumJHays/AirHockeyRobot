/* blobtrack.cpp
Written by Callum Hays
For QUT Robotics Club
Air Hockey Robot
Note: This file is for testing purposes only.
*/

#include <iostream>
#include "opencv2/opencv.hpp"
#include "library/BlobResult.h"

// use namespaces for less characters when programming
using namespace std;
using namespace cv;

// video capture object is cap. Individual video frames are stored in frame.
VideoCapture cap(0);
Mat frame;
SimpleBlobTracker tracker;

// main loop function. return true to continue loop or false to quit.
bool loop(){
	// attempt to read frame from cap object. if failed, notify and end program.
	if(!cap.read(frame)){
		cout << "Could not read frame from cap" << endl;
		return false;
	}

	// crop frame to only show sides of table at maximum
	frame = frame(Rect(10, 50, 265, 175));

	
	// return true to restart loop
	return true;
}

// program starts here
int main(){
	// use opencv functions to open the camera and store camera interface object in cap
    if(!cap.isOpened()){
        cout << "Cannot open the camera" << endl;
        return -1;
    }

    // begin mainloop
    while(loop());

    return 0;
}