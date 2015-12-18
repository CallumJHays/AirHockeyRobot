from objects.simobject import SimObject
import constants
import pygame

class Arm(SimObject):
    def __init__(self):
        armLength = constants.ARM_LENGTHS[0]+constants.ARM_LENGTHS[1]
        self.surface = pygame.Surface((armLength*2, armLength*2))

    def tick(self):
        pass

    def draw(self):
        pygame.draw.circle(self.surface, (0, 255, 0), (10, 10), 10)
        self.surface.fill((255, 255, 255, 200))
        return self.surface