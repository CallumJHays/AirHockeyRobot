#include "servo.cpp"
#include <iostream>

using namespace std;

class Ikine {
	double basePos = [50, 0];

	Servo* baseServo;
	const double upperArmLength = 23.0;

	Servo* elbowServo;
	const double lowerArmLength = 23.0;

public:
	Ikine(){

	}
	double getDifference(double pos1, double pos2){
		return [pos2[0] - pos1[0], pos2[1] - pos1[1]];
	}
	double getDifference(double pos1, double pos2){
		double diff = getDifference(pos1, pos2);
		return math.sqrt(diff[0]^2, diff[1]^2);
	}
	double calculateInverseKinematics(){

	}
	double getBaseAngle(targetPos){
		double triangleAngle = calculateInverseKinematics(targetPos)[1];
		double a = 
	}
}