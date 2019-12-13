import sys
import logging
from intcode_computer import IntcodeComputer
from collections import defaultdict
from operator import itemgetter
from copy import deepcopy

class Bot():

    def __init__(self, file_name, start_input):
        self.brain = IntcodeComputer(output_method=self.handle_output, name="bot_brain")
        self.brain.get_code_from_file(file_name)
        # DIRECTIONS:      up       right    down     left
        self.directions = [(0, -1), (+1, 0), (0, +1), (-1, 0)]
        self.brain.set_input(int(start_input))  # start on a WHITE panel for part 2
        self.current_direction = 0
        self.position = (0, 0)
        self.painted_panels = defaultdict(int)
        self.output_state = "color"

    def handle_output(self, output):
        if self.output_state == "color":
            self.painted_panels[self.position] = output
            self.output_state = "rotation"
            logging.info("TILE %s coloured %d", self.position, output)
        else:
            if output == 0:
                logging.debug("Bot rotating LEFT")
                # rotate left
                output = -1
            else:
                #rotate right
                logging.debug("Bot rotating RIGHT")
            self.current_direction = (self.current_direction + output) % len(self.directions)
            logging.debug("Current Direction: %d", self.current_direction)
            self.position = tuple(a+b for a, b, in zip(self.position, self.directions[self.current_direction]))
            self.brain.set_input(self.painted_panels[self.position])
            self.output_state = "color"
            logging.debug("Bot Moved to %s", self.position)
            logging.debug("Inputting %d to bot", self.painted_panels[self.position])

    def run_bot(self):
        self.brain.run()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]
    start_input = sys.argv[2]

    bot = Bot(file_name, start_input)
    bot.run_bot()
    logging.info("Bot painted %d tiles", len(bot.painted_panels))
    logging.debug(bot.painted_panels)
    coords = sorted(list(bot.painted_panels))
    max_x = max(coords, key=itemgetter(0))[0]
    min_x = min(coords, key=itemgetter(0))[0]
    max_y = max(coords, key=itemgetter(1))[1]
    min_y = min(coords, key=itemgetter(1))[1]
    logging.debug("Top left coord: %s", (min_x, min_y))
    logging.debug("Bottom Right Coord: %s", (max_x, max_y))

    for y in range(min_y, max_y + 1):
        row = ''
        for x in range(min_x, max_x):
            paint = ' ' if bot.painted_panels[(x, y)] == 0 else '█'
            row = row + paint
        logging.info(row)


