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



def get_distances():
    distances = [avg_fwd(), avg_r(), avg_bck(), avg_l()]
    return distances

def rotate_distances(right: bool):
    distances = get_distances()

    if right:
        rotated_dist = distances[:3]
        rotated_dist.insert(0, distances[-1])
    if not right:
        rotated_dist = distances[1:]
        rotated_dist.append(distances[0])

    return rotated_dist


def compare_distances(rotated_dist):
    sensor_inputs = [sense_fwd(), sense_r(), sense_bck(), sense_l()]
    correct = 0
    for i in range(len(sensor_inputs)):
        if abs(sensor_inputs[i]-rotated_dist[i]) < 15:
            correct += 1

    if correct >= 3:
        TURNING_L = False
        TURNING_R = False


""" 
def shortest_dist(right):
    distances = [avg_fwd(), avg_r(), avg_bck(), avg_l()]
    min_val = min(distances)
    index = distances.index(min_val)
    if right:
        index -= 1
        if index < 0:
            index = 3
    if not right:
        index += 1
        if index > 3:
            index = 0

    return index

def check_change """



""" def check_turn_l():
    if chg_l() > 10 or ORIGINAL_FWD - sense_r() < 5:
        TURNING_L = True
    else:
        TURNING_L = False

def check_turn_r():
    if chg_r() > 10 or ORIGINAL_FWD - sense_l() < 5:
        TURNING_R = True
    else:
        TURNING_R = False """

