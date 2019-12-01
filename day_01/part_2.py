# day one, fuel calculator. divide by 3, round down, subtract 2
import sys

file_name = sys.argv[1]

def calc_fuel_requirements(mass):
    fuel = mass // 3
    fuel = fuel -2
    if fuel < 0:
        return 0
    return fuel + calc_fuel_requirements(fuel)  # recurse for fuel weight

with open(file_name) as f:
    total = 0
    for line in f:
        val = calc_fuel_requirements(int(line.strip()))
        print("Original Val: {}, Calc Fuel: {}".format(line, val))
        total = total + val
    print("TOTAL: {}".format(total))