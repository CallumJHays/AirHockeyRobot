from math import sqrt
import math
import pygame

class Point:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def __repr__(self):
        return str("Point(%d,%d)"%(self.x, self.y))

    def getTuple(self):
        return (self.x, self.y)

    def getDifference(self, point):
        return point.x-self.x, point.y-self.y

    def getDistance(self, point):
        diff = self.getDifference(point)
        return sqrt((diff[0]**2)+(diff[1]**2))

    def draw(self):
        pygame.draw.circle(self.parent.surface, (100, 255, 100), self.parent.toPygame(self.getTuple()), 5)

    """
    Converts from polar to cartesian space.
    """
    def polarToCartesian(self, angle, length):
        x = length * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(angle))
        return Point(x, y)
