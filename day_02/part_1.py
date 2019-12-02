import sys
from copy import deepcopy
# read in opcodes:

def get_opcodes(file_name):
    with open(file_name) as f:
        data = f.read()
        print(data)
        data = [int(x) for x in data.split(',')]
    return data

def run_opcodes(opcodes):
    index = 0
    stop = False
    while not stop:
        opcode = opcodes[index]
        dat_1_pos = opcodes[index + 1]
        dat_2_pos = opcodes[index + 2]
        out_pos = opcodes[index + 3]
        # print("OPCODE: {}\nDAT_1_POS: {}\nDAT_2_POS: {}\nOUT_POS: {}".format(opcode, dat_1_pos, dat_2_pos, out_pos))
        if opcode == 1:
            print("ADDITION")
            # addition
            dat_1 = opcodes[dat_1_pos]
            dat_2 = opcodes[dat_2_pos]
            opcodes[out_pos] = dat_1 + dat_2
            increment = 4
        elif opcode == 2:
            print("MULTIPLICATION")
            dat_1 = opcodes[dat_1_pos]
            dat_2 = opcodes[dat_2_pos]
            opcodes[out_pos] = dat_1 * dat_2
            increment = 4
        else:            
            stop = True
            break
        
        index = index + increment
    
    return opcodes


def get_target_output(opcodes, target):
    
    for noun in range(0, 99):
        for verb in range(0, 99):

            opcodes_copy = deepcopy(opcodes)
            opcodes_copy[1] = noun
            opcodes_copy[2] = verb
            ran_opcodes = run_opcodes(opcodes_copy)
            if ran_opcodes[0] == target:
                return noun, verb
    return "NONE", "NONE"


if __name__ == "__main__":
    file_name = sys.argv[1]
    opcodes = get_opcodes(file_name)
    print(opcodes)
    if file_name == "data.txt":
        # required by puzzle
        target = 19690720
        noun, verb = get_target_output(opcodes, target)
        print("NOUN: {}, VERB: {}".format(noun, verb))
    else:
        ran_opcodes = run_opcodes(opcodes)
        print(ran_opcodes)
    