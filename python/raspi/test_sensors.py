import imrt_robot_serial
import signal
import time
import sys
import random
import os




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


print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now:
    os.system('clear')
    print("sensor 3:", motor_serial.get_dist_3())
    time.sleep(0.1)




print('I dont hate you.')

