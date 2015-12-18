import pygame
import constants
from objects.simobject import SimObject

class Table(SimObject):
    def __init__(self):
        self.surface = pygame.Surface(constants.TABLE_SIZE)

    def tick(self):
        pass

    def draw(self):
        self.surface.fill((255, 255, 255))

    def drawQuadrants(self):
        pygame.draw.line(self.surface, (255, 0, 0), (0, constants.TABLE_SIZE[1]/2), (constants.TABLE_SIZE[0], constants.TABLE_SIZE[1]/2))
        pygame.draw.line(self.surface, (255, 0, 0), (constants.TABLE_SIZE[0]/2, 0), (constants.TABLE_SIZE[0]/2, constants.TABLE_SIZE[1]))


