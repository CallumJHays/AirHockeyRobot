#include <stdio.h>
#include <iostream>

class Servo{
	static const int ELBOW_PIN = 0;
	static const int BASE_PIN = 1;
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
			minDeg = 35;
			maxDeg = 145;
			minPulse = 900;
			maxPulse = 2300;
		}
		else if(servoPin == BASE_PIN){
			invert = true;
			minDeg = -5;
			maxDeg = 105;
			minPulse = 900;
			maxPulse = 2300;
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
	bool set(double deg){
		std::cout << servoPin << ": " << deg << std::endl;
		if(deg < minDeg || deg > maxDeg)
			return false;
		double pulsePerDeg = (maxPulse - minPulse) / (maxDeg - minDeg);
		if(invert){
			pulse(maxPulse - (deg * pulsePerDeg));
		} else {
			pulse(minPulse + (deg * pulsePerDeg));
		}
		return true;
	}
	void off(){
		set(0);
	}
	~Servo(){
		off();
		fclose(servoDev);
	}
};
