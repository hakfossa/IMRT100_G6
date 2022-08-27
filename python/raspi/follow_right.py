import imrt_robot_serial
import signal
import time
import sys
import random


LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 100
TURNING_SPEED = 100
STOP_DISTANCE = 25


def stop_robot(duration):

    iterations = int(duration * 10)
    
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)



def drive_robot(direction, duration):
    
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, speed)
        time.sleep(0.10)

def turn_robot(direction, duration):

    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, -speed)
        time.sleep(0.10)






# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port. Exit if serial port cannot be opened
try:
    motor_serial.connect("/dev/ttyUSB0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

    
# Start serial receive thread
motor_serial.run()


# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :

    sensor_fwd = motor_serial.get_dist_1()
    sensor_right = motor_serial.get_dist_3()
    sensor_left = motor_serial.get_dist_4()


    if sensor_fwd < 25:
        #stop_robot(1)
        if sensor_left >sensor_right*2:
            turn_robot(LEFT,1.8)
        else:
            turn_robot(RIGHT, 1.8)

    elif sensor_right > 50:
        turn_robot(RIGHT,1.8)        

    elif sensor_right < 15:
        turn_robot(LEFT,0.3)
        drive_robot(FORWARDS, 0.3)

    elif sensor_left < 15:
        turn_robot(RIGHT, 0.3)
        drive_robot(FORWARDS, 0.3)

    else: 
        drive_robot(FORWARDS, 0.3)



# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
print("I don't hate you")

