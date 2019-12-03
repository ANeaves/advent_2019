import logging
import sys

class wire(object):

    def __init__(self, path):
        """Follow the path, work out all the grid spaces occupied by this wire"""
        if isinstance(path, str):
            path = path.split(',')
        self.spaces = {}

        current_pos = [0, 0]  # [x, y], y is horizontal, up, right are positive moves
        current_length = 0
        for path_part in path:
            direct = path_part[0]
            path_part = path_part.strip(direct)
            dist = int(path_part)
            logging.debug("%s: %d", direct, dist)
            
            if direct == "U":  # Up
                new_pos = [current_pos[0], current_pos[1] + dist]
                for i in range(current_pos[1], new_pos[1]):
                    coord = (current_pos[0], i)
                    if coord not in self.spaces:
                        self.spaces[coord] = current_length
                    current_length += 1
            elif direct == "D":  # Down
                new_pos = [current_pos[0], current_pos[1] - dist]
                for i in range(current_pos[1], new_pos[1], -1):
                    coord = (current_pos[0], i)
                    if coord not in self.spaces:
                        self.spaces[coord] = current_length
                    current_length += 1
            elif direct == "L":  # left
                new_pos = [current_pos[0] - dist, current_pos[1]]
                for i in range(current_pos[0], new_pos[0], -1):
                    coord = (i, current_pos[1])
                    if coord not in self.spaces:
                        self.spaces[coord] = current_length
                    current_length += 1
            elif direct == "R": # Right
                new_pos = [current_pos[0] + dist, current_pos[1]]
                for i in range(current_pos[0], new_pos[0]):
                    coord = (i, current_pos[1])
                    if coord not in self.spaces:
                        self.spaces[coord] = current_length
                    current_length += 1
            else:15678
                logging.error("DIRECTION NOT VALID: %s", direct)
                return
            current_pos = new_pos
        
        self.spaces_set = set(self.spaces.keys())    
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
    intersections.remove((0,0))
    logging.info("NUM INTERSECTIONS: %d", len(intersections))
    logging.info("Example: %s", list(intersections)[0])
    distances = []
    for coord in intersections:
        dist = wires[0].spaces[coord] + wires[1].spaces[coord]
        distances.append(dist)
    logging.info("LOWEST DIST: %d", min(distances))