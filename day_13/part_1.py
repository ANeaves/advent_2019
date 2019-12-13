import sys
import logging
from enum import Enum
from intcode_computer import IntcodeComputer


class cabinet_tiles(Enum):
    empty = 0
    wall = 1
    block = 2
    hor_padd = 3
    ball = 4


class Cabinet():

    def __init__(self, file_name):

        self.cpu = IntcodeComputer(name="cpu")
        self.cpu.set_output_method(self.handle_output)
        self.cpu.get_code_from_file(file_name)
        self.outputs = []
        self.screen = {}

    def play(self):
        self.cpu.run()

    def handle_output(self, output):
        self.outputs.append(output)

        if len(self.outputs) == 3:
            x = self.outputs[0]
            y = self.outputs[1]
            self.screen[(x, y)] = cabinet_tiles(self.outputs[2])
            self.outputs = []


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]
    game = Cabinet(file_name)
    game.play()
    logging.debug(game.screen)
    block_list = []
    for key in game.screen:
        if game.screen[key] == cabinet_tiles.block:
            block_list.append(key)
    logging.info("Num Block Tiles: %d", len(block_list))