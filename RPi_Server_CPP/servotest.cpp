#include "servo.cpp"
#include <iostream>
using namespace std;

Servo* baseServo;
Servo* elbowServo;

int main(){
	baseServo = new Servo(0);
	elbowServo = new Servo(1);
	while(true){
		baseServo->set(0);
		elbowServo->set(90);
		cin.ignore();
		baseServo->set(90);
		elbowServo->set(0);
		cin.ignore();
	}
	
	return 1;
}
