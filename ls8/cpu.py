"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    
    def __init__(self):
        """Construct a new CPU."""
        # r5 = interrupt mask
        # r6 = interrupt status
        # r7 = stack pointer
        self.registers = [0] * 8 # r0 - r7
        self.running = False
        self.ram = [0] * 128
        self.pc = 0


    def ram_read(self, MAR):
        """Read the RAM. MAR = memory address register"""
        try:
            return self.ram[MAR]
        except IndexError:
            print("index out of range for RAM read")


    def ram_write(self, MDR, MAR):
        """write to the RAM. MDR = Memory Data Register"""
        try:
            self.ram[MAR] = MDR
            print("saved to RAM")
        except IndexError:
            print("index out of range for RAM write")

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram_write(instruction, address)
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

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            op_code = bin(self.ram_read(self.pc)) # instruction

            if op_code == 0b00000001:# HLT (halt)
                self.running = False
                sys.exit(1)

            elif op_code == 0b10000010:  # LDI (load "immediate")
                data_a = self.ram_read(self.pc + 1)
                data_b = self.ram_read(self.pc + 2)
                self.registers[data_a] = data_b
                self.pc += 3
                
            elif op_code == 0b01000111:  # PRN ()
                data_a = self.ram_read(self.pc + 1)
                print(self.registers[data_a])
                self.pc += 1
                pass
            else:
                print(op_code)


 