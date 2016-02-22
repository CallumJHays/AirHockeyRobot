/*
 * Name: QUTRCAH_ArduinoClient
 * Author: John Board
 * Date: 22/01/2016
 * Description:
 *  Arduino slave to the RPiv2 for it's IO (serial/PWM)
 *  RPiv2 does all the logic and heavy lifting, the arudino
 *  serves mainly to generate the PWM signals for the
 *  servos.
 * 
 * 
 * Board: Mega (subject to become Teensy or Uno)
 * Pinout:
 *  P2: Upper Servo
 *  P3: Lower Servo
 *  1/0: TX/RX Computer Serial
 *  P18/19: TX/RX CMUCam Serial
 *    - Please note that we may want to switch CMUCam to using SPI on the RPi
 * 
 * Computer Comms:
 * 
 * #{motor to move} {position to move to}\n
 * 
 * For example:
 * #0 500
 * #1 2500
 */

#include <Servo.h>

Servo upperArm;
Servo lowerArm;

char serialBuffer[5];
int servoSelected;
int pulseSelected;

int upperArmPulse = 1500;
int lowerArmPulse = 1500;

void setup(){
  initializeServos(); 
  Serial.begin(115200); 
}

void initializeServos(){
  lowerArm.attach(9);
  upperArm.attach(8);  
  return;
}

//====================[ LOGIC ]====================//

void loop() {
  processSerial();
  if(servoSelected == 8){
    Serial.println("8 used.");
    lowerArmPulse = pulseSelected; 
  } 
  if (servoSelected == 9) {
    Serial.println("9 used.");
    upperArmPulse = pulseSelected;
  }
  
  lowerArm.write(lowerArmPulse);
  upperArm.write(upperArmPulse);
  delay(500);
  lowerArm.write(lowerArmPulse);
  upperArm.write(upperArmPulse);
  delay(500);
}

boolean processSerial(){  
  if (Serial.available() > 0){
    if (Serial.read() == '#'){
      Serial.readBytes(serialBuffer, 6);      
      if(serialBuffer[1] == ' '){
        servoSelected = serialBuffer[0]-48;        
        pulseSelected = (serialBuffer[2]-48)*1000 + 
                      (serialBuffer[3]-48)*100 + 
                      (serialBuffer[4]-48)*10 + 
                      (serialBuffer[5]-48)*1;
        return true;
      }
    }  
  }
  return false;
}

