#include "point.h"
#include <tuple>
#include <cmath>

class Point
{
public:
	int x;
	int y;

	//Essentially creates a tuple (two int return) for getDifference function	
	typedef std::pair<int, int> posDifference;

	//Access using getDifference(...).first/second;
	posDifference getDifference(Point p){
		return posDifference(x-p.x, y-p.y);
	}

	double getDistance(Point p){
		sqrt(pow(getDifference(p).first, 2) + pow(getDifference(p).second, 2));
	}

};