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

imrt_connect.handshake()

# Exec loop?
while not motor_serial.shutdown_now:
    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    print("Dist 1:", dist_1, "   Dist 2:", dist_2)

    # Check if there is an obstacle in the way
    if dist_1 < STOP_DISTANCE or dist_2 < STOP_DISTANCE:
        # There is an obstacle in front of the robot
        # First let's stop the robot for 1 second
        print("Obstacle!")
        stop_robot(1)

        # Reverse for 0.5 second
        drive_robot(BACKWARDS, 0.5)

        # Turn random angle
        turn_robot_random_angle()
        

    else:
        # If there is nothing in front of the robot it continus driving forwards
        drive_robot(FORWARDS, 0.1)

print("Bye!")