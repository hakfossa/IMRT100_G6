

sensor_input = [10,21,32,11]
orientation = 1

def orient_sensor_input(sensor_input, orientation):
    "Change the list based on orientation of robot"
    oriented_output = []
    ori_modifier = orientation

    while len(oriented_output) < 4:
        oriented_output.append(sensor_input[ori_modifier])
        ori_modifier += 1

        if ori_modifier > 3:
            ori_modifier = 0
    
    return oriented_output


    
for orientation in range(4):
    print(orient_sensor_input(sensor_input, orientation))
