import sys
from intcode_computer import IntcodeComputer
import logging

output_list = []

def output(output):
    logging.info("OUTPUT: %d", output)
    output_list.append(output)

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]

    with open(file_name) as f:
        data = f.read()
        logging.debug(data)
        data = [int(x) for x in data.split(',')]

    computer = IntcodeComputer(data, output_method=output, name="Day 9")
    computer.set_input(2)
    computer.run()

    logging.info(output_list)