import logging
import sys
from ascii_computer import AsciiComputer

def get_cross_coords(scaf_str):
    # convert to lists?
    line_list = scaf_str.split('\n')
    coord_list = []
    for y, line in enumerate(line_list):
        for x, char in enumerate(line):
            if char == '#':
                # logging.debug("# found at coord (%d, %d)", x, y)
                try:
                    u = line_list[y-1][x]
                    d = line_list[y+1][x]
                    l = line_list[y][x-1]
                    r = line_list[y][x+1]
                    # logging.debug("u: %s, d %s, l: %s, r: %s", u, d, l, r)
                    if all([u == '#', d == '#', l == '#', r == '#']):
                        coord_list.append((x, y))
                except IndexError:
                    pass
    return coord_list

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]
    ascii_pc = AsciiComputer()
    ascii_pc.get_code_from_file(file_name)
    ascii_pc.run()
    print(ascii_pc.output_string)
    cross_points = get_cross_coords(ascii_pc.output_string)
    logging.debug(cross_points)
    total = 0
    for point in cross_points:
        total += (point[0] * point[1])
    logging.info("Total Alignment Params: %d", total)