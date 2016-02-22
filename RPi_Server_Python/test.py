import numpy as np
a = np.random.rand(480, 640, 3)  # create array of random values
b = a.tobytes()
c = np.fromstring(b).reshape(480, 640, 3)
print(a)
#print(b)
print("cat")
print(c)

