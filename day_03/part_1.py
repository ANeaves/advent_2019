import logging
import sys

class wire(object):

    def __init__(self, path):
        """Follow the path, work out all the grid spaces occupied by this wire"""
        if isinstance(path, str):
            path = path.split(',')
        self.spaces = []

        current_pos = [0, 0]  # [x, y], y is horizontal, up, right are positive moves
        for path_part in path:
            direct = path_part[0]
            path_part = path_part.strip(direct)
            dist = int(path_part)
            logging.debug("%s: %d", direct, dist)
            
            if direct == "U":  # Up
                new_pos = [current_pos[0], current_pos[1] + dist]
                for i in range(current_pos[1], new_pos[1]):
                    self.spaces.append((current_pos[0], i))
            elif direct == "D":  # Down
                new_pos = [current_pos[0], current_pos[1] - dist]
                for i in range(new_pos[1], current_pos[1]):
                    self.spaces.append((current_pos[0], i))
            elif direct == "L":  # left
                new_pos = [current_pos[0] - dist, current_pos[1]]
                for i in range(new_pos[0], current_pos[0]):
                    self.spaces.append((i, current_pos[1]))
            elif direct == "R": # Right
                new_pos = [current_pos[0] + dist, current_pos[1]]
                for i in range(current_pos[0], new_pos[0]):
                    self.spaces.append((i, current_pos[1]))
            else:
                logging.error("DIRECTION NOT VALID: %s", direct)
                return
            current_pos = new_pos
        
        self.spaces = set(self.spaces)    
        logging.info("WIRE COMPLETE")
        logging.info("FINAL WIRE COORD: %s", current_pos)
        logging.debug("TOTAL WIRE POSITIONS: %s", self.spaces)
        logging.info("WIRE SPACES LENGTH: %d", len(self.spaces))


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    file_path = sys.argv[1]
    with open(file_path) as f:
        wire_paths = [line.split(',') for line in f]
    
    wires = []
    for path in wire_paths:
        wires.append(wire(path))

    # intersections = [x for x in wires[0].spaces if x in wires[1].spaces]
    intersections = set(wires[0].spaces).intersection(wires[1].spaces)
    # intersections.remove((0,0))
    logging.info("NUM INTERSECTIONS: %d", len(intersections))

    distances = []
    for intersect in intersections:
        distances.append(abs(intersect[0]) + abs(intersect[1]))

    logging.info("CLOSEST DISTANCE: %d", min(distances))
