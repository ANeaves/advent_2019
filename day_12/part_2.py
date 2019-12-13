import logging
import sys
from math import gcd
from copy import deepcopy
import time

class moon():

    def __init__(self, position):
        self.position = position
        self.inital_position = deepcopy(position)
        self.velocity = [0, 0, 0]

    def calc_velocity(self, other_moon):
        other_pos = other_moon.position

        for index in range(len(self.velocity)):
            if self.position[index] < other_pos[index]:
                self.velocity[index] += 1
            elif self.position[index] > other_pos[index]:
                self.velocity[index] -= 1

    def calc_position(self):
        for index in range(len(self.position)):
            self.position[index] += self.velocity[index]



if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    test_data = [[-1, 0, 2], [2, -10, -7], [4, -8, 8], [3, 5, -1]]
    # test_data = [[-8, -10, 0], [5, 5, 10], [2, -7, 3], [9, -8, -3]]

    actual_data = [[0, 4, 0], [-10, -6, -14], [9, -16, -3], [6, -1, 2]]

    if sys.argv[1] == "test":
        use_data = test_data
    else:
        use_data = actual_data

    # num_steps = int(sys.argv[2])
    moons = []
    for moon_start in use_data:
        moons.append(moon(moon_start))

    time_step = 0
    found_loops = [None] * 3
    while True:
        logging.debug("After %d Steps:", time_step)

        for moon in moons:
            for other_moon in moons:
                if other_moon is not moon:
                    moon.calc_velocity(other_moon)
        for moon in moons:
            moon.calc_position()

        time_step += 1

        for index, loop in enumerate(found_loops):
            match_list = []
            if not loop:
                # logging.debug("Checking loop %d", index)
                for moon in moons:
                    # if moon is in same state as at start (same position, no velocity) add to list
                    moon_same_state =  moon.velocity[index] == 0
                    # logging.debug("Moon same state: %s", moon_same_state)
                    match_list.append(moon_same_state)
                if all(match_list):
                    found_loops[index] = time_step
                    logging.debug("Found loop at step %d TIME FOR A REALLY LONG LINE SO WE SEE THIS WIZZ PAST", time_step)
                    time.sleep(1)
        if all(found_loops):
            break
    logging.debug("Loops for each: %s", found_loops)
