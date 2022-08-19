class Intersection():

    def __init__(self, previous, oriented_sensor_output, mazewidth):

        self.previous = previous
        self.branches_open = []
        self.check_open(oriented_sensor_output, mazewidth)

        self.dead_end = False 


    def check_open(self, oriented_sensor_output, mazewidth):

        direction = 0
        for distance in oriented_sensor_output:
            if distance > mazewidth *0.8:
                self.branches_open.append(True)
            else: 
                self.branches_open.append(False)
            
            direction += 1

    def print_branches(self):
        print(self.branches_open)


if __name__=="__main__":
    
    mazewidth = 300
    
    oriented_sensor_output = [150, 450, 233, 50]
    intersection = Intersection(None, oriented_sensor_output, mazewidth)
    intersection.print_branches()
