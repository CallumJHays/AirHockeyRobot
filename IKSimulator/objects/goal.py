from objects.simobject import SimObject
import pygame
import constants

class Goal(SimObject):
    def __init__(self):
        self.surface = pygame.Surface(constants.GOAL_SIZE)
        self.color = (255, 0, 0)

    def setColor(self, color):
        self.color = color

    def tick(self):
        pass

    def draw(self):
        self.surface.fill(self.color)
        return self.surface