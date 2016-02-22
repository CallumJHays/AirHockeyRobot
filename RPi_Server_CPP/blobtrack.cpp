#include "opencv2/highgui/highgui.hpp"
#include "opencv2/opencv.hpp"
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

void onMouse( int event, int x, int y, int, void* );
Mat frame;

int main(int argc, char* argv[])
{
    VideoCapture cap(0); // open the video camera no. 0

    if (!cap.isOpened())  // if not success, exit program
    {
        cout << "Cannot open the video cam" << endl;
        return -1;
    }

   double dWidth = cap.get(CV_CAP_PROP_FRAME_WIDTH); //get the width of frames of the video
   double dHeight = cap.get(CV_CAP_PROP_FRAME_HEIGHT); //get the height of frames of the video

    //cout << "Frame size : " << dWidth << " x " << dHeight << endl;

    namedWindow("RGB",CV_WINDOW_AUTOSIZE); //create a window called "MyVideo"
    //namedWindow("Threshold",CV_WINDOW_AUTOSIZE); //create a window called "MyVideo"
    namedWindow("Keypoints",CV_WINDOW_NORMAL); //create a window called "MyVideo"

    setMouseCallback( "RGB", onMouse, 0 );


    SimpleBlobDetector::Params params;
    params.minDistBetweenBlobs = 1.0f;
    params.filterByInertia = false;
    params.filterByConvexity = false;
    params.filterByColor = false;
    params.filterByCircularity = false;
    params.filterByArea = true;
    params.minArea = 6.0f;
    params.maxArea = 50.0f;

    cv::Ptr<cv::SimpleBlobDetector> detector = cv::SimpleBlobDetector::create(params);

    Size size(64, 48);

    while (1)
    {
        cap.read(frame); // read a new frame from video

        Mat output;

        clock_t begin = clock();
        //==========[Start Timing]==========//


        inRange(frame, cv::Scalar(0, 75, 20), cv::Scalar(90, 120, 100), output);
        Mat n;
        resize(output,n,size);

        std::vector<KeyPoint> keypoints;
        detector->detect( n, keypoints);

        //==========[End Timing]==========//
        clock_t end = clock();
        double elapsed_secs =(double(end - begin) / CLOCKS_PER_SEC)*1000;
        //cout << "FPS " << to_string(elapsed_secs) << endl;

        Mat im_with_keypoints;
        drawKeypoints( n, keypoints, im_with_keypoints, Scalar(0,0,255), DrawMatchesFlags::DRAW_RICH_KEYPOINTS );

        imshow("RGB", frame); //show the frame in "MyVideo" window
        imshow("Keypoints", im_with_keypoints);

        if (waitKey(30) == 27)
       {
            cout << "esc key is pressed by user" << endl;
            break;
       }
    }
    return 0;
}

void onMouse( int event, int x, int y, int, void* ){
    if( event != CV_EVENT_LBUTTONDOWN )
            return;
    Point pt = Point(x,y);
    //std::cout<<"x="<<pt.x<<"\t y="<<pt.y<<"\t value="<<frame.at<uchar>(x,y)<<"\n";
    Vec3b colour = frame.at<Vec3b>(Point(x, y));
    //cout << "B" << std::to_string(colour.val[0]) << " G" << std::to_string(colour.val[1]) << " R" <<std::to_string(colour.val[2]) << endl ;
}
