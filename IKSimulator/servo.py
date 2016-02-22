import os

ELBOW_PIN = 1
BASE_PIN = 0

class Servo:
    def __init__(self, pin):
        self.pin = pin
        if pin == ELBOW_PIN:
            self.invert = False
            self.minDeg = 47
            self.maxDeg = 135
            self.minPulse = 1000
            self.maxPulse = 2100
        elif pin == BASE_PIN:
            self.invert = True
            print("Base")
            self.minDeg = 0
            self.maxDeg = 90
            self.minPulse = 930 #90 Deg
            self.maxPulse = 2200

        self.pulse(1500)

    def stop(self):
        self.set(0)

    def pulse(self, pulse):
        command = "echo "+str(self.pin)+"="+str(int(pulse/10))+" > /dev/servoblaster"
        print(command)
        os.system(command)

    def set(self, deg):
        self.pulsePerDeg = float(self.maxPulse - self.minPulse) / (self.maxDeg - self.minDeg)
        if self.invert: #Base Servo!
            pulse = self.maxPulse-(deg*self.pulsePerDeg)
        else:           #Elbow Servo!
            pulse = self.minPulse+(deg*self.pulsePerDeg)

        self.pulse(pulse)