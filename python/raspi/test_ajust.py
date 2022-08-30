import imrt_robot_serial
import signal
import time
import sys
import random

TURNING_SPEED = 100
LEFT = -1
RIGHT = 1


def turn_robot(direction, duration):

    speed = TURNING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, -speed)
        time.sleep(0.10)



def ajust_90deg(sens_lfwd, sens_rfwd):
    diff_fwd = abs(sens_rfwd-sens_lfwd)
    print("diff_fwd:", diff_fwd)

    if diff_fwd > 60:
        # dersom kun ser noe på en sensor forran, snu 90
        if sens_rfwd > sens_rfwd:
            turn_robot(RIGHT, 1.0)
        else:
            turn_robot(LEFT, 1.0)

        print("wallavoid completed")

    else:
        # juster til 90 grader på vegg
        while diff_fwd < 2:
            if sens_lfwd > sens_rfwd:
                turn_robot(RIGHT, 0.1)
                print("turned right")
            elif sens_lfwd < sens_rfwd:
                turn_robot(LEFT, 0.1)
                print("turned left")
            else:
                print("in else")
                pass
            
            sens_rfwd = motor_serial.get_dist_1() 
            sens_lfwd = motor_serial.get_dist_2()

            diff_fwd = abs(sens_rfwd-sens_lfwd)

        print("Incremental ajust complete")
    


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

print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :
    sensor_rfwd = motor_serial.get_dist_1() 
    sensor_lfwd = motor_serial.get_dist_2()

    print(sensor_lfwd, sensor_rfwd)

    if sensor_lfwd < 15 or sensor_rfwd < 15:
        ajust_90deg(sensor_lfwd, sensor_rfwd)



print("I dont hate you")