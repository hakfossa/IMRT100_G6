import sys
import keyboard  # using module keyboard

running = True
while running:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            print("Stopping robot")
            #stop_robot()
            print("Terminating program")
            sys.exit()
