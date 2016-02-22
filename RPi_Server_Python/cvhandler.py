#Name: cvhandler.py
#Author: John Board
#Date: 11/02/2016
#Description: OpenCV handler for the OpenCV for the AirHockeyRobot

import numpy as np
import cv2
import base64
import json
import threading
import time
import base64

import cProfile, pstats, StringIO

import mmap

class CVHandler:
    def __init__(self):
        self.newFrame = False
        self.frame = None
        self.running = False

        self.thread = None

        self.profiling = False

        self.o = open("cv", "r+")
        self.i = open("cv", "r+")

        self.o_mm = mmap.mmap(-1, 921600)#921600)
        #self.i_mm = mmap.mmap(-1, 1000000)

        self.f = ""




    def start(self):
        self.cam = cv2.VideoCapture(0)
        self.running = True

        self.thread = threading.Thread(target=self.render)
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        self.cam.release()
        self.running = False

    def tick(self):
        self.pr = cProfile.Profile()
        self.pr.enable()
        self.profiling = True

        ret, self.frame = self.cam.read()
        #s = self.frame.tostring()
        #self.o_mm.seek(0)
        #self.o_mm.write(s)

        #self.f = base64.b64encode(s)
        #self.f = s
        #print("Meow", self.frame.size)

        self.newFrame = True

        self.pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(self.pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print s.getvalue()


    def render(self):
        mm = None
        while self.running:
            if self.newFrame == True:
                #mm = mmap.mmap(-1, 921600)
                #print("Read", len(mm.read(921600)))
                #print(self.frame)
                #a = self.frame.tobytes()
                #pr#int("A", self.frame.size)
                #b= np.fromstring(a)
                #print("B", b.size)
                #print(b)

                #cv2.imshow("Frame", self.frame)
                pass
                #cv2.waitKey(1)
                #uv4l --driver raspicam --auto-video_nr --width=640 --height=480 --encoding=yuv420 --framerate 200


                #print(frame.size)
                #print(frame)
            else:
                print()



