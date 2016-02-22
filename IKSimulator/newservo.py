import os

class Servo:
	def __init__(self, isElbowServo):
		self.pin = isElbowServo
		if(isElbowServo):
			self.minDeg = 10
			self.maxDeg = 110
		else:
			self.minDeg = -5
			self.maxDeg = 105

		self.minPulse = 90
		self.maxPulse = 210

		self.set(50)

	def set(self, deg):
		if(deg < self.minDeg or deg > self.maxDeg):
			return 0

		deg -= self.minDeg

		pulse = (self.maxPulse - self.minPulse) - (self.maxPulse - self.minPulse) / (self.maxDeg - self.minDeg) * deg + self.minPulse
		command = "echo "+str(self.pin)+"="+str(int(pulse))+" > /dev/servoblaster"
		print(command)
		os.system(command)

	def turnOff(self):
		os.system("echo "+str(self.pin)+"=0 > /dev/servoblaster")