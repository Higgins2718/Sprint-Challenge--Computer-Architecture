"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    get_command = {
        1: 'HLT',
        130: 'LDI',
        71: 'PRN',
        167: 'CMP',
        85: 'JEQ',
        84: 'JMP',
        86: 'JNE'
    }

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.halted = False
        self.L = 0
        self.G = 0
        self.E = 0
        self.register = [0] * 8
        self.SP = 7
        self.register[self.SP] = 0xf4
        self.branch_table = {
            'HLT': self.handle_halt,
            'LDI': self.handle_ldi,
            'PRN': self.handle_prn,
            'CMP': self.handle_cmp,
            'JEQ': self.handle_jeq,
            'JMP': self.handle_jmp,
            'JNE': self.handle_jne
            }

    def handle_halt(self):
        self.halted = True
        self.pc += 1

    def handle_ldi(self):
        reg_num = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.register[reg_num] = value
        self.pc += 3

    def handle_prn(self):
        print(self.register[self.ram[self.pc + 1]])
        self.pc += 2
        pass

    def handle_cmp(self):
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

    def handle_jeq(self):
        if self.E == 1:
            goto = self.ram[self.pc + 1]
            self.pc = self.register[goto]

        elif self.E == 0:
            self.pc += 2
        else:
            print("ERROR")
            exit()

    def handle_jmp(self):
        goto = self.ram[self.pc + 1]
        self.pc = self.register[goto]

    def handle_jne(self):
        if self.E == 0:
            goto = self.ram[self.pc + 1]
            self.pc = self.register[goto]
        elif self.E != 0:
            self.pc += 2

        else:
            self.pc += 2

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
            action = self.get_command[instruction]
            self.branch_table[action]()