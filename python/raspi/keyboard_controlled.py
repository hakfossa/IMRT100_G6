import imrt_robot_serial
import signal
import time
import sys
import random

import pygame


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



def drive_robot(direction, duration, l_speed_modifier=1, r_speed_modifier=1):
    
    l_speed = int(DRIVING_SPEED * direction * l_speed_modifier)
    r_speed = int(DRIVING_SPEED * direction * r_speed_modifier)
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(l_speed, r_speed)
        time.sleep(0.10)

def turn_robot(direction, duration):

    speed = TURNING_SPEED * direction
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


turn_timer = -1
print("sleep for 2")
time.sleep(2)
print("sleep done")


# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :

    """ sensor_rfwd = motor_serial.get_dist_1() 
    sensor_lfwd = motor_serial.get_dist_2()
    sensor_right = motor_serial.get_dist_3()
    sensor_left = motor_serial.get_dist_4()
 """

    try:  # Try such that other keypresses will not generate errors
        if k.is_pressed('w'):
           drive_robot(FORWARDS, 0.1) 

        elif k.is_pressed('s'):
            drive_robot(BACKWARDS, 0.1)

        elif k.is_pressed('d'):
            turn_robot(RIGHT, 0.1)
        
        elif k.is_pressed('a'):
            turn_robot(LEFT, 0.1)

    except SystemExit:
        sys.exit()  
    
    try: 
        pass
    except KeyboardInterrupt:
        break

# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
print("I don't hate you")

