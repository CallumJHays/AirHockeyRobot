import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)



class Servo:
	def __init__(self, isElbowServo):
		pin = 0
		if(isElbowServo):
			pin = 1
		GPIO.setup(pin, GPIO.OUT)
		self.pwm = setup(pin, 50)
		self.pwm.start(50)

	def set(self, deg)
		self.pwm.changeDutyCycle(deg)