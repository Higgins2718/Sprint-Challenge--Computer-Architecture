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
    # THESE SHOULD BE TUPLES
    # Like (false, 0)
    L = 0
    G = 0
    E = 0
    # COMMENT OUT MAYBE
    register[SP] = 0xf4

    HALT = 1
    #LDI = 10000010
    LDI = 130
    MUL = 162
    #PRN = 1000111
    PRN = 71
    CMP = 167
    JEQ = 85
    JMP = 84
    JNE = 86

    def __init__(self):
        """Construct a new CPU."""
        #self.equal['L'] = 0
        #self.equal['G'] = 0
        #self.equal['E'] = 0
        #val0 = ('L', 0)
        #self.equal.append(val0)
        #print("EQUL", self.equal)
        #print("FIND", self.equal['L'])
        pass

    def load(self, progname=None):
        """Load a program into memory."""
        progname='sctest.ls8'

        #progname='examples/print8.ls8'
        #progname='examples/mult.ls8'

        print("LOADING")
        address = 0

        # For now, we've just hardcoded a program:
        #'''
        with open(progname) as f:
            for line in f:
                line = line.split('#')[0]
                line = line.strip()
        
                if line == '':
                    continue
                val = int(line, 2)
                #print("VAL", val)
                self.ram[address] = val
                address += 1
        #print("RAM", self.ram)
        '''
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        print("PROGRAM ", program)
        for instruction in program:
            self.ram[address] = instruction
            address += 1
        '''

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
        # cpu.pc += 1
        print(value)

    def ram_write(self, value, address):

        self.ram[address] = value
        # cpu.pc += 1
    def run(self):
        """Run the CPU."""
        #print("RUNNING")
        #pass
        while not self.halted:
            #print("REGISTER", self.register)

            instruction = self.ram[self.pc]
            #print("INSTRUCTION ", instruction)
            if instruction == self.LDI:
                #REMEMBER TO STORE AT PROPER PLACE
                # LIKE 00001 or 00000
                #print("RUN LDI")
                #value = self.ram[self.pc + 1]
                #reg_num = self.ram[self.pc + 2]
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]

                #print("REG NUM", reg_num)
                #print("VALUE", value)

                self.register[reg_num] = value
                self.pc += 3
            elif instruction == self.CMP:
                index1 = self.ram[self.pc + 1]
                index2 = self.ram[self.pc + 2]

                first = self.register[index1]
                second = self.register[index2]
                #print("COMPARE", first, second)
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
                    #print("GOTO", instruction[self.pc])
                    goto = self.ram[self.pc + 1]
                    self.pc = self.register[goto]

                elif self.E == 0:
                    #print("STAY")
                    self.pc += 2
                else:
                    print("ERROR")
                    exit()
            elif instruction == self.JNE:
                #self.trace()
                #print("JNE")
                if self.E == 0:
                    goto = self.ram[self.pc + 1]
                    #print("GOTO", goto)
                    #print("REGISTER", self.register)

                    self.pc = self.register[goto]
                    #print('JNE GOTO', self.pc)
                elif self.E != 0:
                    self.pc += 2
                    #print('JNE FAILED GOTO', self.pc)


                else:
                    # IS THIS RIGHT?
                    self.pc += 2
                    #print('JNE FAILED GOTO', self.pc)

            elif instruction == self.JMP:
                goto = self.ram[self.pc + 1]
                #print("JMP TO", goto)
                self.pc = self.register[goto]

            elif instruction == self.PRN:
                #print("RUN PRN")
                #print("REGISTER", self.register)
                #reg_num = self.ram[self.pc + 1]
                #print(self.register[reg_num])
                #print(self.register[0])
                #print("PRINT AT THIS LOCATION", self.ram[self.pc + 1])
                #print("AT 72", self.register[self.ram[self.pc + 1]])
                print(self.register[self.ram[self.pc + 1]])
                self.pc += 2
            elif instruction == self.HALT:
                print("RUN HALT")

                self.halted = True
                self.pc +=1
