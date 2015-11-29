import pygame, math, sys

SCREEN_RESOLUTION = (750, 750)

LENGTHS = 300, 350

class Application:
    def __init__(self):
        self.running = True
        self.mousePos = (1, 1)

        self.ai = AirHockeyAI()

    """
    Initializes the appropriate stuff.
    Starts the main loop.
    """
    def start(self):
        pygame.init()
        self.font = pygame.font.Font(None, 24)
        self.running = True
        self.initDisplay()
        self.loop()

    """
    See self.loop comment
    """
    def stop(self):
        self.running = False

    """
    Initializes the display with the appropriate screen resolution
    Called in self.start
    """
    def initDisplay(self):
        self.surface = pygame.display.set_mode(SCREEN_RESOLUTION)
        pygame.display.set_caption('Air Hockey Robot Simulation')

    """
    Main Loop
    Loops until self.running == false
    """
    def loop(self):
        while self.running:
            self.surface.fill((0, 0, 0))          #Fills display with white
            self.handleEvents()                         #Handles events

            self.drawQuadrants()
            self.drawArm()
            self.drawAngleValues()

            pygame.display.flip()                       #Draws display buffer to display



        """
        Quitting procedure.
        """
        pygame.quit()
        sys.exit(0)

    """
    Handles pygame events.
    """
    def handleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.MOUSEMOTION:
                self.mousePos = event.dict["pos"]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()

    def polarToCartesian(self, length, angle):
        x = length * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(angle))
        return(x, y)

    def drawArm(self):

        base = (0, 0)
        target = fromPygame(self.mousePos)

        """Gets angle to the midarm"""
        globalBaseAngle = self.ai.getBaseAngle(target)


        """Gets angle to the end arm"""
        globalMidArmAngle = self.ai.getMidArmAngle(target)

        """Deals with the coordinate mid arm"""
        midArm = self.polarToCartesian(self.ai.upperArmLength, globalBaseAngle)

        """ Deals with the coordinate for the end of the arm: essentially mathematical version of target"""
        cart = self.polarToCartesian(self.ai.lowerArmLength, globalMidArmAngle)
        endArm = midArm[0]+cart[0], midArm[1]+cart[1]

        pygame.draw.line(self.surface, (0, 255, 0), toPygame(base), toPygame(midArm), 3)
        pygame.draw.line(self.surface, (0, 255, 0), toPygame(midArm), toPygame(endArm), 3)
        #pygame.draw.line(self.surface, (0, 0, 255), toPygame(target), toPygame(base), 3)

    def iT(self, t):
        return -t[0], -t[1]

    def drawOrigin(self):
        p1 = toPygame((0, 0))
        p2 = self.mousePos
        pygame.draw.line(self.surface, (255, 255, 255), p1, p2, 3)

    def drawQuadrants(self):
        pygame.draw.line(self.surface, (255, 0, 0), (0, SCREEN_RESOLUTION[1]/2), (SCREEN_RESOLUTION[0], SCREEN_RESOLUTION[1]/2))
        pygame.draw.line(self.surface, (255, 0, 0), (SCREEN_RESOLUTION[0]/2, 0), (SCREEN_RESOLUTION[0]/2, SCREEN_RESOLUTION[1]))

    def drawAngleValues(self):
        baseAngleText = self.font.render("Base Angle: " + str(self.ai.getBaseAngle(self.mousePos)), True, (255,255,255))
        baseAngleTextBox = baseAngleText.get_rect()
        baseAngleTextBox.centerx = self.surface.get_rect().centerx
        self.surface.blit(baseAngleText, baseAngleTextBox)


class AirHockeyAI:
    def __init__(self):
        self.upperArmLength = LENGTHS[0]/2
        self.lowerArmLength = LENGTHS[1]/2

        self.basePos = (0, 0)


    def getDifference(self, pos1, pos2):
        return (pos2[0]-pos1[0], pos2[1]-pos1[1])

    def getDistance(self, pos1, pos2):
        xDiff = self.getDifference(pos1, pos2)[0]
        yDiff = self.getDifference(pos1, pos2)[1]
        return math.sqrt(xDiff**2 + yDiff**2)


    """
    Returns the angle for the upper arm's servo.
    0 is defined as facing right
    """
    def getBaseAngle(self, targetPos):
        #Angle local to the triangle.
        triangleAngle = self.calculateInverseKinematics(targetPos)[1]
        a = self.findAngle((0, 0), targetPos)
        return triangleAngle+a

    def findAngle(self, pos1, pos2):
        try:
            diff = self.getDifference(pos1, pos2)
            deg = math.degrees(math.atan(float(diff[1])/float(diff[0])))
            if diff[0] < 0:
                deg = 180+deg
            elif diff[1] < 0 and diff[0] > 0:
                deg = 360+deg
            return deg
        except ZeroDivisionError:
            return self.findAngle((pos1[0]+1, pos1[1]), pos2)

    """
    Returns the angle for the lower arm's servo.
    0 is defined as right.
    """
    def getMidArmAngle(self, targetPos):
        return (self.getBaseAngle(targetPos)-180)+self.calculateInverseKinematics(targetPos)[2]

    def calculateInverseKinematics(self, targetPos):
        try:
            """
            L1, 2, and 3 correspond to the triangle lengths for the IK
            """
            l1 = self.upperArmLength
            l2 = self.lowerArmLength
            l3 = self.getDistance(self.basePos, targetPos)

            if l3 > l1+l2:
                l3 = l1+l2

            """
            Law of Cosines - find an angle!
            """

            #L1 = upperArm
            #L2 = lowerArm
            #L3 = Distance from base to point

            #A1 = angle opposite L1
            #A2 = angle opposite L2; Base Angle
            #A3 = angle opposite L3; Angle between lower and upper arms
            a3 = -math.degrees(math.acos((l1**2 + l2**2 - l3**2)/(2*l1*l2)))
            a1 = -math.degrees(math.acos((l2**2 + l3**2 - l1**2)/(2*l2*l3)))
            a2 = -math.degrees(math.acos((l3**2 + l1**2 - l2**2)/(2*l3*l1)))


            #print(a1,a2,a3)

            return (a1, a2, a3)
        except:
            print("Invalid stuff.")
            return(60, 60, 60)



"""
Essentially makes the origin in the centre of the window, rather than top right.
"""
def toPygame(pos):
    return pos[0]+SCREEN_RESOLUTION[0]/2, (-pos[1]+SCREEN_RESOLUTION[1]/2)

def fromPygame(pos):
    return pos[0]-SCREEN_RESOLUTION[0]/2, -(pos[1]-SCREEN_RESOLUTION[1]/2)

"""
If this file was not imported, then start the application's code.
"""
if __name__ == "__main__":
    app = Application()
    app.start()