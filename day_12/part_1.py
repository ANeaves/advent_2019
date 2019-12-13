import logging
import sys


class moon():

    def __init__(self, position):
        self.position = position
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

    def calc_energy(self):

        pot_energy = sum(abs(val) for val in self.position)
        kin_energy = sum(abs(val) for val in self.velocity)
        logging.debug("Potential Energy: %d, Kinetic Energy: %d", pot_energy, kin_energy)
        return pot_energy * kin_energy


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    test_data = [[-1, 0, 2], [2, -10, -7], [4, -8, 8], [3, 5, -1]]

    actual_data = [[0, 4, 0], [-10, -6, -14], [9, -16, -3], [6, -1, 2]]

    if sys.argv[1] == "test":
        use_data = test_data
    else:
        use_data = actual_data

    num_steps = int(sys.argv[2])
    moons = []
    for moon_start in use_data:
        moons.append(moon(moon_start))

    time_step = 0
    for time_step in range(num_steps):
        logging.debug("After %d Steps:", time_step)
        for moon in moons:
            moon_pos = moon.position
            moon_vel = moon.velocity
            logging.debug("pos=<x=%3d, y=%3d, z=%3d> vel=<x=%3d, y=%3d, z=%3d>", moon_pos[0], moon_pos[1], moon_pos[2], moon_vel[0], moon_vel[1], moon_vel[2])
            for other_moon in moons:
                if other_moon is not moon:
                    moon.calc_velocity(other_moon)
        for moon in moons:
            moon.calc_position()

    total_energy = 0
    for moon in moons:
        total_energy += moon.calc_energy()

    logging.info("Total Energy after %d steps: %d", time_step, total_energy)