"""
Essentially makes the origin in the centre of the window, rather than top right.
"""
from constants import *

def toPygame(pos):
    return pos[0]+SCREEN_RESOLUTION[0]/2, (-pos[1]+SCREEN_RESOLUTION[1]/2)

def fromPygame(pos):
    return pos[0]-SCREEN_RESOLUTION[0]/2, -(pos[1]-SCREEN_RESOLUTION[1]/2)