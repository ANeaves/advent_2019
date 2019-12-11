# OH GODS HOW DO LINE OF SIGHT STUFF?
import logging
import sys
import math
import operator

def get_angle(source_coord, target_coord):
    # something something use maths?
    src_x, src_y = source_coord
    tgt_x, tgt_y = target_coord
    return math.degrees(math.atan2(tgt_y-src_y, tgt_x-src_x))

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]

    asteroids = {}
    x = 0
    y = 0
    with open(file_name) as f:
        for line in f:
            for char in line.strip():
                if char == '#':
                    asteroids[(x, y)] = []
                x += 1
            x = 0
            y += 1
            
    logging.debug("Asteroids: %s", asteroids)

    for asteroid in asteroids:
        for other_asteroid in asteroids:
            if asteroid != other_asteroid:
                angle = get_angle(asteroid, other_asteroid)
                if angle not in asteroids[asteroid]:
                    asteroids[asteroid].append(angle)
    
    logging.debug(asteroids)
    lengths = []
    for key in asteroids:
        lengths.append(len(asteroids[key]))
    logging.info("Max visable: %d", max(lengths))
