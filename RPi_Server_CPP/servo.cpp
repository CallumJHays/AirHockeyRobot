#include <stdio.h>
#include <iostream>

class Servo{
	static const int ELBOW_PIN = 2;
	static const int BASE_PIN = 0;
	FILE * servoDev;
	bool invert;
	int servoPin, minDeg, maxDeg, minPulse, maxPulse;
	void pulse(int pulse){
		fprintf(servoDev, "%d=%d\n", servoPin, (int)(pulse/10));
		fflush(servoDev);
	}
public:
	void init(){
		servoDev = fopen("/dev/servoblaster", "w");
		if(servoPin == ELBOW_PIN){
			invert = false;
			minDeg = 47;
			maxDeg = 137;
			minPulse = 800;
			maxPulse = 1800;
		}
		else if(servoPin == BASE_PIN){
			invert = true;
			minDeg = 0;
			maxDeg = 90;
			minPulse = 930;
			maxPulse = 2200;
		}

		pulse((maxPulse + minPulse) / 2);
	}
	Servo(){
		servoPin = 0;
		init();
	}
	Servo(int pin){
		servoPin = pin;
		init();
	}
	void set(double deg){
		double pulsePerDeg = (maxPulse - minPulse) / (maxDeg - minDeg);
		if(invert){
			pulse(maxPulse - (deg * pulsePerDeg));
		} else {
			pulse(minPulse + (deg * pulsePerDeg));
		}
	}
	void off(){
		set(0);
	}
	~Servo(){
		off();
		fclose(servoDev);
	}
};
