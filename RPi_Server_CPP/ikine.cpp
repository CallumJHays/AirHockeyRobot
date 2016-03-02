#include "servo.cpp"
#include <iostream>
#include <math.h>

using namespace std;

class Ikine {
	static const short baseX = 50;
	static const short baseY = 5;

	Servo* baseServo;
	static const double upperArmLength = 22.75;

	Servo* elbowServo;
	static const double lowerArmLength = 24.05;

public:
	double toDeg(double rad){
		return rad * 180 / M_PI;
	}
	double cosRule(double a, double b, double c){
		return acos((b*b + c*c - a*a) / (2 * b * c));
	}
	bool moveTo(double x, double y){
		cout << "Attempting to go to (" << x << ", " << y << ")" << endl;
		x -= baseX;
		y -= baseY;
		double base2malletDist = sqrt(x * x + y * y);
		if(base2malletDist > lowerArmLength + upperArmLength){
			return false;
		}
		double base2malletRad = atan2(y, x);

		double baseRad = cosRule(lowerArmLength, upperArmLength, base2malletDist);
		double elbowRad = cosRule(base2malletDist, lowerArmLength, upperArmLength);

		if(baseServo->set(toDeg(base2malletRad - baseRad)) && elbowServo->set(toDeg(elbowRad))){
			cout << "Moving to (" << x << ", " << y << ")" << endl;
		} else {
			cout << "Servos cannot move to the location: (" << x << ", " << y << ")" << endl;
		}
		return true;
	}
	Ikine(){
		baseServo = new Servo(1);
		elbowServo = new Servo(0);
		moveTo(0, 15);
	}
};

int main(){
	cout << "Ikine test begin!" << endl;
	Ikine* ikine = new Ikine();

	while(true){
		ikine->moveTo(50, 30);
		cin.ignore();
		ikine->moveTo(50, 35);
		cin.ignore();
	}

	return 0;
}