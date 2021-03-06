import sys
from copy import deepcopy
import logging
import threading
from queue import Queue
from collections import defaultdict


class IntcodeStates():
    idle = 0
    running = 1
    halted = 99

    error = -1


class IntcodeComputer():

    def __init__(self, code=[], prog_input=[], name=None, is_async=False, output_method=print):
        logging.info("Creating Intcode Computer V4: Now with Relative Indexing!")
        self.code = code
        # self.memory = deepcopy(self.code)
        self.memory = defaultdict(int)
        self.save_code(self.code)
        self.pointer = 0
        self.state = IntcodeStates.idle
        self.input = Queue()
        for put in prog_input:
            self.input.put(put)
        self.input_count = 0
        self.output = None
        self.output_method = output_method
        self.name = name
        self.is_async = is_async
        self.thread = None

        self.rel_base = 0

        self.instruction_set = {
            1: (self.add, 3, 'ADDI'),
            2: (self.mul, 3, 'MULI'),
            3: (self.put, 1, 'INPT'),
            4: (self.out, 1, 'OUTP'),
            5: (self.jmp_true, 2, "JPNZ"),
            6: (self.jmp_flse, 2, 'JPEZ'),
            7: (self.less, 3, "TLST"),
            8: (self.eql, 3, "TEQT"),
            9: (self.set_base, 1, "BASE"),
            99: (self.halt, 0, "HALT")
        }

        self.show_opcode_debug = True

    def set_input(self, prog_input):
        logging.info("%s SETTING INPUT TO %s", self.name, prog_input)
        if isinstance(prog_input, list):
            for item in prog_input:
                self.input.put(item)
        else:
            self.input.put(prog_input)

    def set_output_method(self, method):
        self.output_method = method

    def save_code(self, code):
        self.code = code
        for index, val in enumerate(self.code):
            self.memory[index] = val

    def reset_memory(self):
        self.save_code(self.code)
        self.pointer = 0
        self.input = Queue()
        self.output = None

    def get_code_from_file(self, file_name):
        with open(file_name) as f:
            data = f.read()
            logging.debug(data)
            data = [int(x) for x in data.split(',')]
        self.save_code(data)

    def run(self):
        # in a thread, or not?
        if self.is_async:
            self.thread = threading.Thread(target=self.__run_prog)
            self.thread.start()
            # run in thread
        else:
            self.__run_prog()

    def __run_prog(self):
        self.state = IntcodeStates.running
        logging.info("Starting Run of %s", self.name)
        while self.state == IntcodeStates.running:
            # logging.debug("Current Address: %d", self.pointer)
            try:
                full_opcode = self.memory[self.pointer]
                opcode = full_opcode % 100
                # logging.debug("OPCODE: %d", opcode)
                instruction, param_count, print_name = self.instruction_set[opcode]
                params = [self.memory[x]for x in range(self.pointer + 1, self.pointer + param_count + 1)]
                param_modes = str(full_opcode)[0:-2].rjust(param_count, '0')
                self.create_debug_code_line(opcode, print_name, params, param_modes)
                instruction(*params, param_modes)
                self.pointer += 1 + param_count

            except KeyError:
                self.state = IntcodeStates.error
                logging.error("ERROR: Instruction not found: %d", instruction)

            except IndexError as err:
                self.state = IntcodeStates.error
                logging.error("ERROR: Index Out of Bounds: %s", err)

    def get_param(self, param, param_mode):

        if param_mode == '1':
            return param
        elif param_mode == '2':
            address = param + self.rel_base
        else:
            address = param
        # logging.debug("RELATIVE ADDRESS: %d", address)
        ret_val =  self.memory[address]
        return ret_val

    def get_params(self, params, param_modes):
        # logging.debug(param_modes)
        param_modes = reversed(param_modes)
        return list(map(self.get_param, params, param_modes))

    # OPCODE METHODS BELOW
    def add(self, a, b, out, param_modes):
        a, b, _ = self.get_params([a, b, out], param_modes)
        if param_modes[0] == '2':
            out = out + self.rel_base
        self.memory[out] = a + b

    def mul(self, a, b, out, param_modes):
        a, b, _ = self.get_params([a, b, out], param_modes)
        if param_modes[0] == '2':
            out = out + self.rel_base
        self.memory[out] = a * b

    def put(self, put_addr, param_modes):
        if param_modes == '2':
            put_addr = put_addr + self.rel_base
        self.memory[put_addr] = self.input.get()

    def out(self, out, param_modes):
        out = self.get_params([out], param_modes)[0]
        self.output = out
        if self.output_method:
            self.output_method(out)

    def jmp_true(self, check, jmp_addr, param_modes):
        check, jmp_addr = self.get_params([check, jmp_addr], param_modes)
        if check:
            self.pointer = jmp_addr - 3  # the minus 3 is to account for the pointer moving at the end of the run loop

    def jmp_flse(self, check, jmp_addr, param_modes):
        check, jmp_addr = self.get_params([check, jmp_addr], param_modes)
        if not check:
            self.pointer = jmp_addr - 3

    def less(self, a, b, out, param_modes):
        a, b, _ = self.get_params([a, b, out], param_modes)
        if param_modes[0] == '2':
            out = out + self.rel_base
        if a < b:
            self.memory[out] = 1
        else:
            self.memory[out] = 0

    def eql(self, a, b, out, param_modes):
        a, b, _ = self.get_params([a, b, out], param_modes)
        if param_modes[0] == '2':
            out = out + self.rel_base
        if a == b:
            self.memory[out] = 1
        else:
            self.memory[out] = 0

    def set_base(self, a, param_modes):
        a = self.get_param(a, param_modes)
        self.rel_base += a

    def halt(self, param_modes):
        logging.info("%2s: Program Complete", self.name)
        self.state = IntcodeStates.halted

    def create_debug_code_line(self, opcode, method_name, params, param_modes):
        print_params = []
        print_line = ''
        if self.name:
            print_line += '[{}] '.format(self.name)
        if self.show_opcode_debug:
            print_line += '{:0>3}/{:0>2}: '.format(param_modes, opcode)

        for param, mode in zip(params, reversed(param_modes)):
            if mode == '1':
                print_params.append(param)
            elif mode == '2':
                addr = self.rel_base + param
                print_params.append('({1})@{0}'.format(addr, self.memory[addr]))
            else:
                print_params.append('({1})@{0}'.format(param, self.memory[param]))

        while len(print_params) < 3:
            print_params.insert(0, '')

        # special cases for special opcodes
        if opcode == 9:  # MODIFYING BASE ADDR
            print_params.pop(0)
            print_params.append(self.rel_base)
            print_params[0] = '[BASE_ADDR]'
        if opcode == 4:  # OUTPUTTING
            print_params.pop(0)
            print_params.append('[OUTPUT]')


        print_line += "{pos:0>4}: {opname} {params[0]:>16}|{params[1]:>16} -> {params[2]:>16}"  # basic format for the line

        # get params, with addresses if need be

        logging.debug(print_line.format(pos=self.pointer, opname=method_name, params=print_params))

def handle_output(output):
    output_list.append(output)

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]  
    output_list = []      
    computer = IntcodeComputer(output_method=handle_output)
    computer.get_code_from_file(file_name)
    if len(sys.argv) > 2:
        computer_input = [int(x) for x in sys.argv[2:]]
        computer.set_input(computer_input)
    computer.run()
    logging.debug(output_list)
