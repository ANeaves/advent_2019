# day 6, part 1: orbit checksum

# and input of AAA)BBB means "BBB is in orbit around AAA"
import logging
import sys

class ObjectInSpace(object):  # too complex? Maybe so

    def __init__(self, name, orbital_parent=None):
        logging.debug("CREATING BODY %s", name)
        if orbital_parent:
            self.parent = orbital_parent
            self.orbit_count = self.parent.orbit_count + 1
        else:
            self.parent = None
            self.orbit_count = 0
        self.name = name
    
    def __str__(self):
        return "{} ORBITING {}".format(self.name, self.parent.name)

    def __repr__(self):
        return self.__str__()
    
    def assign_parent(self, parent):
        self.parent = parent
        self.orbit_count = parent + 1

    def recalc_orbit(self):
        logging.debug("RECALC FOR %s", self.name)
        


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]
    dict_of_bodies = {}

    # with open(file_name) as f:
    #     for line in f:
    #         parent, body = line.strip().split(')')
    #         if parent not in dict_of_bodies:
    #             dict_of_bodies[parent] = ObjectInSpace(parent)
    #         dict_of_bodies[body] = ObjectInSpace(body, dict_of_bodies[parent])
    # logging.debug(dict_of_bodies.keys())

    with open(file_name) as f:
        for line in f:
            parent, body = line.strip().split(')')
            dict_of_bodies[body] = parent
    
    logging.debug(dict_of_bodies)
    total = 0
    for body in dict_of_bodies:
        while body in dict_of_bodies:
            total += 1
            body = dict_of_bodies[body]
    # for key in dict_of_bodies:
    #     dict_of_bodies[key].recalc_orbit()
    #     total += dict_of_bodies[key].orbit_count
    logging.info("TOTAL ORBITS: %d", total)

    # PART THE SECOND
    you_parent = dict_of_bodies["YOU"]
    santa_parent = dict_of_bodies['SAN']

    you_path = []
    santa_path = []
    # GET YOUR PATH TO COM
    while you_parent in dict_of_bodies:
        you_path.append(you_parent)
        you_parent = dict_of_bodies[you_parent]

    while santa_parent in dict_of_bodies:
        santa_path.append(santa_parent)
        santa_parent = dict_of_bodies[santa_parent]
        
    logging.debug("YOU PATH: %s", you_path)
    logging.debug("SANTA PATH: %s", santa_path)

    total_path = list(set(you_path).symmetric_difference(santa_path))
    logging.debug("TOTAL PATH: %s", total_path)
    logging.debug("LENGTH TO SANTA: %d", len(total_path))
