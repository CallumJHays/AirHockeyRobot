from math import atan, degrees
from model.point import Point
import pygame

class Line():
    def __init__(self, slope, intercept, parent=None):
        self.slope = slope
        self.intercept = intercept
        self.parent = parent

    def setSlope(self, value):
        self.slope = value

    def setIntercept(self, value):
        self.intercept = value

    def getSlope(self):
        return self.slope

    def getIntercept(self):
        return self.intercept

    """
    Provided with x, returns y on line
    """
    def getY(self, x):
        return self.slope*x + self.intercept

    """
    Provided with y, returns x on line
    """
    def getX(self, y):
        return (self.intercept-y)/-self.slope

    """
    Returns point of intersection of two lines
    """
    def getIntersection(self, line):
        x = (self.intercept()-line.intercept())/(line.slope-self.slope)
        y = self.getSlope()*x + self.getYIntercept()
        return Point(x, y, self.parent)

    """
    Returns line segment. Segment start and end pos defined by
    bounds. Uses -bounds and bounds as the X positions for the two points.
    Calculates y from those x positions.
    """
    def getLineSegment(self, bounds):
        x1 = self.getX(-bounds)
        y1 = self.getY(x1)

        x2 = self.getX(bounds)
        y2 = self.getY(x2)
        return LineSegment(Point(x1, y1), Point(y1, y2), self.parent)

class LineSegment():
    def __init__(self, point1=None, point2=None, parent=None):
        self.p1 = point1
        self.p2 = point2
        self.parent = parent

        self.color = (255, 255, 100)

    """
    If the slope is undefined, return Noneparent=NoneZ
    """
    def getSlope(self):
        try:
            diff = self.p1.getDifference(self.p2)
            return float(diff[1])/diff[0]
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
        #try:
        x = (self.getYIntercept()-line.getYIntercept())/(line.getSlope()-self.getSlope())
        y = self.getSlope()*x + self.getYIntercept()
        return Point(x, y, self.parent)
        #except ZeroDivisionError:
        #    return None

    """
    Get length of line
    """
    def getLength(self):
        return self.p1.getDistance(self.p2)

    def draw(self):
        pygame.draw.line(self.parent.surface, self.color, self.parent.toPygame(self.p1.getTuple()), self.parent.toPygame(self.p2.getTuple()), 5)


    """
    Reflects specified line off self. It returns point of reflection, and angle of reflection
    """
    def reflect(self, line):
        diff = self.p1.getDifference(self.p2)
        p1 = self.getIntersection(line)
        p2 = p1.polarToCartesian((self.getAngle()-line.getAngle())+self.getAngle(), line.p1.getDistance(p1))
        ls = LineSegment(p1, p2, self.parent)
        ls.setColor((255, 0, 0))

        print("Inter", line.p1.getDistance(p1))
        print("LS", ls.getLength())

        return ls

    def setColor(self, color):
        self.color = color

    """
    Returns line in slope-intercept form
    """
    def getLine(self):
        return Line(self.getSlope, self.getYIntercept())