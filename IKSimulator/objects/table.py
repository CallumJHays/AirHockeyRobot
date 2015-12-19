import pygame
import constants
from objects.simobject import SimObject
from objects.goal import Goal
from objects.arm import Arm
from objects.puck import Puck
from model.point import Point

class Table(SimObject):
    def __init__(self):
        self.surface = pygame.Surface(constants.TABLE_SIZE)

        self.topGoal = Goal()
        self.topGoal.setColor((255, 100, 100))
        self.bottomGoal = Goal()
        self.bottomGoal.setColor((100, 100, 255))

        self.puck = Puck()

        self.arm = Arm()

    def tick(self):
        self.arm.tick()

        self.topGoal.tick()
        self.bottomGoal.tick()

    def draw(self):
        self.surface.fill((255, 255, 255))
        self.drawQuadrants()

        topGoalSurf = self.topGoal.draw()
        topGoalPos = self.toPygame((-topGoalSurf.get_width()/2, self.surface.get_height()-topGoalSurf.get_height()))
        self.surface.blit(topGoalSurf, topGoalPos)

        bottomGoalSurf = self.bottomGoal.draw()
        bottomGoalPos = self.toPygame((-bottomGoalSurf.get_width()/2, 0))
        self.surface.blit(bottomGoalSurf, bottomGoalPos)

        #self.arm.mousePos = self.getMousePos()

        armSurf = self.arm.draw()
        armPos = self.toPygame((-armSurf.get_width()/2, 0))
        self.surface.blit(armSurf, armPos)

        mPos = self.getMousePos()
        diff = self.puck.pos.getDifference(Point(mPos[0], mPos[1]))
        self.puck.vel = diff
        self.puck.draw(self.surface)

        return self.surface

    def drawQuadrants(self):
        pygame.draw.line(self.surface, (255, 0, 0), self.toPygame((-constants.TABLE_SIZE[0]/2, constants.TABLE_SIZE[1]/2)), self.toPygame((constants.TABLE_SIZE[0]/2, constants.TABLE_SIZE[1]/2)))
        pygame.draw.line(self.surface, (255, 0, 0), self.toPygame((0, 0)), self.toPygame((0, constants.TABLE_SIZE[1])))

    def toPygame(self, pos):
        return pos[0]+constants.TABLE_SIZE[0]/2, pos[1]

    def getMousePos(self):
        pos = pygame.mouse.get_pos()
        pos = (pos[0]-constants.BORDER_SIZE*constants.SCALE), (pos[1]-constants.BORDER_SIZE*constants.SCALE)
        pos = pos[0]/constants.SCALE, pos[1]/constants.SCALE
        pos = int(pos[0]-constants.TABLE_SIZE[0]/2), int(constants.TABLE_SIZE[1]-pos[1])
        return pos


