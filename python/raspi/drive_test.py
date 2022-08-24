from turtle import forward
import imrt_robot_serial
import signal
import time
import sys
import random

FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 100
TURNING_SPEED = 100

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

def turn_left(duration = 1):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(-75,75)

def turn_right(duration = 1):
    iterations = int(duration * 10)
    for i in range(iterations):
        motor_serial.send_command(75,-75)

# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port. Exit if serial port cannot be opened
try:
    motor_serial.connect("/dev/ttyACM0")
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

       # Get and print readings from distance sensors
    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_4()
    print("Dist 1:", dist_1, "   Dist 2:", dist_2,"   Dist 3",dist_3,"   Dist 4",dist_4)

    if dist_1 < 15 or dist_2 < 15 or dist_3 < 15 or dist_4 < 15
        stop_robot(1)
        turn_left() 
    else:
        drive_robot(FORWARDS,1)
    
    
        