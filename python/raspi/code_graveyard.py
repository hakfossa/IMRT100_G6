#code graveyard

def left_too_close():
    return avg_l() < 10


def rigth_too_close():
    return avg_r() < 10


def avoid_wall(right):
    duration = 1
    drive_robot(BACKWARDS, duration)
    
    if right:
        turn_robot(RIGHT, duration)
    else:
        turn_robot(LEFT, duration)

