import sys
import logging
from intcode_computer import IntcodeComputer

class AsciiComputer(IntcodeComputer):

    def __init__(self):
        super().__init__()
        self.output_string = ''
        self.output_method = self.handle_ascii_output
    
    def handle_ascii_output(self, output):
        self.output_string += str(chr(output))

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]
    ascii_pc = AsciiComputer()
    ascii_pc.get_code_from_file(file_name)
    ascii_pc.run()
    print(ascii_pc.output_string)