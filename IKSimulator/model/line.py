from math import atan, degrees
from model.point import Point

class Line:
    """
    p1 and p2 are the first and second points of the line.
    These points are defined by the class Point in model/point.py
    """



    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

    """
    If the slope is undefined, return None
    """
    def getSlope(self):
        try:
            diff = self.p1.getDifference(self.p2)
            return diff[1]/diff[0]
        except ZeroDivisionError:
            return None


    """
    Return slope degrees, unless the slope is undefined, then return 90
    """
    def getAngle(self):
        slope = self.getSlope()
        if not slope == None:
            return degrees(atan(self.getSlope()))
        else:
            return 90

    """
    y = mx + self.getYIntercept()
    """
    def getYIntercept(self):
        return self.p1.y - self.getSlope()*self.p1.x

    """
    Prints line's equation in slope intercept form
    """
    def printSlopeIntercept(self):
        print("y = "+str(self.getSlope())+"(x) + "+str(self.getYIntercept()))

    """
    Return point of intersection of specified line.
    If lines parallel, returns None
    """
    def getIntersection(self, line):
        try:
            x = (self.getYIntercept()-line.getYIntercept())/(line.getSlope()-self.getSlope())
            y = self.getSlope()*x + self.getYIntercept()
            return x, y
        except ZeroDivisionError:
            return None

    """
    Get length of line
    """
    def getLength(self):
        return self.p1.getDistance(self.p2)