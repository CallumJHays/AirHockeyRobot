from model.point import Point
import constants, pygame, math
from random import randint

class Puck:
    def __init__(self):
        self.pos = Point(-200 , 1500)
        self.vel = (3, 2)

    """
    p is particle, has pos (x, y) and vel (x, y)
    y is the height we're looking at
    w is const, table width
    assume table is centered around x=0
    """
    def calculateTrajectory(self, y):
        w = constants.TABLE_SIZE[0]
        A = (y-self.pos.y)*self.vel[0]/self.vel[1] + self.pos.x + w/2
        zeb = 1 if math.floor(A/w) % 2 == 0 else -1
        return zeb * ((A % w) - w / 2)

    def draw(self, surf):
        lastPos = self.pos.x, self.pos.y
        for y in range(1500, 100, -20):
            traj = self.calculateTrajectory(y), y
            pygame.draw.line(surf, (0, 0, 0), self.toPygame(lastPos), self.toPygame(traj), 10)
            lastPos = traj

    def toPygame(self, pos):
        return pos[0]+constants.TABLE_SIZE[0]/2, pos[1]
