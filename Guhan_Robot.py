import time

from AADFramework.ArduinoComponents import ServoMotor, DigitalInput, DigitalOutput, ControlBoard, InputMonitor
from AADFramework.ArduinoComponents import menuGenerator, ToPoint, FiveBarDrawingRobot, Constants

###################################
#  Build Drawing Robot
##################################
controller = ControlBoard('COM7')

################################################
# you may build monitor if you have input devices
# monitor = controller.buildInputMonitor()
#################################################
# Build Drawing Robot
robot = FiveBarDrawingRobot()
# LeftMotorPinNo = 12; RightMotorPinNo = 10; HeadMotorPinNo = 8
# You may assign different pin number to the motors as you wish
robot.build(controller, 12, 10, 8)
#######################################################################
# you may add more Arduino devices needed in your application below
#######################################################################
#
#
######################################################################

################
# start to run
controller.start()


# monitor.start()   # if you have input devices
##################


##############################################
# functions used in Tutorial
##############################################
# def robotWarmupExercise():
# Move robot head around with given positions defined
# by  angle degrees of left and right motors
# This function can be called to see robot's head can
# be moved around accordingly
def robotWarmupExercise():
    robot.headUp()
    for i in range(1, 4):
        robot.driveTo(90, 90, 2 * i)
        robot.driveTo(140, 40, 2 * i)
    for i in range(1, 71, 10):
        robot.driveTo(20 + i, 20 + i, i)
        robot.driveTo(170 - i, 150 - i, i)
    robot.driveTo(100, 80, 5)
    for i in range(3):
        robot.headUp()
        robot.headDown()
    robot.home()


##################################################################
# def robotHeadUpDown()
# To show how to use robot’s commands to change robot’s head position
###############################################################
def robotHeadUpDown():
    # move robot head to a location defined by motor degrees
    robot.driveTo(110, 70)
    # let robot repeat head down/ head up # for three times
    for i in range(3):
        robot.headUp()  # head up
        robot.headDown()  # head down
    # let robot head move back to parking place
    robot.home()


##################################################################
# def moveToPointWithDegrees()
# To show how to use Robot’s command to move robot’s head to
# a point defined by motor’s degree
###############################################################

def moveToPointWithDegrees():
    while True:
        robot.headUp()  # head up
        # ask user key in motor degrees
        xAngle = int(input('enter left-motor angle:\t'))
        yAngle = int(input('enter right-motor angle:\t'))
        # robot.driveTo(leftMotorDegree, rightMotorDegree,tuningSpeed)
        robot.driveTo(xAngle, yAngle, 2)
        if input('Try again?(y/n)') != 'y':
            robot.headUp()
            break


##################################################################
# def moveToPointWithXYCoordinates()
# To show how to use Robot’s command to move robot’s head
# to a point defined by XY coordinates
###############################################################
def moveToPointWithXYCoordinates():
    while True:
        # machine.headUp()
        xPos = int(input('enter posX:\t'))
        yPos = int(input('enter posY:\t'))
        # ToPoint(x,y,mode) is a special data structure, which
        # is  used to define a point at  the white board to
        # instruct the robot how to move to that point
        # if mode == ToPoint.MOVING the Robot keeps head up and
        # moves to the specified point.
        # if mode == TopPoint.DRAWING, the Robot low down the head and
        # draw a line to the specified point
        pt = ToPoint(xPos, yPos, ToPoint.MOVING)  # move to the given point
        robot.moveTo(pt)
        if input('Try again?(y/n)') != 'y':
            robot.headUp()
            break


##################################################################
# def drawSingleLineWithTwoPoints()
# To show how to generate two ToPoints with given XY coordinates
# of two points on white board and use Robot’s commands to draw a line
###############################################################
def drawSingleLineWithTwoPoints():
    while True:
        p1_x = int(input('start-point.x:\t'))
        p1_y = int(input('start-point.y:\t'))

        # mode = ToPoint.MOVING,  robot moves to the start point
        startPt = ToPoint(p1_x, p1_y, ToPoint.MOVING)

        p2_x = int(input('end-point.x.x:\t'))
        p2_y = int(input('end-point.y:\t'))
        # mode = ToPoint.DRAWING, robot draws to the end point
        endPt = ToPoint(p2_x, p2_y, ToPoint.DRAWING)

        robot.drawLine(startPt, endPt)
        if input('Try again?(y/n)') != 'y':
            robot.headUp()
            break


##################################################################
# drawMultipleLinesWithPointList()
# To show how to create a list of ToPoints with given XY coordinates
# of  points on white table and use Robot;s commands to
# draw multiple lines.
###############################################################
def drawMultipleLinesWithPointList():
    linePoints = []
    i = 1
    while True:
        ptX = int(input('Point {} x:\t'.format(i)))
        ptY = int(input('Point {} y:\t'.format(i)))
        while True:
            rpl = input('Press D for drawing to and M for moving to:\t')
            if rpl == 'D' or rpl == 'd':
                point = ToPoint(ptX, ptY, ToPoint.DRAWING)
                break
            elif rpl == 'M' or rpl == 'm':
                point = ToPoint(ptX, ptY, ToPoint.MOVING)
                break
            else:
                input('Invalid input/ Please press ENTER to try again!')
        linePoints.append(point)
        i += 1
        rpl = input('Do you want to add more points? (y/n):\t')
        if rpl == 'y' or rpl == 'Y':
            continue
        else:
            break
    # robot.drawLines(linePoints) - linePoints is python list, which
    # contains all the ToPoints to instruct the robot to draw multiple lines
    # accordingly
    robot.drawLines(linePoints)


##################################################################
# drawMultipleLinesWithPointList()
# To show how to create a list of ToPoints with given XY coordinates
# of  points on white table and use Robot's commands to
# draw multiple lines.
# The special symbol consists of three horizontal lines and
# three vertical lines crossing three horizontal lines is going to
# be drawn in the rectangle with its top-left point at (-10,60)
# and bottom-riht point  at(10,30)
###############################################################
def drawASpecialSymbol():
    input('Make sure a marker is mounted before press ENTER to continue')



def tutorial():
    menuTitle = 'Tutorial of using Drawing Robot'
    items = ['Robot Warmup Exercise',
             'Robot Head Down and Up',
             'Move to a point with motors degrees ',
             'Move to a point with XY coordinates',
             'Draw a line with two given points',
             'Draw multiple lines with list of given points',
             'Example of drawing a special symbol',
             ]
    while True:
        rpl = menuGenerator(menuTitle, items)
        if rpl == 1:
            robot.headUp()
            print('Dancing started. Waiting...')
            robotWarmupExercise()
            input('Dancing finished.., press ENTER to continue')
        elif rpl == 2:
            robotHeadUpDown()
        elif rpl == 3:
            moveToPointWithDegrees()
        elif rpl == 4:
            moveToPointWithXYCoordinates()
        elif rpl == 5:
            drawSingleLineWithTwoPoints()
        elif rpl == 6:
            drawMultipleLinesWithPointList()
        elif rpl == 7:
            drawASpecialSymbol()
        else:
            robot.home()
            break


#########################################
# Student Project Task Implementation
#########################################
#########################################
# Student Project Task Implementation
#########################################
def studentProjectTask1():
    while True:
        number=input("Which number do u want to write, 1 or 7?")
        if number=='1' or number=='7':
            break
        else:
            print("I can only accept 1 or 7")

    xleft = int(-robot._drawingWidth/6)
    xright = int(robot._drawingWidth/6)
    ytop = robot._drawingTop
    ymid = int((robot._drawingTop-robot._drawingBottom)/2+robot._drawingBottom)
    ybtm = robot._drawingBottom

    if (number=='7'):
        linePoints = []
        pt_x,pt_y=(xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)
        pt_x, pt_y=(xright, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y=(xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        robot.drawLines(linePoints)
    elif (number=='1'):
        linePoints = []
        pt_x,pt_y=(xright, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)
        pt_x,pt_y=(xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        robot.drawLines(linePoints)
    else:
        pass

    robot.headUp()



#########################################
# Student Project Task Implementation
#########################################
def studentProjectTask2():
    while True:
        number2 = input("Which number do u want to write from 0 to 9?")
        if number2 == '0' or number2 == '1' or number2 == '2' or number2 == '3' or number2 == '4' or number2 == '5' or number2 == '6' or number2 == '7' or number2 == '8' or number2 == '9':
            break
        else:
            print("I can only accept 0 to 9")

    xleft = int(-robot._drawingWidth/6)
    xright = int(robot._drawingWidth/6)
    ytop = robot._drawingTop
    ymid = int((robot._drawingTop-robot._drawingBottom)/2+robot._drawingBottom)
    ybtm = robot._drawingBottom






    if(number2 == '9'):
        linePoints = []
        pt_x, pt_y = (xright, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)

        pt_x, pt_y = (xleft, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xright, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        robot.drawLines(linePoints)




    elif (number2 == '8'):
        linePoints = []
        pt_x, pt_y = (xright, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)

        pt_x, pt_y = (xleft, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xright, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xleft, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        robot.drawLines(linePoints)




    elif (number2 == '7'):
        linePoints = []
        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)
        pt_x, pt_y = (xright, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        robot.drawLines(linePoints)


    elif (number2 == '6'):
        linePoints = []
        pt_x, pt_y = (xright, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)

        pt_x, pt_y = (xleft, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xleft, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xleft, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        robot.drawLines(linePoints)

    elif (number2 == '5'):
        linePoints = []
        pt_x, pt_y = (xleft, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)

        pt_x, pt_y = (xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xright, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xright, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)


        robot.drawLines(linePoints)

    elif (number3 == '4'):
        linePoints = []
        pt_x, pt_y = (xright, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)

        pt_x, pt_y = (xleft, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xleft, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xright, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xright, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        robot.drawLines(linePoints)

    elif (number2 == '3'):
            linePoints = []
            pt_x, pt_y = (xright, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)


            robot.drawLines(linePoints)





    elif (number2 == '2'):
        linePoints = []
        pt_x, pt_y = (xleft, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)

        pt_x, pt_y = (xright, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xright, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ymid)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        pt_x, pt_y = (xleft, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        pt_x, pt_y = (xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)

        robot.drawLines(linePoints)



        robot.drawLines(linePoints)
    elif (number2 == '1'):
        linePoints = []
        pt_x,pt_y=(xright, ytop)
        posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
        linePoints.append(posn)
        pt_x,pt_y=(xright, ybtm)
        posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
        linePoints.append(posn)
        robot.drawLines(linePoints)
    else:
        pass

    robot.headUp()


def studentProjectTask3():
    positioning()
    number3()



def positioning():
    while True:
        print('Please input values for the X and y Axis.')
        print('position(-20,60)  (20, 46)')
        xPos = int(input('enter posX:\t'))
        yPos = int(input('enter posY:\t'))
        pt = ToPoint(xPos, yPos, ToPoint.MOVING)
        robot.moveTo(pt)
        ans = input('Would you like to continue?')
        if ans == 'yes':
            xPos = int(input('enter posX:\t'))
            yPos = int(input('enter posY:\t'))
            pt = ToPoint(xPos, yPos, ToPoint.MOVING)
            robot.moveTo(pt)
        else:
            break



def number3():
    while True:
        number3 = input("Choose a number from 0 to 9 to be written.")
        if number3 in '0123456789':

            xleft = int(-robot._drawingWidth/6)
            xright = int(robot._drawingWidth/8)
            ytop = int(robot._drawingTop - 10)
            ymid = int((robot._drawingTop-robot._drawingBottom)/3+robot._drawingBottom)
            ybtm = robot._drawingBottom

        if (number3 == '9'):
            linePoints = []
            pt_x, pt_y = (xright, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
            linePoints.append(posn)

            pt_x, pt_y = (xleft, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            robot.drawLines(linePoints)




        elif (number3 == '8'):
            linePoints = []
            pt_x, pt_y = (xright, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
            linePoints.append(posn)

            pt_x, pt_y = (xleft, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            pt_x, pt_y = (xleft, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            robot.drawLines(linePoints)




        elif (number3 == '7'):
            linePoints = []
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            robot.drawLines(linePoints)


        elif (number3 == '6'):
            linePoints = []
            pt_x, pt_y = (xright, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
            linePoints.append(posn)

            pt_x, pt_y = (xleft, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            pt_x, pt_y = (xleft, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            pt_x, pt_y = (xleft, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            robot.drawLines(linePoints)

        elif (number3 == '5'):
            linePoints = []
            pt_x, pt_y = (xleft, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
            linePoints.append(posn)

            pt_x, pt_y = (xright, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            pt_x, pt_y = (xright, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            robot.drawLines(linePoints)

        elif (number3 == '4'):
                linePoints = []
                pt_x, pt_y = (xright, ymid)
                posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
                linePoints.append(posn)

                pt_x, pt_y = (xleft, ymid)
                posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
                linePoints.append(posn)
                pt_x, pt_y = (xleft, ytop)
                posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
                linePoints.append(posn)

                pt_x, pt_y = (xleft, ymid)
                posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
                linePoints.append(posn)
                pt_x, pt_y = (xright, ymid)
                posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
                linePoints.append(posn)

                pt_x, pt_y = (xright, ytop)
                posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
                linePoints.append(posn)
                pt_x, pt_y = (xright, ybtm)
                posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
                linePoints.append(posn)

                robot.drawLines(linePoints)

        elif (number3 == '3'):
            linePoints = []
            pt_x, pt_y = (xright, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)


            robot.drawLines(linePoints)



        elif (number3 == '2'):
            linePoints = []
            pt_x, pt_y = (xleft, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
            linePoints.append(posn)

            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            pt_x, pt_y = (xright, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ymid)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            pt_x, pt_y = (xleft, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            pt_x, pt_y = (xright, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)

            robot.drawLines(linePoints)

            robot.drawLines(linePoints)
        elif (number3 == '1'):
            linePoints = []
            pt_x, pt_y = (xright, ytop)
            posn = ToPoint(pt_x, pt_y, ToPoint.MOVING)
            linePoints.append(posn)
            pt_x, pt_y = (xright, ybtm)
            posn = ToPoint(pt_x, pt_y, ToPoint.DRAWING)
            linePoints.append(posn)
            robot.drawLines(linePoints)
        else:
            pass

        robot.headUp()













############################################################

def main(isDebugging=False):
    Constants.isDebugging = isDebugging
    robot.home()
    menuTitle = 'Five-Bar Drawing Robot Controller'
    items = [
        'System Setup/Calibration',
        'Tutorial of Using Drawing Robot',
        'Project Task 1 ',
        'Project Task 2 ',
        'Project Task 3'
    ]
    while True:
        rpl = menuGenerator(menuTitle, items)
        if rpl == 1:
            robot.systemCalibration()
        elif rpl == 2:
            tutorial()
        elif rpl == 3:
            studentProjectTask1()
        elif rpl == 4:
            studentProjectTask2()
        elif rpl == 5:
            studentProjectTask3()
        else:
            robot.home()
            break
    controller.shutdown()
    print('\n' * 4)
    print('')
    print('Thank you very much for using NYP Five-Bar Drawing Robot!')
    print('')


main()