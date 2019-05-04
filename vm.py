'''
Virtual Machine

The vm is what would be the Printed Circuit Board
as well as the etched silicon and logic gates

For now, vm.py looks at the hex file (file.hex)
Eventually, vm.py will look at the binary (file.bin)

```
hhhh hhhh
hhhh hhhh
hhhh hhhh
hhhh hhhh
...
```

where `h` is a hexadecimal value (4 bits, 1/2 a byte) which takes on a value
between 0-f (16 unique values).

This is how 2 rows is interpreted

```
hhhh[index in RAM]hhhh[command]
hhhhhhhh[value]
```

A WORD is a 4byte string of hex values, or 32 bits
```
hhhh hhhh
```

An example of my setup:
```python
ROM = [
    '0x00030001',
    '0x00000004',
    '0x00030002',
    '0x00000006',
    '0x00030003',
    '0x00000001'
]

RAM = []
PC = 0  # program counter
```
'''
import os
import string
import sys
import time
import util

# CPU constants and data structures
COMMANDS_PER_SEC = 10
DELAY_BETWEEN_COMMANDS = 1. / COMMANDS_PER_SEC  # in seconds
ROM = []
RAM_NUM_OF_SLOTS = 128000  # units of 4 bytes // 512KB == Bill Gates Number
MAX_RAM_VALUE = 2**32 - 1  # largest value in a slot of RAM (hhhhhhhh)
RAM = [0] * RAM_NUM_OF_SLOTS

STACK = []

def fill_ROM_with_hex_lines(hex_lines):
    for line in hex_lines:
        ROM.append(line)

def reset_RAM_values_to_zero():
    RAM = [0] * RAM_NUM_OF_SLOTS

def manage_stack_over_under_flow(index_in_RAM):
    if RAM[index_in_RAM] < 0:
        RAM[index_in_RAM] = MAX_RAM_VALUE + RAM[index_in_RAM]
        print("Stack Underflow at RAM[%r]"%index_in_RAM)
    elif RAM[index_in_RAM] > MAX_RAM_VALUE:
        RAM[index_in_RAM] = MAX_RAM_VALUE - RAM[index_in_RAM]
        print("Stack Overflow at RAM[%r]"%index_in_RAM)

def validate_hex_file(file_hex, remove_empty_lines=True, sleeptime=0.1):
    util.slow_print('Validating hex file...')
    time.sleep(0.4)
    lines = util.return_lines_from_file(file_hex)

    sys.stdout.write('\n\r    (  )  even number of hex lines')
    assert len(lines) % 2 == 0, util.EVEN_NUMBER_OF_HEX_LINES_ERROR_MSG
    sys.stdout.flush()
    time.sleep(sleeptime)
    sys.stdout.write('\r    (ok) \n')
    time.sleep(sleeptime*2)

    sys.stdout.write('\r    (  )  all lines in file.hex are 8 chars long')
    assert all(len(line) == 8 for line in lines), util.CHARS_PER_LINE_ERROR_MSG
    sys.stdout.flush()
    time.sleep(sleeptime)
    sys.stdout.write('\r    (ok) \n')
    time.sleep(sleeptime*2)

    sys.stdout.write('\r    (  )  all chars are valid hexadecimal')
    assert all(char in string.hexdigits + 'x' for char in "".join(lines)), util.VALID_HEX_VALUES_ERROR_MSG
    sys.stdout.flush()
    time.sleep(sleeptime)
    sys.stdout.write('\r    (ok) \n')
    time.sleep(sleeptime*2)

    util.slow_print('Validation: PASS!', print_empty_line=True)
    time.sleep(0.4)

def exec(lines_from_file_hex):
    '''Execute lines in ROM'''
    PC = 0  # program counter
    EXIT_LOOP = False
    while True:
        time.sleep(DELAY_BETWEEN_COMMANDS)
        # check if end of ROM
        try:
            ROM[PC]
            ROM[PC+1]
        except IndexError:
            break

        print('PC: %r'%PC)
        print('    ROM lines:')
        print('        %s'%ROM[PC])
        print('        %s'%ROM[PC+1])

        # convert all hex to int
        word0_first_half = util.hex_to_int(ROM[PC][:4])
        word0_second_half = util.hex_to_int(ROM[PC][4:])
        word1 = util.hex_to_int(ROM[PC+1])

        PC += 2

        ############
        # OP CODES #
        ############

        # GOTO == 1
        if word0_second_half == 1:
            PC = word1
            print('    GOTO: PC -> %s' %word1)

        # DIRECT LOAD == 2
        elif word0_second_half == 2:
            RAM[word0_first_half] = word1
            print('\n    LD RAM[%s] %s' %(word0_first_half, word1))

        # DIRECT ADD == 3
        elif word0_second_half == 3:
            RAM[word0_first_half] += word1
            manage_stack_over_under_flow(word0_first_half)
            print('    ADD RAM[%s] %s' %(word0_first_half, word1))

        # DIRECT SUBTRACT == 4
        elif word0_second_half == 4:
            RAM[word0_first_half] -= word1
            manage_stack_over_under_flow(word0_first_half)
            PC += 2
            print('    SUB RAM[%s] %s' %(word0_first_half, word1))

        # DIRECT MULTIPLY == 5
        elif word0_second_half == 5:
            RAM[word0_first_half] *= word1
            manage_stack_over_under_flow(word0_first_half)
            print('    MUL RAM[%s] %s' %(word0_first_half, word1))

        # DIRECT DIVIDE == 6
        elif word0_second_half == 6:
            RAM[word0_first_half] /= word1
            manage_stack_over_under_flow(word0_first_half)
            print('    DIV RAM[%s] %s' %(word0_first_half, word1))

        # REGISTER TO REGISTER LOAD == 7
        elif word0_second_half == 7:
            RAM[word0_first_half] = RAM[word1]
            print('    LD RAM[%s] RAM[%s]' %(word0_first_half, word1))

        # REGISTER TO REGISTER ADD == 8
        elif word0_second_half == 8:
            RAM[word0_first_half] += RAM[word1]
            manage_stack_over_under_flow(word0_first_half)
            print('    ADD RAM[%s] RAM[%s]' %(word0_first_half, word1))

        # REGISTER TO REGISTER SUBTRACT == 9
        elif word0_second_half == 9:
            RAM[word0_first_half] -= RAM[word1]
            manage_stack_over_under_flow(word0_first_half)
            print('    SUB RAM[%s] RAM[%s]' %(word0_first_half, word1))

        # REGISTER TO REGISTER MULTIPLY == a
        elif word0_second_half == 10:
            RAM[word0_first_half] *= RAM[word1]
            manage_stack_over_under_flow(word0_first_half)
            print('    MUL RAM[%s] RAM[%s]' %(word0_first_half, word1))

        # REGISTER TO REGISTER DIVIDE == b
        elif word0_second_half == 11:
            RAM[word0_first_half] /= RAM[word1]
            manage_stack_over_under_flow(word0_first_half)
            print('    DIV RAM[%s] RAM[%s]' %(word0_first_half, word1))

        # COMPARE REGISTER TO VALUE  == c
        elif word0_second_half == 12:
            cmp_true = 'false'
            if RAM[word0_first_half] == word1:
                cmp_true = 'true'
                PC += 2
            print('    CMP RAM[%s] %s -> %s' %(word0_first_half, word1, cmp_true))

        # COMPARE REGISTER TO REGISTER == d
        elif word0_second_half == 13:
            cmp_true = 'false'
            if RAM[word0_first_half] == RAM[word1]:
                PC += 2
                cmp_true = 'true'

            print('    CMP RAM[%s] RAM[%s] -> %s' %(word0_first_half, word1, cmp_true))

        # CALL == e
        elif word0_second_half == 14:
            STACK.append(PC)
            PC = word1
            print('    CALL: Push %s to the Stack: PC -> %s' %(word1, word1))

        # RETURN == f
        elif word0_second_half == 15:
            PC = STACK.pop()
            print('    RETURN: Pop %s from the Stack: PC -> %s' %(PC, PC))

        # EXIT VM == ffff
        elif word0_second_half == 2**16 - 1:
            EXIT_LOOP = True

        # print statements
        i_line_print = '   i:'
        RAM_line_print = 'R[i]:'

        int_width = 4
        sep_space = ' ' * 2
        for i in range(17):
            i_line_print += sep_space
            i_line_print += str(i).rjust(int_width)  # or str(i).zfill(int_width)

            RAM_line_print += sep_space
            RAM_line_print += str(RAM[i]).rjust(int_width)

        print('')
        print(RAM_line_print)
        print(i_line_print)
        print('')

        if EXIT_LOOP:
            util.slow_print('Exiting VM...', 0.11, print_empty_line=True)
            break

if __name__ == "__main__":
    hexfilename = sys.argv[1]
    hex_lines = util.return_lines_from_file(hexfilename)
    fill_ROM_with_hex_lines(hex_lines)
    validate_hex_file(hexfilename)  # validate
    exec(hex_lines)
