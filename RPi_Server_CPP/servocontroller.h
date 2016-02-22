// servocontroller.h
#ifndef servocontroller_h
#define servocontroller_h
#include <stdio.h>

class Servo {
	int signalPin;
	static const double maxDegrees = 60.0;
	FILE * servoBlaster;
public:
	Servo(int pin);
	Servo (int pin, double initialDegrees);
	int setServo(double degrees);
	int close();
};

#endif