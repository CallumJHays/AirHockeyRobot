#include <stdio.h>
#include <opencv2/opencv.hpp>
#include "opencvblobslib/library/blob.h"
#include "opencvblobslib/library/BlobResult.h"

#define NUMCORES 4
#define RGB_LOW Scalar(0, 0, 175)
#define RGB_HIGH Scalar(165, 80, 256)

using namespace std;
using namespace cv;

int main(){
	VideoCapture cap(0);

	Mat frame, threshold;

	while(true){
		double start = (double) getTickCount();
		cap.read(frame);

		inRange(frame, RGB_LOW, RGB_HIGH, threshold);
		
		CBlobResult blobs(threshold, Mat(), NUMCORES);

		if(blobs.GetNumBlobs() > 0){
			rectangle(frame, blobs.GetBlob(0)->GetBoundingBox(), Scalar(0,220,0), 3);
		}

		cout << 1 / (((double) getTickCount() - start) / getTickFrequency()) << " FPS" << endl;

		imshow("Blob Tracking", frame);

		waitKey(1);
	}

	return 0;
}