"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    register = [0] * 8
    ram = [0] * 256
    pc = 0
    SP = 7
    halted = False
    equal = [0] * 8

    L = 0
    G = 0
    E = 0
    register[SP] = 0xf4

    HALT = 1
    LDI = 130
    MUL = 162
    PRN = 71
    CMP = 167
    JEQ = 85
    JMP = 84
    JNE = 86

    def __init__(self):
        """Construct a new CPU."""
        pass

    def load(self, program=None):
        """Load a program into memory."""

        program = 'sctest.ls8'
        address = 0

        with open(program) as f:
            for line in f:
                line = line.split('#')[0]
                line = line.strip()
        
                if line == '':
                    continue
                val = int(line, 2)
                self.ram[address] = val
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        value = self.ram[address]
        return value

    def ram_write(self, value, address):

        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        while not self.halted:
            instruction = self.ram[self.pc]
            if instruction == self.LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.register[reg_num] = value
                self.pc += 3
            elif instruction == self.CMP:
                index1 = self.ram[self.pc + 1]
                index2 = self.ram[self.pc + 2]

                first = self.register[index1]
                second = self.register[index2]
                if first < second:
                    self.L = 1
                    self.G = 0
                    self.E = 0
                elif first > second:
                    self.L = 1
                    self.G = 1
                    self.E = 0

                elif first == second:
                    self.L = 0
                    self.G = 0
                    self.E = 1

                else:
                    print("ERROR")
                    exit()
                self.pc += 3
            elif instruction == self.JEQ:
                if self.E == 1:
                    goto = self.ram[self.pc + 1]
                    self.pc = self.register[goto]

                elif self.E == 0:
                    self.pc += 2
                else:
                    print("ERROR")
                    exit()
            elif instruction == self.JNE:
                if self.E == 0:
                    goto = self.ram[self.pc + 1]
                    self.pc = self.register[goto]
                elif self.E != 0:
                    self.pc += 2

                else:
                    self.pc += 2

            elif instruction == self.JMP:
                goto = self.ram[self.pc + 1]
                self.pc = self.register[goto]

            elif instruction == self.PRN:
                print(self.register[self.ram[self.pc + 1]])
                self.pc += 2
            elif instruction == self.HALT:
                self.halted = True
                self.pc += 1
