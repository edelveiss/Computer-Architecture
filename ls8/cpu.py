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
        self.stack_pointer = 7
        # stack pointer is a special register
        # 0xF4 is 244 in decimal
        self.address = 0
        self.reg[self.stack_pointer] = 0xF4

        # Set up the branch table
        self.branchtable = {
            ADD: self.add,
            SUB: self.sub,
            MUL: self.mul,
            DIV: self.div,
            MOD: self.mod,
            LDI: self.ldi,
            HLT: self.hlt,
            PRN: self.prn,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret,

        }
     

    # branchtabel functions
    def prn(self,operand_a, operand_b):
        print(self.reg[operand_a])

    def ldi(self,operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def hlt(self,operand_a, operand_b):
        print(self.reg[operand_a])

    def mul(self,operand_a, operand_b):
        self.reg[operand_a] *= self.reg[operand_b]

    def add(self,operand_a, operand_b):
        self.reg[operand_a] += self.reg[operand_b]

    def sub(self,operand_a, operand_b):
        self.reg[operand_a] -= self.reg[operand_b]

    def div(self,operand_a, operand_b):
        if self.reg[operand_b] != 0:
            self.reg[operand_a] //= self.reg[operand_b]
        else:
            print("division by 0 is undefined")

    def mod(self,operand_a, operand_b):
        if self.reg[operand_b] != 0:
            self.reg[operand_a] %= self.reg[operand_b]
        else:
            print("division by 0 is undefined")

    # python3 ls8.py examples/stack.ls8
    # PUSH function
    def push(self,operand_a, operand_b):
        if self.reg[self.stack_pointer] < self.address:
            print("Stack overflow!")
            sys.exit(2)
        else:
            # decrement stack pointer
            self.reg[self.stack_pointer] -= 1
            # get a value of operand_a register
            value_in_reg = self.reg[operand_a]
            self.ram_write(value_in_reg,self.reg[self.stack_pointer] )
            # self.ram[self.reg[self.stack_pointer]] = value_in_reg

    # POP function
    def pop(self,operand_a, operand_b):
        if self.reg[self.stack_pointer] == 0xF4:
            print("Stack underflow!")
            sys.exit(2)
        else:
            # pop top stack value
            top_stack_value = self.ram_read(self.reg[self.stack_pointer])
            # top_stack_value = self.ram[self.reg[self.stack_pointer]]
            # increment stack pointer
            self.reg[self.stack_pointer] += 1
            # write top stack value into operand_a register
            self.reg[operand_a] = top_stack_value

    # CALL op
    def call(self,operand_a, operand_b):
        given_register = self.ram_read(operand_a)
        # decrement the stack pointer
        self.reg[self.stack_pointer] -= 1
        return_address = self.pc +2
        # store the return address onto the stack
        self.ram_write(return_address,self.reg[self.stack_pointer] )
        # set pc to the value in given register
        self.pc = self.reg[given_register]


    # RET op
    def ret(self,operand_a, operand_b):
        # set pc to the value at the top of the stack
        self.pc = self.ram_read(self.reg[self.stack_pointer])
        # increment the stack pointer
        self.reg[self.stack_pointer] += 1


      
    # python3 ls8.py examples/print8.ls8
    def load_hardcoded(self):
        # For now, we've just hardcoded a program:
        address = 0 
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
            print(self.ram)
            address += 1

    # python3 ls8.py examples/mult.ls8
    def load(self, filename):
        """Load a program into memory."""


        try:
            with open(filename) as f:
                for line in f:
                    # Split the current line on the symbol #
                    split_line = line.split("#")
                    # Remove white spaces and \n character
                    code_value = split_line[0].strip()
                    # Make sure that the value bafore the # symbol is not empty
                    if code_value == "":
                        continue
                    num = int(code_value,2)
                    self.ram_write(num, self.address)
                    self.address += 1

        except FileNotFoundError:
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)


    def set_pc_operation(self, IR,operand_a, operand_b ):
        '''set_pc_operation'''
        if IR in self.branchtable:
            self.branchtable[IR](operand_a, operand_b)

        else:
            raise Exception("Unsupported set_pc_operation")

  

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op in self.branchtable:
            self.branchtable[op](reg_a, reg_b)

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
            IR = self.ram_read(self.pc)
            
            # size of operation code
            shifted_num = IR >> 6
            op_size = shifted_num +1
            alu_operation = IR >> 5 & 0b001 
            set_to_pc = IR >> 4 & 0b0001
            

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if set_to_pc == 0:
                if alu_operation == 1:
                    self.alu(IR, operand_a, operand_b)

                elif IR == HLT:
                    running = False
                    # sys.exit(0) 

                elif IR in self.branchtable:
                    self.branchtable[IR](operand_a,operand_b)

                else:
                    print(f"Unknown operation: {IR}")
                    sys.exit(1)

                
                self.pc += op_size

            else:
                self.set_pc_operation(IR,operand_a, operand_b )

#-------------------------------------------------------------------
    # def run_without_branch_table(self):
    #     """Run the CPU."""
    #     # keep track of running
    #     running = True
       
    #     while running:
    #         # self.trace()
    #         # Instruction Register
    #         IR = self.ram_read(self.pc)
            
    #         # size of operation code
    #         shifted_num = IR >> 6
    #         op_size = shifted_num +1
    #         alu_operation = IR >> 5 & 0b001 

    #         operand_a = self.ram_read(self.pc + 1)
    #         operand_b = self.ram_read(self.pc + 2)
            
    #         if alu_operation == 1:
    #             # operand_a = self.ram_read(self.pc + 1)
    #             # operand_b = self.ram_read(self.pc + 2)
    #             self.alu(IR, operand_a, operand_b)

    #         elif IR == LDI:
    #             # operand_a = self.ram_read(self.pc + 1)
    #             # operand_b = self.ram_read(self.pc + 2)
    #             self.reg[operand_a] = operand_b

    #         elif IR == PRN:
    #             # operand_a = self.ram_read(self.pc + 1)
    #             print(self.reg[operand_a])

    #         elif IR == HLT:
    #             running = False
    #             # sys.exit(0) 

    #         else:
    #             print(f"Unknown operation: {IR}")
    #             sys.exit(1)
    #         self.pc += op_size


    # def run_without_bitwise(self):
    #     """Run the CPU."""
    #     # keep track of running
    #     running = True
       
    #     while running:
    #         # self.trace()
    #         # Instruction Register
    #         value = self.ram_read(self.pc)
    #         IR = self.convert_to_bin_str(value)

    #         # size of operation code  
    #         op_size = int(IR[2:4], 2) +1
    #         alu_operation = IR[4:5]
    #         if alu_operation == 1:
    #             pass

    #         elif IR == self.convert_to_bin_str(LDI):
    #             operand_a = self.ram_read(self.pc + 1)
    #             operand_b = self.ram_read(self.pc + 2)
    #             self.reg[operand_a] = operand_b

    #         elif IR == self.convert_to_bin_str(PRN):
    #             operand_a = self.ram_read(self.pc + 1)
    #             print(self.reg[operand_a])

    #         elif IR == self.convert_to_bin_str(HLT):
    #             running = False
    #             # sys.exit(0) 

    #         else:
    #             print(f"Unknown operation: {IR}")
    #             sys.exit(1)
    #         self.pc += op_size

    # def alu_without_branch_table(self, op, reg_a, reg_b):
    #     """ALU operations."""
    #     if op == ADD:
    #         self.reg[reg_a] += self.reg[reg_b]
    #     elif op == MUL: 
    #         self.reg[reg_a] *= self.reg[reg_b]
    #     elif op == SUB: 
    #         self.reg[reg_a] -= self.reg[reg_b]
    #     elif op == DIV: 
    #         if self.reg[reg_b] != 0:
    #             self.reg[reg_a] /= self.reg[reg_b]
    #         else:
    #             print("division by 0 is undefined")
    #     elif op == MOD: 
    #         if self.reg[reg_b] != 0:
    #             self.reg[reg_a] %= self.reg[reg_b]
    #         else:
    #             print("division by 0 is undefined")


    #     else:
    #         raise Exception("Unsupported ALU operation")

            

        
        


