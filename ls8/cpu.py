"""CPU functionality."""

import sys

# ALU ops
ADD = 0b10100000 
SUB = 0b10100001 
MUL = 0b10100010 
DIV = 0b10100011 
MOD = 0b10100100 

INC = 0b01100101 
DEC = 0b01100110 

CMP = 0b10100111 

AND = 0b10101000 
NOT = 0b01101001 
OR  = 0b10101010 
XOR = 0b10101011 
SHL = 0b10101100 
SHR = 0b10101101 

# PC mutators
CALL = 0b01010000 
RET = 0b00010001

INT = 0b01010010 
IRET= 0b00010011

JMP = 0b01010100 
JEQ = 0b01010101 
JNE = 0b01010110 
JGT = 0b01010111 
JLT = 0b01011000 
JLE = 0b01011001 
JGE = 0b01011010 

# Other
NOP = 0b00000000

HLT = 0b00000001 

LDI = 0b10000010 

LD =  0b10000011 
ST  = 0b10000100 

PUSH = 0b01000101 
POP = 0b01000110 

PRN = 0b01000111 
PRA = 0b01001000 

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # CPU has a total of 256 bytes of memory
        self.ram = [0] * 256
        # program counter
        self.pc = 0
        # 8 general-purpose registers
        self.reg = [0] * 8

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
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address_to_read):
        return self.ram[address_to_read]

    def ram_write(self, mdr_data, mar_address):
        '''
        mar is an address from Memory Address Register
        mdr is a data from Memory Data Register
        '''
        self.ram[mar_address] = mdr_data

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


    def convert_to_bin_str(self, number):
        return f"{number:#010b}"

    

    def run(self):
        """Run the CPU."""
        # keep track of running
        running = True
       
        while running:
            # self.trace()
            # Instruction Register
            value = self.ram_read(self.pc)
            IR = self.convert_to_bin_str(value)
            
            # size of operation code
            op_size = int(IR[2:4], 2) +1
            alu_operation = IR[4:5]
            if alu_operation == 1:
                pass

            elif IR == self.convert_to_bin_str(LDI):
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b

            elif IR == self.convert_to_bin_str(PRN):
                operand_a = self.ram_read(self.pc + 1)
                print(self.reg[operand_a])

            elif IR == self.convert_to_bin_str(HLT):
                running = False
                # sys.exit(0) 

            else:
                print(f"Unknown operation: {IR}")
                sys.exit(1)
            self.pc += op_size

            

        
        


