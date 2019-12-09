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
        IntcodeComputer(data, name="A", is_async=True),
        IntcodeComputer(data, name="B", is_async=True),
        IntcodeComputer(data, name="C", is_async=True),
        IntcodeComputer(data, name="D", is_async=True),
        IntcodeComputer(data, name="E", is_async=True),
    ]
    # SET OUTPUT METHOD AS INPUT TO QUEUE OF NEXT AMPLIFIER
    amplifiers[0].set_output_method(amplifiers[1].set_input)
    amplifiers[1].set_output_method(amplifiers[2].set_input)
    amplifiers[2].set_output_method(amplifiers[3].set_input)
    amplifiers[3].set_output_method(amplifiers[4].set_input)
    amplifiers[4].set_output_method(amplifiers[0].set_input)

    logging.debug([x.output for x in amplifiers])
    all_phase_permutations = list(permutations([5, 6, 7, 8, 9]))
    logging.debug(all_phase_permutations)


    all_outputs = []
    for permutation in all_phase_permutations:
        logging.info("TRYING PERMUTATION: %s", permutation)
        for phase, computer in list(zip(permutation, amplifiers)):
            computer.set_input(phase)
            if computer.name == "A":
                computer.set_input(0)
            # computer.run()  # THIS WILL RUN IN THREAD
        for computer in amplifiers:
            computer.run()

        for computer in amplifiers:
            computer.thread.join()
        all_outputs.append(amplifiers[4].output)
        for computer in amplifiers:
            computer.reset_memory()

    logging.debug("ALL OUTPUTS: %s", all_outputs)
    logging.info("MAX OUTPUT: %d", max(all_outputs))

