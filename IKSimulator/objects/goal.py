from objects.simobject import SimObject
import pygame
import constants

class Goal(SimObject):
    def __init__(self):
        self.surface = pygame.Surface(constants.GOAL_SIZE)

    def tick(self):
        pass

    def draw(self):
        self.surface.fill((255, 0, 0))
        return self.surface