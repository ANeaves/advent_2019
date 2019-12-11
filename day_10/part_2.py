# OH GODS HOW DO LINE OF SIGHT STUFF?
import logging
import sys
import math
from collections import defaultdict

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
                    asteroids[(x, y)] = {}
                x += 1
            x = 0
            y += 1
            
    # logging.debug("Asteroids: %s", asteroids)

    lengths = {}

    for asteroid in asteroids:
        for other_asteroid in asteroids:
            if asteroid != other_asteroid:
                angle = round(get_angle(asteroid, other_asteroid), 2)
                if angle == 180:
                    angle = -180
                if angle in asteroids[asteroid]:
                    asteroids[asteroid][angle].append(other_asteroid)
                else:
                    asteroids[asteroid][angle] = [other_asteroid]
                
        lengths[len(asteroids[asteroid])] = asteroid
        
    
    # logging.debug(lengths)
    max_visible = max(lengths)
    tgt_asteroid_coord = lengths[max_visible]
    target_asteroid = asteroids[tgt_asteroid_coord]
    all_angles = sorted(target_asteroid.keys())
    logging.info("Max visable: %d", max_visible)
    logging.info("Station based on asteroid: %s", tgt_asteroid_coord)
    logging.info("Target's Angles: %s", all_angles)
    
    # reorder list so it starts at -90?
    index = all_angles.index(-90)
    index -= 1
    destroyed_asteroids = []
    while all_angles:
        index = (index + 1) % len(all_angles)
        angle = all_angles[index]
        logging.debug("%f: %s", angle, target_asteroid[angle])
        if angle < 0:
            remove_index = -1
        else:
            remove_index = 0
        target = target_asteroid[angle].pop(remove_index)
        destroyed_asteroids.append(target)
        if not target_asteroid[angle]:  # if list empty, remove key from all_angles:
            all_angles.pop(index)
            index -= 1

        # index = index + 1
    logging.debug(destroyed_asteroids)
    logging.debug("destroyed asteroid 000: %s", destroyed_asteroids[0])
    logging.debug("destroyed asteroid 001: %s", destroyed_asteroids[1])
    logging.debug("destroyed asteroid 002: %s", destroyed_asteroids[2])
    logging.debug("destroyed asteroid 009: %s", destroyed_asteroids[9])
    logging.debug("destroyed asteroid 019: %s", destroyed_asteroids[19])
    logging.debug("destroyed asteroid 049: %s", destroyed_asteroids[49])
    logging.debug("destroyed asteroid 099: %s", destroyed_asteroids[99])
    logging.debug("destroyed asteroid 198: %s", destroyed_asteroids[198])
    logging.info("200th destroyed asteroid: %s", destroyed_asteroids[199])
    logging.debug("destroyed asteroid 200: %s", destroyed_asteroids[200])
    logging.debug("destroyed asteroid 298: %s", destroyed_asteroids[298])
