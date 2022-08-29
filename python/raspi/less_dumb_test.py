# Py Modules
from re import A
import signal
import time
import sys
import random
import math
import operator
import keyboard

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
STOP_DISTANCE = 15
ROBOT_WIDTH = 0.40 # metres

# By default we set the robot to not be turning in any direction
TURNING_R = False
TURNING_L = False

tfreq = 10 # Timer Frequency, Execution frequency in Hz
tstep = 1/tfreq # Timer Step length

# oof ow my head hurty

#############################
#  _                        #
# | |                       #
# | |     ___   ___  _ __   #
# | |    / _ \ / _ \| '_ \  #
# | |___| (_) | (_) | |_) | #
# \_____/\___/ \___/| .__/  #
#                   | |     #
# v v v v v v v v v |_| v v #
#############################

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

# Main loop
print("Entrer dans la boucle. Ctrl+c pour terminer.")
while not motor_serial.shutdown_now:

print("Au revoir.")