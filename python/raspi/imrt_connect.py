# Py Modules
import signal
import time
import sys
import random

# Homebrew modules
import imrt_robot_serial
import imrt_connect

motor_serial = imrt_robot_serial.IMRTRobotSerial() # Create motor serial object

def handshake():
    print("Hi!")
    try: # Open serial port. Exit if serial port cannot be opened
        motor_serial.connect("/dev/ttyACM0")
    except:
        print("Could not open port. Is your robot connected?\nExiting program")
        sys.exit()
    motor_serial.run() # Start serial receive thread
