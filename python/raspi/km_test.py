# Py Modules
from re import A
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

DX_fwd = []
DX_bck = []
DX_r = []
DX_l = []
DXlength = 10

# Go through the sensors and give them an appropriate amount of nothing
valid_sensors = [DX_fwd,DX_bck,DX_r,DX_l]
for sensor in valid_sensors:
    for i in range(DXlength):
        sensor.append(255)
print("Sensor arrays filled with gibberish")

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
    motor_serial.connect("/dev/ttyUSB0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

# Start serial receive thread
motor_serial.run()

# Functions that retrieve sensor data & avges
def sense_fwd():
    dist_fwd = motor_serial.get_dist_1()
    return dist_fwd
def avg_fwd():
    avg_dist_fwd = sum(DX_fwd)/DXlength
    return avg_dist_fwd

def sense_bck():
    dist_bck = motor_serial.get_dist_2()
    return dist_bck
def avg_bck():
    avg_dist_bck = sum(DX_bck)/DXlength
    return avg_dist_bck

def sense_r():
    dist_r = motor_serial.get_dist_3()
    return dist_r
def avg_r():
    avg_dist_r = sum(DX_r)/DXlength
    return avg_dist_r

def sense_l():
    dist_l = motor_serial.get_dist_4()
    return dist_l
def avg_l():
    avg_dist_l = sum(DX_l)/DXlength
    return avg_dist_l

def avg_update():    
    # Update sensors' indices of recent values:
    DX_fwd.append(sense_fwd()) # Add most recent value
    DX_fwd.pop(0) # Delete oldest value

    DX_bck.append(sense_bck())
    DX_bck.pop(0)

    DX_r.append(sense_r())
    DX_r.pop(0)

    DX_l.append(sense_l())
    DX_r.pop(0)

# Exec loop
while not motor_serial.shutdown_now:

    avg_update()
    print(sense_fwd(),avg_fwd())

    # Obstacle check
    if avg_fwd() < STOP_DISTANCE:
        print("halt")
        stop_robot(tstep)
    else:
        drive_robot(FORWARDS, tstep)

print("Bye!")