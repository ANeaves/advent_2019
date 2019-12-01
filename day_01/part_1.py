# day one, fuel calculator. divide by 3, round down, subtract 2
import sys

file_name = sys.argv[1]

with open(file_name) as f:
    total = 0
    for line in f:
        line = line.strip()
        val = int(line)
        val = val // 3
        val = val -2
        print("Original Val: {}, Calc Fuel: {}".format(line, val))
        total = total + val
    print("TOTAL: {}".format(total))
        