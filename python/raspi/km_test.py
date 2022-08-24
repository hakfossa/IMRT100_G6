# Py Modules
from re import A
import signal
import time
import sys
import random
from turtle import width

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
sensor_list = [DX_fwd,DX_bck,DX_r,DX_l]
for sensor in sensor_list:
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

# Threshold for scrapping data on its way into the average, in approximate cm*s^-1
avg_threshold = 160

# Update indices for recent values
def avg_update():    
    current_fwd = sense_fwd()
    # If diff between value and previous avg is more than x,
    # discard newest value and repeat 2nd most recent value instead.
    if abs((sum(DX_fwd)/DXlength) - current_fwd) < avg_threshold:
            DX_fwd.append(current_fwd)
    else:
        DX_fwd.append(DX_fwd[DXlength-1])
        print("FWD scrapped from average")
    DX_fwd.pop(0) # Delete oldest value

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

# Scrapped plotter
#
# plotwidth = 8
# plotheight = 10
# plotgrid = []
#
# def plotsensors():
#    print(sense_fwd()/25)
#    for x in range(plotwidth):
#        row = []
#        for y in range(plotheight):
#            if y < (sense_fwd()/20):
#                row.append('#')
#            elif 1 < x < 3 and (plotheight-2) < y < plotheight:
#                row.append(sense_fwd())
#            else: row.append(' ')
#        plotgrid.append(row)
#     plotthis = ''
#    for y in reversed(range(plotheight)):
#        plotline=''
#        for x in range(plotwidth):
#            plotline = plotline+str(plotgrid[x][y])
#        plotthis = plotthis+plotline+'\n'
#    print(plotthis)


# Exec loop
while not motor_serial.shutdown_now:

    avg_update()
    sense_fwd()

    print(sense_fwd(),sense_bck(),sense_r(),sense_l())
    print("avges,",DXlength,"times timestep memory:",avg_fwd(),avg_bck(),avg_r(),avg_l())

    # Obstacle check
    if avg_fwd() < STOP_DISTANCE:
        print("halt")
        stop_robot(tstep)
    else:
        drive_robot(FORWARDS, tstep)

print("Bye!")