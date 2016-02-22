from model.point import Point
from math import sqrt
import pygame

class Circle:
    def __init__(self, pos, r, parent=None):
        self.radius = r
        self.pos = pos
        self.parent = parent

    def draw(self):
        pygame.draw.circle(self.parent.surface, (255, 0, 0), self.parent.toPygame(self.pos.getTuple()), self.radius, 5)

    """
    Returns boolean if point is in circle
    """
    def pointCollides(self, point):
        return self.pos.getDistance(point) < self.radius

    """
    Gets the point(s) of intersection of the line with the circle.
    """
    def getLineIntersection(self, line):
        #https://math.stackexchange.com/questions/228841/how-do-i-calculate-the-intersections-of-a-straight-line-and-a-circle
        #Line: y = mx + c
        #Circle: (x-p)**2 + (y-q)**2 = r**2

        m = line.getSlope()
        c = line.getYIntercept()
        p = self.pos.x
        q = self.pos.y
        r = self.radius

        A = (m**2 + 1)
        B = 2*((m*c) - (m*q) - p)
        C = (q**2 - r**2 + p**2 - 2*c*q + c**2)

        i = B**2 - (4*A*C)
        if i < 0:       #For some reason if i is less than 0, there are no points.
            return None
        elif i == 0:    #If i is 0 apparently there is point (the line is tangent)
            x1 = (-B + sqrt(B**2 - 4*A*C))/(2*A)
            y1 = (m*x1)+c
        elif i > 0:     #If i is greater than 0, there are two points of intersection
            x1 = (-B + (+sqrt(B**2 - 4*A*C)))/(2*A)
            y1 = (m*x1)+c

            x2 = (-B + (-sqrt(B**2 - 4*A*C)))/(2*A)
            y2 = ((m*x2)+c)
            return [Point(int(x1), int(y1), self.parent), Point(int(x2), int(y2), self.parent)]