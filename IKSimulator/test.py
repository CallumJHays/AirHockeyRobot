import servo, time

s = servo.Servo(1)

while True:
	try:
		print("0")
		s.set(0)
		time.sleep(2)
		print("90")
		s.set(90)
		time.sleep(2)
	except KeyboardInterrupt:
		s.set(0)
		break

