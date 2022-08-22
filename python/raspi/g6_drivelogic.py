from IMRT100_G6.python.raspi.imrt_robot_serial import IMRTRobotSerial
import imrt_robot_serial
import signal
import time
import sys
#import random

FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 100
TURNING_SPEED = 100

def stop_robot(duration):
    
    iterations = int(duration*10)

    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)


def drive_robot(direction, duration):

    speed = DRIVING_SPEED * direction
    iterations = int(10*duration)

    for i in range(iterations):
        motor_serial.send_command(speed, speed)
        time.sleep(0.10)








motor_serial = IMRTRobotSerial()


