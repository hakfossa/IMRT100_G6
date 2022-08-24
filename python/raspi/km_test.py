# Py Modules
import signal
import time
import sys
import random

# Homebrew modules
import imrt_robot_serial
import imrt_connect

# Globals
LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 100
TURNING_SPEED = 100
STOP_DISTANCE = 25

tfreq = 10 # Timer Frequency, Execution frequency in Hz
tstep = 1/tfreq # Timer Step length

# Motile functions

def stop_robot(duration):
    iterations=int(duration*10)
    for i in range(iterations):
        motor_serial.send_command(0,0)
    time.sleep(tstep)

def drive_robot(direction, duration):
    speed = DRIVING_SPEED * direction
    iterations=int(duration*10)
    for i in range(iterations):
        motor_serial.send_command(speed,speed)
        time.sleep(tstep)

def turn_robot(direction, duration):
    motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
    time.sleep(tstep)

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

# Exec loop?
while not motor_serial.shutdown_now:
    dist_fwd = motor_serial.get_dist_1()
    dist_back = motor_serial.get_dist_2
    dist_r = motor_serial.get_dist_3()
    dist_l = motor_serial.get_dist_4()
    print("fwd:", dist_fwd, "bck:", dist_back, "R:", dist_r, "L:", dist_l)

    # Check if there is an obstacle in the way
    if dist_fwd < STOP_DISTANCE:
        # There is an obstacle in front of the robot
        # First let's stop the robot for 1 second
        print("halt")
        stop_robot(tstep)
    else:
        drive_robot(FORWARDS, tstep)

print("Bye!")