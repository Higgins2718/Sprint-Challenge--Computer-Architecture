#!/usr/bin/env python3

"""Main."""
'''
import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()
'''


def ram_read(address):
    value = cpu.ram[address]
    #cpu.pc += 1
    print(value)


def ram_write(value, address):

    cpu.ram[address] = value
    #cpu.pc += 1

def push(value, address):
    cpu.register[cpu.SP] -= 1
    reg_num = cpu.memory[cpu.pc + 1]
    cpu.register[reg_num] = value
    cpu.register[cpu.SP] += 1
    cpu.pc += 2

if __name__ == "__main__":
    import sys
    from cpu import *

    cpu = CPU()

    cpu.load()
    cpu.run()
    #cpu.load()