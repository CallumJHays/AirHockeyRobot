#ifndef servocontroller_h
#define servocontroller_h
#include <stdio.h>
#include <iostream>

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

int Servo::setServo(double degrees){
	fprintf(servoBlaster, "%d=%d%%\n", signalPin, degrees / maxDegrees);
	fflush(servoBlaster);
	return 1;
}

Servo::Servo(int pin){
	signalPin = pin;
	servoBlaster = fopen("/dev/servoblaster", "w");
}

Servo::Servo(int pin, double initDegrees){
	signalPin = pin;
	servoBlaster = fopen("/dev/servoblaster", "w");
	setServo(initDegrees);
}

int Servo::close(){
	fclose(servoBlaster);
	return 1;
}

int main(){
	Servo* base = new Servo(0);
	base->setServo(0.0);
	std::cin.ignore();
	base->setServo(50.0);
}