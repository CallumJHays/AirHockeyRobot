from model.point import Point
from math import sqrt

class Circle:
    def __init__(self, pos, r):
        self.radius = r
        self.pos = pos

    """
    Returns boolean if point is in circle
    """
    def pointCollides(self, point):
        return self.pos.getDistance(point) < self.radius

    """
    Get intersection(s) of a line
    NOT WORKING YET - Feel free to add support for this :}
    """
    def i(self, line):
        a = 1
        b = -1
        c = line.getYIntercept()

        r = self.radius
        print(a, b, c, r)

        x1 = ((a*c) - (b*sqrt((r**2)*(a**2 + b**2)) - c**2))/a**2+b**2
        y1 = ((b*c) + (a*sqrt((r**2)*(a**2 + b**2)) - c**2))/a**2+b**2
        print(x1, y1)








