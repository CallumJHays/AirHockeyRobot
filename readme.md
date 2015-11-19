<h1>QUTRC Air Hockey Robot</h1>
<h2>Brief</h2>
This is the git repo for the Air Hockey Robot being developed by the QUT Robotics club. The robot will function by controlling a revolute-revolute robotic armature with a Raspberry Pi 2 capable of moving an air-hockey mallet at fast enough speeds to rival even the fastest human players.  The code will be written in C++.

To do this the project will be constructed of 3 main parts:

 - Computer Vision System (RPi Camera + OpenCV)
 - A.I. Decision making
 - Servo Control System (Inverse Kinematics + Camera Correction)

The Raspberry Pi mounted on the robot will be rigged to auto-update and recompile from the master branch if any changes have been made since the last time the robot was tested. All development must be made on an external branch before pulling onto the master branch. 
<h2>TODO</h2>
Arm Kinematics:
        - Find the kinematic equations (should return 0, 1, or 2 solutions (servo1 val, servo2 val) for any given tool point x, y)
        - Make an algorithm that, if given multiple solutions, finds the "closest" one (servo-wise)
        - Make algorithm to determine time till we reach desired point
       
Vision:
        - Train pixy
        - Find the homography matrix (should be fixed for each camera/location pair)
        - Set up our own camera and thresholds for the puck and the opponent's mallet
        - Test position accuracy extensively, optimise lots
       
Puck Kinematics:
        - Kalman filter the puck's position at any given moment
        - Get velocity vectors, estimate paths (need to deal with walls too!)
                - http://ieeexplore.ieee.org.ezp01.library.qut.edu.au/xpls/icp.jsp?arnumber=6491223
                - http://bit.ly/1Ln3XTd
                - http://bit.ly/1Ln3Xml
       
       
Combining all this:
        - First, make mallet follow puck.x. Should be a relatively lazy system, should still win most of the time
        - Next, look into hitting the puck
                - Much more complicated, because multiple variables involved.
                - Must be able to:
                        - get path of puck quickly
                        - find where (and when) it intersects our toolspace
                        - pick a point that we can reach at the same time the puck will
                        - actually move and hit it
                        - return to a base point
                - and this is just for blindly hitting, aiming is harder
        - Next, look into aiming the puck
                - http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6119852
                - http://ieeexplore.ieee.org.ezp01.library.qut.edu.au/xpls/icp.jsp?arnumber=7020736
                - http://ieeexplore.ieee.org.ezp01.library.qut.edu.au/search/searchresult.jsp?newsearch=true&queryText=Air%20Hockey

<h2>Computer Vision System</h2>
Prototyping with the vision system will initially be completed using the CMUcam5 Pixy. Work done on the vision system using the Raspberry Pi Camera with OpenCV must therefore produce outputs in the same format for use by the AI. See [here](http://cmucam.org/projects/cmucam5/wiki/Hooking_up_Pixy_to_a_Microcontroller_like_an_Arduino) for information on how Pixy encodes it's object detection.
<h2>AI Decision Making</h2>
The AI decision making algorithm must be designed to accept Pixy-like (explained above) object detection blocks in order to produce output to the servo control system.

- Where the puck currently is and what trajectory it is travelling in.
- Where the walls currently are and the likely trajectory of the puck if bouncing off the wall.
- Where the mallet (held by the robot arm) currently is, if it is in the right place and if it is moving at the intended speed to hit the puck at the intended angle and speed.

<h2>Servo Control System</h2>
Controls two servos using inverse kinematics to move the air-hockey mallet to the desired location as set by the AI. Inputs to this, received from the AI system are yet to be clarified