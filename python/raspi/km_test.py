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
    for i in range(DXLength):
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
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

# Start serial receive thread
motor_serial.run()

# Defining a function that retrieves sensor data and updates the time avg. array for each sensor
def sense():
    # Sensor outputs
    dist_fwd = motor_serial.get_dist_1()
    dist_back = motor_serial.get_dist_2()
    dist_r = motor_serial.get_dist_3()
    dist_l = motor_serial.get_dist_4()
    print("fwd:", dist_fwd, "bck:", dist_back, "R:", dist_r, "L:", dist_l)
    
    # Update sensors' indices of recent values:
    DX_fwd.append(dist_fwd) # Add most recent value
    DX_fwd.pop(0) # Delete oldest value

    DX_bck.append(dist_back)
    DX_bck.pop(0)

    DX_r.append(dist_r)
    DX_r.pop(0)

    DX_l.append(dist_l)
    DX_r.pop(0)

    # Extract instantaneous values
    DXv_fwd = sum(DX_fwd)/DXlength
    DXv_bck = sum(DX_bck)/DXlength
    DXv_r = sum(DX_r)/DXlength
    DXv_l = sum(DX_l)/DXlength
    print("DXv_fwd:",DXv_fwd,"DXv_bck:",DXv_bck,"DXv_r:",DXv_r,"DXv_l:",DXv_l)

# Exec loop
while not motor_serial.shutdown_now:

    sense()

    # Obstacle check
    if DXv_fwd < STOP_DISTANCE:
        print("halt")
        stop_robot(tstep)
    else:
        drive_robot(FORWARDS, tstep)

print("Bye!")