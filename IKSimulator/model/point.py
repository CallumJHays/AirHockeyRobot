from math import sqrt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.x

    @x.setter
    def x(self, value):
        self.x = value

    @property
    def y(self):
        return self.y

    @x.setter
    def y(self, value):
        self.y = value

    def getDifference(self, point):
        return point.x-self.x, point.y-self.y

    def getDistance(self, point):
        diff = self.getDifference(point)
        return sqrt(diff[0]**2+diff[1]**2)