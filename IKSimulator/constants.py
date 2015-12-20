SCALE = 0.37

BORDER_SIZE = 150
DIMENSIONS = (1220, 2140)

TABLE_SIZE = (DIMENSIONS[0]-BORDER_SIZE*2, DIMENSIONS[1]-BORDER_SIZE*2)
GOAL_SIZE = (TABLE_SIZE[0]/3, TABLE_SIZE[1]/20)

SCREEN_RESOLUTION = int(DIMENSIONS[0]*SCALE), int(DIMENSIONS[1]*SCALE)

MALLET_RADIUS = 50

ARM_LENGTHS = (300/3)*2, (350/3)*2
print(ARM_LENGTHS)