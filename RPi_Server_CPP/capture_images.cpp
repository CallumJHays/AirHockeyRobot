#include "opencv2/highgui/highgui.hpp"
#include "opencv2/opencv.hpp"
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

void onMouse( int event, int x, int y, int, void* );
Mat frameBGR;
Mat frame;

Mat cMat = (Mat_<double>(3,3) << 6.7755787141193980e+02, 0, 3.1950000000000000e+02, 0,
    6.7755787141193980e+02, 2.3950000000000000e+02, 0, 0, 1);
Mat dMat = (Mat_<double>(5,1) << -9.6077790106132444e-01, -1.1475291579624882e+00, 0, 0,
    6.8919587593787934e+00);
    
Mat mapx;
Mat mapy;

vector<Mat> channels;

int cvChromaticityTest();

int main(){
	return cvChromaticityTest();
}

int cvChromaticityTest(){
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
    //namedWindow("Threshold",CV_WINDOW_AUTOSIZE); //create a window called "MyVideo"
    namedWindow("Keypoints",CV_WINDOW_NORMAL); //create a window called "Keypoints"

    setMouseCallback( "HSV", onMouse, 0 );

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
    params.maxArea = 10.0f;

    cv::Ptr<cv::SimpleBlobDetector> detector = cv::SimpleBlobDetector::create(params);

    Size size(128, 96);
    
    Mat gt = Mat::zeros(128, 96, CV_8U);
    Mat rt = gt.clone();


    while (1)
    {
        cap.read(frameBGR); // read a new frame from video
        remap(frameBGR, frameBGR, mapx, mapy, INTER_LINEAR);
	


        //clock_t begin = clock();
        //==========[Start Timing]==========//
	
	
        Mat n;
        resize(frameBGR,n,size);

	split(n, channels);
	
	Mat B = channels[0];
	Mat G = channels[1];
	Mat R = channels[2];
	B.convertTo(B, CV_32F);
	G.convertTo(G, CV_32F);
	R.convertTo(R, CV_32F);
	
	Mat sum = B;
	add(B, G, sum);
	add(R, sum, sum);
	
	Mat g = G.clone();
	Mat r = R.clone();
	g = G / sum;
	r = R / sum;
	
	imshow("g", g);
	imshow("r", r);
	
	threshold(g, gt, 0.4, 1, THRESH_BINARY);
	threshold(r, rt, 0.28, 1, THRESH_BINARY_INV);
	multiply(rt, gt, n, 255);	
	n.convertTo(n, CV_8U);

        std::vector<KeyPoint> keypoints;
        detector->detect( n, keypoints);

        //==========[End Timing]==========//
        //clock_t end = clock();
        //double elapsed_secs =(double(end - begin) / CLOCKS_PER_SEC)*1000;
        // cout << "FPS " << to_string(elapsed_secs) << endl;

        Mat im_with_keypoints;
        drawKeypoints( n, keypoints, im_with_keypoints, Scalar(0,0,255), DrawMatchesFlags::DRAW_RICH_KEYPOINTS );

        imshow("HSV", frameBGR); //show the frame in "MyVideo" window
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
    //Point pt = Point(x,y);
    //std::cout<<"x="<<pt.x<<"\t y="<<pt.y<<"\t value="<<frame.at<uchar>(x,y)<<"\n";
    Vec3b colour = frame.at<Vec3b>(Point(x, y));
    cout << "B" << std::to_string(colour.val[0]) << " G" << std::to_string(colour.val[1]) << " R" <<std::to_string(colour.val[2]) << endl ;
}

