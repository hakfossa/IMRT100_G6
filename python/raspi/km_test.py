# Py Modules
from re import A
import signal
import time
import sys
import random
import math
from turtle import width

# Homebrew modules
import imrt_robot_serial
import imrt_connect

# Globals
LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 50
TURNING_SPEED = 100
STOP_DISTANCE = 25
ROBOT_WIDTH = 0.40 # metres

tfreq = 10 # Timer Frequency, Execution frequency in Hz
tstep = 1/tfreq # Timer Step length

###########################################
#   _____                                 #
#  /  ___|                                #
#  \ `--.  ___ _ __  ___  ___  _ __ ___   #
#   `--. \/ _ \ '_ \/ __|/ _ \| '__/ __|  #
#  /\__/ /  __/ | | \__ \ (_) | |  \__ \  #
#  \____/ \___|_| |_|___/\___/|_|  |___/  #
#                                         #
# v v v v v v v v v v v v v v v v v v v v #
###########################################

# Setup buffers for recent average smoothing of sensor data.
DX_fwd = []
DX_bck = []
DX_r = []
DX_l = []

# Setup buffers for tracking increase/decrease in sensor data.
change_fwd = []
change_bck = []
change_r = []
change_l = []

# Setup how many recordings should be kept in memory at once.
# Recordings happen once every tstep miliseconds.
# A higher value means more dampening over longer time.
# DXlength is for the buffer dealing with sensor data smoothing,
# chgbuffer_length is the buffer dealing with changes in sensor data.
# 
# Effectively the latter has this parameter for "how long ago do I
# compare the current data with to see if stuff is changing", 10=1s.
DXlength = 20
chgbuffer_length = 10

# We accept X units as error before assuming a change has happened.
changethresh = 3

# Go through the buffers and give them an appropriate amount of nothing
sensor_list = [DX_fwd,DX_bck,DX_r,DX_l]
for sensor in sensor_list:
    for i in range(DXlength):
        sensor.append(255)
chgbuffer_list = [change_fwd,change_bck,change_r,change_l]
for buffer in chgbuffer_list:
    for i in range(chgbuffer_length):
        buffer.append(255)
print("Buffers filled with gibberish.")

# Functions that retrieve sensor data:
def sense_fwd():
    dist_fwd = motor_serial.get_dist_1()
    return dist_fwd
def sense_bck():
    dist_bck = motor_serial.get_dist_2()
    return dist_bck
def sense_r():
    dist_r = motor_serial.get_dist_3()
    return dist_r
def sense_l():
    dist_l = motor_serial.get_dist_4()
    return dist_l

# Functions that output dampened (= recent average of) sensor data:
def avg_fwd():
    avg_dist_fwd = sum(DX_fwd)/DXlength
    return avg_dist_fwd
def avg_bck():
    avg_dist_bck = sum(DX_bck)/DXlength
    return avg_dist_bck
def avg_r():
    avg_dist_r = sum(DX_r)/DXlength
    return avg_dist_r
def avg_l():
    avg_dist_l = sum(DX_l)/DXlength
    return avg_dist_l

# Functions that check for change in the dampened sensor data:
def chg_fwd():
    chg_fwd = change_fwd[chgbuffer_length-1] - change_fwd[0] # Now vs X ms ago
    if abs(chg_fwd) < changethresh: # Tiny changes are sensor fluctuation and we disregard them
        chg_fwd = 0
    return chg_fwd

def chg_bck():
    chg_bck = change_bck[chgbuffer_length-1] - change_bck[0]
    if abs(chg_bck) < changethresh:
        chg_bck = 0
    return chg_bck

def chg_r():
    chg_r = change_r[chgbuffer_length-1] - change_r[0]
    if abs(chg_r) < changethresh:
        chg_r = 0
    return chg_r

def chg_l():
    chg_l = change_l[chgbuffer_length-1] - change_l[0]
    if abs(chg_l) < changethresh:
        chg_l = 0
    return chg_l

# Function that tells us if the magnitude of something is 1/0/-1,
# intended for checking magnitude of change but really it'll take whatever
def magnitude(arg):
    if arg > 0:
        magnitude = 1
    elif arg == 0:
        magnitude = 0
    else:
        magnitude = -1
    return magnitude

# Threshold for scrapping data on its way into the average, set to higher
# than our sensor range because coding this as badly as I did was a mistake.
# Effectively its function is to neutralize spaghetti code.
avg_threshold = 300

# Function that updates the change-in-dampened-data buffer
def change_update():
    change_fwd.append(avg_fwd())    # Add newest value
    change_fwd.pop(0)               # Wipe oldest value
    change_bck.append(avg_bck())
    change_bck.pop(0)
    change_r.append(avg_r())
    change_r.pop(0)
    change_l.append(avg_l())
    change_l.pop(0)


# Function that updates the dampening buffers
def avg_update():    
    current_fwd = sense_fwd()
    # If the difference between value and previous avg is more than x,
    # discard newest value and repeat 2nd most recent value instead.
    # 
    # This function is disabled via avg_threshold>255, which again is
    # on purpose because it kind of sucked ass and broke the dampening.
    if abs((sum(DX_fwd)/DXlength) - current_fwd) < avg_threshold:
        DX_fwd.append(current_fwd)
    else:
        DX_fwd.append(DX_fwd[DXlength-1])
        print("FWD scrapped from average")
    DX_fwd.pop(0)

    current_bck = sense_bck()
    if abs((sum(DX_bck)/DXlength) - current_bck) < avg_threshold:
        DX_bck.append(current_bck)
    else:
        DX_bck.append(DX_bck[DXlength-1])
        print("BCK scrapped from average")
    DX_bck.pop(0)

    current_r = sense_r()
    if abs((sum(DX_r)/DXlength) - current_r) < avg_threshold:
        DX_r.append(current_r)
    else:
        DX_r.append(DX_r[DXlength-1])
        print("R scrapped from average")
    DX_r.pop(0)

    current_l = sense_l()
    if abs((sum(DX_l)/DXlength) - current_l) < avg_threshold:
            DX_l.append(current_l)
    else:
        DX_l.append(DX_l[DXlength-1])
        print("L scrapped from average")
    DX_l.pop(0)



#####################################
#  ___  ___      _                  #
#  |  \/  |     | |                 #
#  | .  . | ___ | |_ ___  _ __ ___  #
#  | |\/| |/ _ \| __/ _ \| '__/ __| #
#  | |  | | (_) | || (_) | |  \__ \ #
#  \_|  |_/\___/ \__\___/|_|  |___/ #
#                                   #
# v v v v v v v v v v v v v v v v v #
#####################################

# !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! #
# The 1st motor in the motor_serial commands is the LEFT, the 2nd is the RIGHT. #
# !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! !! #

# Functions that make the robot go places
def stop_robot(duration):
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(0,0)
        time.sleep(tstep)

def drive_robot(direction, duration):
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed,speed)
        time.sleep(tstep)

def turn_robot(direction, duration):
    motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
    time.sleep(tstep)

# Drive centered

# Take inputs from either side, compare them.
# If they're equidistant within a margin, you're OK;
# check change on each, adjust motor balance to 

def drive_centered(direction, duration):
    speed = DRIVING_SPEED * direction
    iterations = int(duration*10)
    for i in range(iterations):
        l_coeff = int((avg_r()/avg_l())*10)
        r_coeff = int((avg_l()/avg_r())*10)
        motor_serial.send_command(l_coeff + speed, r_coeff + speed)
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

# Main loop
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now:

    avg_update()
    change_update()

#    print("aFWD:",round(avg_fwd()),"chg_fwd:",round(chg_fwd(),1),"magnitude.chg_fwd:",magnitude(chg_fwd()))

#    print(" FWD:",round(sense_fwd(),1),"BCK:",round(sense_bck(),1),"R:",(round(sense_r(),1),"L:",round(sense_l(),1)))
#    print("aFWD:",round(avg_fwd(),1),"aBCK:",round(avg_bck(),1),"aR:",round(avg_r(),1),"aL:",round(avg_l(),1))

    # Obstacle check
    if sense_fwd() < STOP_DISTANCE:
        print("Holding")
        stop_robot(tstep)
    else:
        print("Driving")
        drive_centered(FORWARDS, tstep)

print("Bye!")