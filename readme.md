#QUTRC Air Hockey Robot
##Brief
This is the git repo for the Air Hockey Robot being developed by the QUT Robotics club. The robot will function by controlling a revolute-revolute robotic armature with a Raspberry Pi 2 capable of moving an air-hockey mallet at fast enough speeds to rival even the fastest human players.  The code will be written in C++.

To do this the project will be constructed of 3 main parts:

 - Computer Vision System (RPi Camera + OpenCV)
 - A.I. Decision making
 - Servo Control System (Inverse Kinematics + Camera Correction)

The Raspberry Pi mounted on the robot will be rigged to auto-update and recompile from the master branch if any changes have been made since the last time the robot was tested. All development must be made on an external branch before pulling onto the master branch. 

#TODO
1. Populate TODO list
#Computer Vision System
Prototyping with the vision system will initially be completed using the CMUcam5 Pixy. Work done on the vision system using the Raspberry Pi Camera with OpenCV must therefore produce outputs in the same format for use by the AI. See [here](http://cmucam.org/projects/cmucam5/wiki/Hooking_up_Pixy_to_a_Microcontroller_like_an_Arduino) for information on how Pixy encodes it's object detection.
#AI Decision Making
The AI decision making algorithm must be designed to accept Pixy-like (explained above) object detection blocks in order to produce output to the servo control system.

- Where the puck currently is and what trajectory it is travelling in.
- Where the walls currently are and the likely trajectory of the puck if bouncing off the wall.
- Where the mallet (held by the robot arm) currently is, if it is in the right place and if it is moving at the intended speed to hit the puck at the intended angle and speed.
#Servo Control System
Controls two servos using inverse kinematics to move the air-hockey mallet to the desired location as set by the AI. Inputs to this, received from the AI system are yet to be clarified