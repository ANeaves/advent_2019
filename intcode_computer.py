import sys
from copy import deepcopy
import logging
import threading
from queue import Queue

class IntcodeStates():
    idle = 0
    running = 1
    halted = 99

    error = -1

class IntcodeComputer():

    def __init__(self, code=[], prog_input=[], name=None, is_async=False, output_method=print):
        logging.info("Creating Intcode Computer V3: Now with Multithreading!")
        self.code = code
        self.memory = deepcopy(self.code)
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

        self.instruction_set = {
            1: (self.add, 3),
            2: (self.mul, 3),
            3: (self.put, 1),
            4: (self.out, 1),
            5: (self.jmp_true, 2),
            6: (self.jmp_flse, 2),
            7: (self.less, 3),
            8: (self.eql, 3),
            99: (self.halt, 0)
        }

    def set_input(self, prog_input):
        logging.info("%s SETTING INPUT TO %s", self.name, prog_input)
        self.input.put(prog_input)

    def set_output_method(self, method):
        self.output_method = method

    def save_code(self, code):
        self.code = code
        self.memory = deepcopy(self.code)

    def reset_memory(self):
        self.memory = deepcopy(self.code)
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
                instruction, param_count = self.instruction_set[opcode]
                params = self.memory[self.pointer+1:self.pointer+param_count+1]
                param_modes = str(full_opcode)[0:-2].rjust(param_count, '0')
                instruction(*params, param_modes)
                self.pointer += 1 + param_count

            except KeyError:
                self.state = IntcodeStates.error
                logging.error("ERROR: Instruction not found: %d", instruction)
            
            except IndexError:
                self.state = IntcodeStates.error
                logging.error("ERROR: Index Out of Bounds")

    def get_param(self, param, param_mode):
        if param_mode == '1':
            return param
        else:
            return self.memory[param]

    def get_params(self, params, param_modes):
        param_modes = reversed(param_modes)
        return list(map(self.get_param, params, param_modes))

    # OPCODE METHODS BELOW
    def add(self, a, b, out, param_modes):
        a, b, _ = self.get_params([a, b, out], param_modes)
        logging.debug("%2s: %04x: ADD %8x %8x -> %8x", self.name, self.pointer, a, b, out)
        self.memory[out] = a + b

    def mul(self, a, b, out, param_modes):
        a, b, _ = self.get_params([a, b, out], param_modes)
        logging.debug("%2s: %04x: MUL %8x %8x -> %8x", self.name, self.pointer, a, b, out)
        self.memory[out] = a * b

    def put(self, put_addr, param_modes):
        logging.debug("%2s: %04x: LOD %8s %8s -> %8x", self.name, self.pointer, "[INPUT]", " ", put_addr)
        self.memory[put_addr] = self.input.get()

    def out(self, out_addr, param_modes):
        logging.debug("%2s: %04x: WRT %8x %8s -> %8s", self.name, self.pointer, out_addr, "", "[OUTPUT]")
        self.output = self.memory[out_addr]
        if self.output_method:
            self.output_method(self.memory[out_addr])
    
    def jmp_true(self, check, jmp_addr, param_modes):
        check, jmp_addr = self.get_params([check, jmp_addr], param_modes)
        logging.debug("%2s: %04x: JNZ %8x %8s -> %8x", self.name, self.pointer, check, "", jmp_addr)
        if check:
            self.pointer = jmp_addr - 3  # the minus 3 is to account for the pointer moving at the end of the run loop
    
    def jmp_flse(self, check, jmp_addr, param_modes):
        check, jmp_addr = self.get_params([check, jmp_addr], param_modes)
        logging.debug("%2s: %04x: JEZ %8x %8s -> %8x", self.name, self.pointer, check, "", jmp_addr)
        if not check:
            self.pointer = jmp_addr - 3
    
    def less(self, a, b, out, param_modes):
        a, b, _ = self.get_params([a, b, out], param_modes)
        logging.debug("%2s: %04x: TLT %8x %8x -> %8x", self.name, self.pointer, a, b, out)
        if a < b:
            self.memory[out] = 1
        else:
            self.memory[out] = 0
    
    def eql(self, a, b, out, param_modes):
        a, b, _ = self.get_params([a, b, out], param_modes)
        logging.debug("%2s: %04x: TEQ %8x %8x -> %8x", self.name, self.pointer, a, b, out)
        if a == b:
            self.memory[out] = 1
        else:
            self.memory[out] = 0

    def halt(self, param_modes):
        logging.info("%2s: Program Complete", self.name)
        self.state = IntcodeStates.halted

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]
    computer = IntcodeComputer()
    computer.get_code_from_file(file_name)
    computer.run()
    logging.info("Resulting Memory:\n%s", computer.memory)
