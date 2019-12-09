from intcode_computer import IntcodeComputer
import logging
import sys
from itertools import permutations


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]

    with open(file_name) as f:
        data = f.read()
        logging.debug(data)
        data = [int(x) for x in data.split(',')]

    amplifiers = [
        IntcodeComputer(data, name="A"),
        IntcodeComputer(data, name="B"),
        IntcodeComputer(data, name="C"),
        IntcodeComputer(data, name="D"),
        IntcodeComputer(data, name="E"),
    ]
    logging.debug([x.output for x in amplifiers])
    all_phase_permutations = list(permutations([0,1,2,3,4]))
    logging.debug(all_phase_permutations)

    all_outputs = []
    for permutation in all_phase_permutations:
        logging.info("TRYING PERMUTATION: %s", permutation)
        current_output = 0
        for phase, computer in list(zip(permutation, amplifiers)):
            computer.set_input(phase)
            computer.set_input(current_output)
            computer.run()
            current_output = computer.output
        all_outputs.append(current_output)
        for computer in amplifiers:
            computer.reset_memory()

    logging.debug(all_outputs)
    logging.info("MAX OUTPUT: %d", max(all_outputs))
