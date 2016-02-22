import pygame

class Rect:
    """
    p1 is top left.
    p2 is bottom right.
    """
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2



    def pointCollides(self, point):
        if point.x > p1.x and point.x < p2.x:
            if point.y > p2.y and point.y < p1.y:
                return True
        return False

    def draw(self, surf):
        diff = self.p1.getDifference(self.p2)
        pygame.draw.rect(surf, (0, 0, 255), pygame.Rect(self.p1.x, self.p1.y, diff[0], diff[1]))