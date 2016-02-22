import math
from constants import ARM_LENGTHS

class AirHockeyAI:
    def __init__(self):
        self.upperArmLength = ARM_LENGTHS[0]/2
        self.lowerArmLength = ARM_LENGTHS[1]/2

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
            return(60, 60, 60)