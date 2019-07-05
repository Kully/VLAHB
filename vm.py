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
import math
import os
import random
import string
import sys
import time
import util

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame import gfxdraw


# CPU constants and data structures

COMMANDS_PER_SEC = 10
DELAY_BETWEEN_COMMANDS = 1. / COMMANDS_PER_SEC  # in seconds

RAM_NUM_OF_SLOTS = 128000  # 512KB == Bill Gates Number
MAX_RAM_VALUE = 2**32 - 1  # largest value in a slot of RAM (hhhh hhhh) - 4 bytes
RAM = [0] * RAM_NUM_OF_SLOTS

STACK = []
STACK_FRAME_SIZE = 128
STACK_MAX_SIZE = 32

ROM = []


timing_the_opcodes_str = 'opcode,time\n'

# pygame
WIDTH_DISPLAY_PIXELS = 160
HEIGHT_DISPLAY_PIXELS = 120


def starting_PC():
    f = open('start_pc.txt', 'r')
    PC = int(f.readlines()[0])
    f.close()
    return PC


def return_intermediate_color(value):
    fraction = (value) / (RAM_NUM_OF_SLOTS)
    return (0, int(fraction * 255), 0)


def fill_ROM_with_hex_lines(hex_lines):
    for line in hex_lines:
        ROM.append(line)


def reset_RAM_values_to_zero():
    RAM = [0] * RAM_NUM_OF_SLOTS


def manage_ram_slot_overunder_flow(index_in_RAM):
    if RAM[index_in_RAM] < 0:
        RAM[index_in_RAM] = MAX_RAM_VALUE + RAM[index_in_RAM]
        print('    ***Stack Underflow at RAM[%r]***'%index_in_RAM)

    elif RAM[index_in_RAM] > MAX_RAM_VALUE:
        RAM[index_in_RAM] = MAX_RAM_VALUE - RAM[index_in_RAM]
        print('    ***Stack Overflow at RAM[%r]***'%index_in_RAM)


def manage_stack_size_overflow():
    assert len(STACK) <= STACK_MAX_SIZE, util.STACK_OVERFLOW_ERROR_MSG.format(STACK_MAX_SIZE)


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
    global timing_the_opcodes_str
    # pygame init
    pygame.init()

    pygame.display.set_caption('VLAHB')
    gameDisplay = pygame.display.set_mode(
        (WIDTH_DISPLAY_PIXELS, HEIGHT_DISPLAY_PIXELS)
    )
    clock = pygame.time.Clock()


    PC = starting_PC()  # program counter
    EXIT_LOOP = False

    while True:
        # time.sleep(DELAY_BETWEEN_COMMANDS)

        try:
            ROM[PC]
            ROM[PC+1]
        except IndexError:
            util.slow_print('PC out of range...exiting vm',
                            0.1, print_empty_line=True)
            break

        print('PC: %r'%PC)
        print('')
        print('    %s'%ROM[PC])
        print('    %s'%ROM[PC+1])
        print('')

        # convert all hex to int
        word0_first_half = util.hex_to_int(ROM[PC][:4])
        word0_second_half = util.hex_to_int(ROM[PC][4:])
        word1 = util.hex_to_int(ROM[PC+1])

        word1_first_half = util.hex_to_int(ROM[PC+1][:4])
        word1_second_half = util.hex_to_int(ROM[PC+1][4:])

        PC += 2

        ############
        # OP CODES #
        ############

        # GOTO == 0001
        if word0_second_half == 1:
            a = time.time()
            PC = word1
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    GOTO: PC -> %s' %word1)


        # DIRECT LOAD == 0002
        elif word0_second_half == 2:
            a = time.time()

            RAM[word0_first_half] = word1
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s] %s' %(word0_first_half, word1))

        # DIRECT ADD == 0003
        elif word0_second_half == 3:
            a = time.time()

            RAM[word0_first_half] += word1
            manage_ram_slot_overunder_flow(word0_first_half)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    ADD R[%s] %s' %(word0_first_half, word1))

        # DIRECT SUBTRACT == 0004
        elif word0_second_half == 4:
            a = time.time()

            RAM[word0_first_half] -= word1
            manage_ram_slot_overunder_flow(word0_first_half)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    SUB R[%s] %s' %(word0_first_half, word1))            

        # DIRECT MULTIPLY == 0005
        elif word0_second_half == 5:
            a = time.time()

            RAM[word0_first_half] *= word1
            manage_ram_slot_overunder_flow(word0_first_half)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    MUL R[%s] %s' %(word0_first_half, word1))

        # DIRECT DIVIDE == 0006
        elif word0_second_half == 6:
            a = time.time()
            RAM[word0_first_half] /= word1
            manage_ram_slot_overunder_flow(word0_first_half)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    DIV R[%s] %s' %(word0_first_half, word1))
            

        # REGISTER TO REGISTER LOAD == 0007
        elif word0_second_half == 7:
            a = time.time()
            RAM[word0_first_half] = RAM[word1]
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s] R[%s]' %(word0_first_half, word1))

        # REGISTER TO REGISTER ADD == 0008
        elif word0_second_half == 8:
            a = time.time()
            RAM[word0_first_half] += RAM[word1]
            manage_ram_slot_overunder_flow(word0_first_half)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    ADD R[%s] R[%s]' %(word0_first_half, word1))
            

        # REGISTER TO REGISTER SUBTRACT == 0009
        elif word0_second_half == 9:
            a = time.time()
            RAM[word0_first_half] -= RAM[word1]
            manage_ram_slot_overunder_flow(word0_first_half)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    SUB R[%s] R[%s]' %(word0_first_half, word1))
            

        # REGISTER TO REGISTER MULTIPLY == 000a
        elif word0_second_half == 10:
            a = time.time()
            RAM[word0_first_half] *= RAM[word1]
            manage_ram_slot_overunder_flow(word0_first_half)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    MUL R[%s] R[%s]' %(word0_first_half, word1))

        # REGISTER TO REGISTER DIVIDE == 000b
        elif word0_second_half == 11:
            a = time.time()
            RAM[word0_first_half] /= RAM[word1]
            manage_ram_slot_overunder_flow(word0_first_half)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    DIV R[%s] R[%s]' %(word0_first_half, word1))
            

        # COMPARE REGISTER TO DIRECT  == 000c
        elif word0_second_half == 12:
            a = time.time()
            cmp_true = 'false'
            if RAM[word0_first_half] == word1:
                cmp_true = 'true'
                PC += 2
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    CMP R[%s] %s -> %s' %(word0_first_half, word1, cmp_true))

        # COMPARE REGISTER TO REGISTER == 000d
        elif word0_second_half == 13:
            a = time.time()
            cmp_true = 'false'
            if RAM[word0_first_half] == RAM[word1]:
                PC += 2
                cmp_true = 'true'
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    CMP R[%s] R[%s] -> %s' %(word0_first_half, word1, cmp_true))

        # CALL == 000e
        elif word0_second_half == 14:
            eee = time.time()
            STACK.append(PC)

            manage_stack_size_overflow()

            index = len(STACK)
            a = STACK_FRAME_SIZE * (0 + index)
            b = STACK_FRAME_SIZE * (1 + index)
            RAM[a : b] = RAM[0 : STACK_FRAME_SIZE]
            PC = word1
            fff = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, fff-eee)
            print('    CALL: Push %s to the Stack: PC -> %s' %(word1, word1))

        # RETURN == 000f
        elif word0_second_half == 15:
            ggg = time.time()

            manage_stack_size_overflow()

            index = len(STACK)
            a = STACK_FRAME_SIZE * (0 + index)
            b = STACK_FRAME_SIZE * (1 + index)
            RAM[0 : STACK_FRAME_SIZE] = RAM[a : b]
            PC = STACK.pop()
            hhh = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, hhh-ggg)
            print('    RETURN: Pop %s from the Stack: PC -> %s' %(PC, PC))

        # POP == fff0
        elif word0_second_half == 65520:
            a = time.time()
            
            manage_stack_size_overflow()

            index = len(STACK)
            a = STACK_FRAME_SIZE * (0 + index)
            b = STACK_FRAME_SIZE * (1 + index)
            RAM[0 : STACK_FRAME_SIZE] = RAM[a : b]
            STACK.pop()
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    POP: Pop %s from the Stack' %(PC))

        # PUSH == fff1
        elif word0_second_half == 65521:
            a = time.time()
            STACK.append(PC)

            manage_stack_size_overflow()

            index = len(STACK)
            a = STACK_FRAME_SIZE * (0 + index)
            b = STACK_FRAME_SIZE * (1 + index)
            RAM[a : b] = RAM[0 : STACK_FRAME_SIZE]
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    PUSH: Push %s to the Stack' %(word1))

        # CLEAR == fff2
        elif word0_second_half == 65522:
            a = time.time()
            len_of_vram = WIDTH_DISPLAY_PIXELS * HEIGHT_DISPLAY_PIXELS
            RAM[4101:4101 + len_of_vram] = [0] * len_of_vram
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    CLEAR')


        # STRICT LESS THAN REGISTER TO DIRECT == 0010
        elif word0_second_half == 16:
            a = time.time()
            is_this_true = 'false'
            if RAM[word0_first_half] < word1:
                is_this_true = 'true'
                PC += 2
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LT R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

        # STRICT LESS THAN REGISTER TO REGISTER == 0011
        elif word0_second_half == 17:
            a = time.time()
            is_this_true = 'false'
            if RAM[word0_first_half] < RAM[word1]:
                is_this_true = 'true'
                PC += 2
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LT R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

        # LESS THAN OR EQUAL REGISTER TO DIRECT == 0012
        elif word0_second_half == 18:
            a = time.time()
            is_this_true = 'false'
            if RAM[word0_first_half] <= word1:
                is_this_true = 'true'
                PC += 2
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LTE R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

        # LESS THAN OR EQUAL REGISTER TO REGISTER == 0013
        elif word0_second_half == 19:
            a = time.time()
            is_this_true = 'false'
            if RAM[word0_first_half] <= RAM[word1]:
                is_this_true = 'true'
                PC += 2
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LTE R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

        # STRICT GREATER THAN REGISTER TO DIRECT == 0014
        elif word0_second_half == 20:
            a = time.time()
            is_this_true = 'false'
            if RAM[word0_first_half] > word1:
                is_this_true = 'true'
                PC += 2
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    GT R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

        # STRICT GREATER THAN REGISTER TO REGISTER == 0015
        elif word0_second_half == 21:
            a = time.time()
            is_this_true = 'false'
            if RAM[word0_first_half] > RAM[word1]:
                is_this_true = 'true'
                PC += 2
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    GT R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

        # GREATER THAN OR EQUAL REGISTER TO DIRECT == 0016
        elif word0_second_half == 22:
            a = time.time()
            is_this_true = 'false'
            if RAM[word0_first_half] >= word1:
                is_this_true = 'true'
                PC += 2
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    GTE R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

        # GREATER THAN OR EQUAL REGISTER TO REGISTER == 0017
        elif word0_second_half == 23:
            a = time.time()
            is_this_true = 'false'
            if RAM[word0_first_half] >= RAM[word1]:
                is_this_true = 'true'
                PC += 2
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    GTE R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))


        # BLIT == 0018
        elif word0_second_half == 24:
            a = time.time()
            surf = pygame.Surface(
                (WIDTH_DISPLAY_PIXELS, HEIGHT_DISPLAY_PIXELS)
                )
            surf.lock()
            for i in range(WIDTH_DISPLAY_PIXELS * HEIGHT_DISPLAY_PIXELS):
                color = RAM[4101 + i]
                rgba_tuple = (
                    (color >> 24) & 0xFF,
                    (color >> 16) & 0xFF,
                    (color >>  8) & 0xFF,
                    (color >>  0) & 0xFF)
                x = int(i % WIDTH_DISPLAY_PIXELS)
                y = int(i / WIDTH_DISPLAY_PIXELS)
                surf.set_at((x, y), rgba_tuple)
            surf.unlock()
            gameDisplay.blit(surf, (0, 0))
            pygame.display.update()

            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    BLIT')

        # DIRECT SQRT == 0019
        elif word0_second_half == 25:
            a = time.time()
            RAM[word0_first_half] = math.sqrt(word1)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    SQRT R[%s] %s' %(word0_first_half, word1))

        # REGISTER TO REGISTER SQRT == 001a
        elif word0_second_half == 26:
            a = time.time()
            RAM[word0_first_half] = math.sqrt(RAM[word1])
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    SQRT R[%s] R[%s]' %(word0_first_half, word1))

        # DIRECT SIN == 001b
        elif word0_second_half == 27:
            a = time.time()
            RAM[word0_first_half] = math.sin(word1)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    SIN R[%s] %s' %(word0_first_half, word1))

        # REGISTER TO REGISTER SIN == 001c
        elif word0_second_half == 28:
            a = time.time()
            RAM[word0_first_half] = math.sin(RAM[word1])
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    SIN R[%s] R[%s]' %(word0_first_half, word1))

        # DIRECT COS == 001d
        elif word0_second_half == 29:
            a = time.time()
            RAM[word0_first_half] = math.cos(word1)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    COS R[%s] %s' %(word0_first_half, word1))

        # REGISTER TO REGISTER COS == 001e
        elif word0_second_half == 30:
            a = time.time()
            RAM[word0_first_half] = math.cos(RAM[word1])
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    COS R[%s] R[%s]' %(word0_first_half, word1))

        # LD R[i:j] k == 001f
        elif word0_second_half == 31:
            a = time.time()
            i = util.hex_to_int(ROM[PC][:4])

            word0_second_half = util.hex_to_int(ROM[PC][4:])

            j = util.hex_to_int(ROM[PC+1][:4])
            k = util.hex_to_int(ROM[PC+1][4:])

            RAM[i:j+1] = [k] * (j+1-i)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s:%s] %s' %(i, j, k))

        # LD R[i:j] R[k] == 0020
        elif word0_second_half == 32:
            a = time.time()
            i = util.hex_to_int(ROM[PC-2][:4])
            
            word0_second_half = util.hex_to_int(ROM[PC - 2][4:])
            
            j = util.hex_to_int(ROM[PC+1 - 2][:4])
            k = util.hex_to_int(ROM[PC+1 - 2][4:])

            RAM[i:j+1] = [RAM[k]] * (j+1-i)
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s:%s] R[%s]' %(i, j, k))

        # LD R[i:j] R[k:l] == 0021
        elif word0_second_half == 33:
            a = time.time()

            ram_span = util.hex_to_int(ROM[PC - 2][:4])  # ram_span := j-i
            word0_second_half = util.hex_to_int(ROM[PC - 2][4:])
            i = util.hex_to_int(ROM[PC+1 - 2][:4])
            k = util.hex_to_int(ROM[PC+1 - 2][4:])

            RAM[i:i + ram_span+1] = RAM[k:k + ram_span+1]
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s:%s] R[%s:%s]' %(i, i+ram_span, k, k+ram_span))


        # FLOOR == 0022
        elif word0_second_half == 34:
            a = time.time()
            RAM[word1] = math.floor(RAM[word1])
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    FLOOR R[%s]' %word1)

        # CEIL == 0023
        elif word0_second_half == 35:
            a = time.time()
            RAM[word1] = math.ceil(RAM[word1])
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    CEIL R[%s]' %word1)

        # RAND == 0024
        elif word0_second_half == 36:
            a = time.time()
            RAM[word1] = random.choice([0, 1])
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    RAND R[%s]' %word1)

        # LD R[V] R[Z] == 0100
        # 
        # LD R[R[i]] R[R[j]]
        elif word0_second_half == 256:
            a = time.time()
            encoded_letters = util.int_to_hex(word0_first_half)

            i = encoded_letters[0]
            j = encoded_letters[1]

            i = util.hex_digit_to_UVYZ[i]
            j = util.hex_digit_to_UVYZ[j]

            ram_index_i = util.UVYZ_to_ram_index[i]
            ram_index_j = util.UVYZ_to_ram_index[j]

            RAM[RAM[ram_index_i]] = RAM[RAM[ram_index_j]]
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s] R[%s]' %(
                RAM[ram_index_i],
                RAM[ram_index_j],
            ))

        # LD R[V:U] R[Z] == 0101
        # 
        # LD R[R[i]:R[j]] R[R[k]]
        elif word0_second_half == 257:
            a = time.time()
            encoded_letters = util.int_to_hex(word0_first_half)

            i = encoded_letters[0]
            j = encoded_letters[1]
            k = encoded_letters[2]

            i = util.hex_digit_to_UVYZ[i]
            j = util.hex_digit_to_UVYZ[j]
            k = util.hex_digit_to_UVYZ[k]

            ram_index_i = util.UVYZ_to_ram_index[i]
            ram_index_j = util.UVYZ_to_ram_index[j]
            ram_index_k = util.UVYZ_to_ram_index[k]

            array_span = len(RAM[RAM[ram_index_i]:RAM[ram_index_j]])
            RAM[RAM[ram_index_i]:RAM[ram_index_j]] = [RAM[RAM[ram_index_k]]] * array_span
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s:%s] R[%s]' %(
                RAM[ram_index_i],
                RAM[ram_index_j],
                RAM[ram_index_k],
            ))

        # LD R[U:V] R[Y:Z] == 0102
        # 
        # LD R[R[i]:R[j]] R[R[k]:R[l]]
        elif word0_second_half == 258:
            a = time.time()
            encoded_letters = util.int_to_hex(word0_first_half)

            i = encoded_letters[0]
            j = encoded_letters[1]
            k = encoded_letters[2]
            l = encoded_letters[2]

            i = util.hex_digit_to_UVYZ[i]
            j = util.hex_digit_to_UVYZ[j]
            k = util.hex_digit_to_UVYZ[k]
            l = util.hex_digit_to_UVYZ[l]

            ram_index_i = util.UVYZ_to_ram_index[i]
            ram_index_j = util.UVYZ_to_ram_index[j]
            ram_index_k = util.UVYZ_to_ram_index[k]
            ram_index_l = util.UVYZ_to_ram_index[l]

            RAM[RAM[ram_index_i]:RAM[ram_index_j]] = RAM[RAM[ram_index_k]:RAM[ram_index_l]]
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s:%s] R[%s:%s]' %(
                RAM[ram_index_i],
                RAM[ram_index_j],
                RAM[ram_index_k],
                RAM[ram_index_l],
            ))

        # LD R[U:V] R[k] == 0103
        # 
        # LD R[R[i]:R[j]] R[k]
        elif word0_second_half == 259:
            a = time.time()
            encoded_letters = util.int_to_hex(word0_first_half)

            i = encoded_letters[0]
            j = encoded_letters[1]

            i = util.hex_digit_to_UVYZ[i]
            j = util.hex_digit_to_UVYZ[j]

            ram_index_i = util.UVYZ_to_ram_index[i]
            ram_index_j = util.UVYZ_to_ram_index[j]

            array_span = len(RAM[RAM[ram_index_i]:RAM[ram_index_j]])
            RAM[RAM[ram_index_i]:RAM[ram_index_j]] = [RAM[word1]] * array_span
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s:%s] R[%s]' %(
                RAM[ram_index_i],
                RAM[ram_index_j],
                word1,
            ))

        # LD R[U] R[i] == 0104
        elif word0_second_half == 260:
            a = time.time()
            encoded_letters = util.int_to_hex(word0_first_half)

            i = encoded_letters[0]
            i = util.hex_digit_to_UVYZ[i]

            ram_index_i = util.UVYZ_to_ram_index[i]

            RAM[RAM[ram_index_i]] = RAM[word1]
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s] R[%s]' %(
                RAM[ram_index_i],
                word1,
            ))

        # LD R[U] i == 0105
        elif word0_second_half == 261:
            a = time.time()
            encoded_letters = util.int_to_hex(word0_first_half)

            i = encoded_letters[0]
            i = util.hex_digit_to_UVYZ[i]

            ram_index_i = util.UVYZ_to_ram_index[i]

            RAM[RAM[ram_index_i]] = word1
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s] %s' %(
                RAM[ram_index_i],
                word1,
            ))

        #  LD R[U:V] i == 0106
        elif word0_second_half == 262:
            a = time.time()
            encoded_letters = util.int_to_hex(word0_first_half)

            u = encoded_letters[0]
            u = util.hex_digit_to_UVYZ[u]

            v = encoded_letters[1]
            v = util.hex_digit_to_UVYZ[v]

            ram_index_u = util.UVYZ_to_ram_index[u]
            ram_index_v = util.UVYZ_to_ram_index[v]

            array_span = len(RAM[RAM[ram_index_u] : RAM[ram_index_v]])
            RAM[RAM[ram_index_u] : RAM[ram_index_v]] = [word1] * array_span
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    LD R[%s:%s] %s' %(
                RAM[ram_index_u],
                RAM[ram_index_v],
                word1,
            ))

        # EXIT == ffff
        elif word0_second_half == 2**16 - 1:
            a = time.time()
            EXIT_LOOP = True
            b = time.time()
            timing_the_opcodes_str += '%s,%s\n' %(word0_second_half, b-a)
            print('    EXIT')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_LOOP = True

        print('RAM:')
        print('    RAM[0:6]    : %r'  %RAM[0 : 6])
        print('    RAM[128:134]: %r'  %RAM[128 : 134])
        print('    RAM[256:262]: %r'  %RAM[128*2 : 128*2 + 6])
        print('    RAM[384:390]: %r'  %RAM[128*3 : 128*3 + 6])
        print('')
        print('    STACK:        %r' %STACK)
        print('    RAM[4100]:    %r  # return value' %RAM[4100])
        print('    RAM[U,V,Y,Z]: [%s, %s, %s, %s]  # stack pointers' %(
            RAM[4096], RAM[4097], RAM[4098], RAM[4099])
        )
        print('\n\n')

        if EXIT_LOOP:
            pygame.quit()
            util.slow_print('Exiting VM...', 0.11, print_empty_line=True)

            # write opcode timings to file
            a_file = open('timing_the_opcodes.csv', 'w')
            a_file.write(timing_the_opcodes_str)
            a_file.close()

            break


if __name__ == "__main__":
    hexfilename = 'hex/file.hex'
    hex_lines = util.return_lines_from_file(hexfilename)
    fill_ROM_with_hex_lines(hex_lines)
    validate_hex_file(hexfilename)

    exec(hex_lines)  # with pygame visualization
