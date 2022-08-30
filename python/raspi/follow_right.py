import imrt_robot_serial
import signal
import time
import sys
import random


LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 140
TURNING_SPEED = 100
STOP_DISTANCE = 25


def stop_robot(duration):

    iterations = int(duration * 10)
    
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)



def drive_robot(direction, duration, l_speed_modifier=1, r_speed_modifier=1):
    
    l_speed = int(DRIVING_SPEED * direction * l_speed_modifier)
    r_speed = int(DRIVING_SPEED * direction * r_speed_modifier)
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(l_speed, r_speed)
        time.sleep(0.10)

def turn_robot(direction, duration):

    speed = TURNING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, -speed)
        time.sleep(0.10)


def calc_speed_modifiers(sensor_left, sensor_right):
    """bestemmer en modifikator for hjul som er lengst unna vegg"""
    if sensor_left < 15:
        r_speed_modifier = 0.7
    elif sensor_left < 20:
        r_speed_modifier = 0.85
    else: 
        r_speed_modifier = 1
    
    if sensor_right < 15:
        l_speed_modifier = 0.7
    elif sensor_right < 20:
        l_speed_modifier = 0.85
    else: 
        l_speed_modifier = 1
    
    return l_speed_modifier, r_speed_modifier








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


turn_timer = 0
time.sleep(3)
print("sleep for 3")


# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :

    sensor_rfwd = motor_serial.get_dist_1() 
    sensor_lfwd = motor_serial.get_dist_2()
    sensor_right = motor_serial.get_dist_3()
    sensor_left = motor_serial.get_dist_4()

    l_speed_modifier, r_speed_modifier = calc_speed_modifiers(sensor_left, sensor_right)

    print("turn timer:", turn_timer)

    # Kjøre fremover
    if sensor_rfwd < 15 or sensor_lfwd < 15:
        turn_timer = -1
        #stop_robot(1)
        if sensor_right > sensor_left*2:
            turn_robot(RIGHT,1.7)
        else:
            turn_robot(LEFT, 1.7)

    


    # svinge inn i åpning høyre
    elif turn_timer == 0:
        turn_robot(RIGHT,1.7)
        turn_timer -= 1

    # se åpning høyre
    elif sensor_right > 60 and turn_timer<=-6:
        turn_timer = 6      


    # unngå høyre vegg
    elif sensor_right < 10:
        turn_robot(LEFT,0.3)
        drive_robot(FORWARDS, 0.2)

    # unngå venstre vegg
    elif sensor_left < 10:
        turn_robot(RIGHT, 0.3)
        drive_robot(FORWARDS, 0.2)

    # kjør rett frem
    else: 
        # ikke snu om glippe
        if 0 < turn_timer < 2 and sensor_right < 60:
            turn_timer = -1

        turn_timer = turn_timer - 1
        drive_robot(FORWARDS, 0.2, l_speed_modifier, r_speed_modifier)



# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
print("I don't hate you")

