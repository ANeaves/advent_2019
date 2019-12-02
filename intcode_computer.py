import sys
from copy import deepcopy
import logging
class IntcodeStates():
    idle = 0
    running = 1
    halted = 99

    error = -1

class IntcodeComputer():

    def __init__(self, code=[]):
        self.code = code
        self.memory = deepcopy(self.code)
        self.pointer = 0
        self.state = IntcodeStates.idle

        self.instruction_set = {
            1: (self.add, 3),
            2: (self.mul, 3),
            99: (self.halt, 0)
        }

    def save_code(self, code):
        self.code = code
        self.memory = deepcopy(self.code)

    def reset_memory(self):
        self.memory = deepcopy(self.code)

    def get_code_from_file(self, file_name):
        with open(file_name) as f:
            data = f.read()
            logging.debug(data)
            data = [int(x) for x in data.split(',')]
        self.save_code(data)

    def run(self):
        self.state = IntcodeStates.running
        logging.info("Starting Run")
        while self.state == IntcodeStates.running:
            logging.debug("Current Address: %d", self.pointer)
            try:
                opcode = self.memory[self.pointer]
                instruction, param_count = self.instruction_set[opcode]
                params = self.memory[self.pointer+1:self.pointer+param_count+1]
                instruction(*params)
                self.pointer += 1 + param_count

            except KeyError:
                self.state = IntcodeStates.error
                logging.error("ERROR: Instruction not found: %d", instruction)
            
            except IndexError:
                self.state = IntcodeStates.error
                logging.error("ERROR: Index Out of Bounds")

    def add(self, a, b, out):
        self.memory[out] = self.memory[a] + self.memory[b]

    def mul(self, a, b, out):
        self.memory[out] = self.memory[a] * self.memory[b]

    def halt(self):
        logging.info("Program Complete")
        self.state = IntcodeStates.halted

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    file_name = sys.argv[1]
    computer = IntcodeComputer()
    computer.get_code_from_file(file_name)
    computer.run()
    logging.info("Resulting Memory:\n%s", computer.memory)
