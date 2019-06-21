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

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame import gfxdraw


# CPU constants and data structures

COMMANDS_PER_SEC = 10  # bump to 100
DELAY_BETWEEN_COMMANDS = 1. / COMMANDS_PER_SEC  # in seconds

RAM_NUM_OF_SLOTS = 128000  # 512KB == Bill Gates Number
MAX_RAM_VALUE = 2**32 - 1  # largest value in a slot of RAM (hhhh hhhh) - 4 bytes
RAM = [0] * RAM_NUM_OF_SLOTS

STACK = []
STACK_FRAME_SIZE = 128
STACK_MAX_SIZE = 32

ROM = []


# for pygame
WIDTH_DISPLAY_PIXELS = 80
HEIGHT_DISPLAY_PIXELS = 60
title = 'VLAHB'
PIXELS_PER_GRID_CELL_WIDTH = 4

VRAM = []  # load all pixels with black color
for x in range(WIDTH_DISPLAY_PIXELS):
    for y in range(HEIGHT_DISPLAY_PIXELS):
        VRAM.append(255)


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


def update_one_pixel_color(gameDisplay, word0_first_half, word1):
    # word0_first_half is the index of VRAM
    x = word0_first_half % WIDTH_DISPLAY_PIXELS
    y = int((word0_first_half - x) / WIDTH_DISPLAY_PIXELS)
    rgba_tuple = util.int_to_rgba_tuple(VRAM[word1])

    gfxdraw.pixel(gameDisplay, x, y, rgba_tuple)


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

    # pygame init
    pygame.init()

    pygame.display.set_caption(title)
    gameDisplay = pygame.display.set_mode(
        (WIDTH_DISPLAY_PIXELS, HEIGHT_DISPLAY_PIXELS)
    )
    clock = pygame.time.Clock()

    PC = starting_PC()  # program counter
    EXIT_LOOP = False

    while True:
        # time.sleep(DELAY_BETWEEN_COMMANDS)
        
        # check if end of ROM
        try:
            ROM[PC]
            ROM[PC+1]
        except IndexError:
            util.slow_print('PC out of range...exiting vm',
                            0.1, print_empty_line=True)
            break

        print('PC: %r'%PC)

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
            print('    LD R[%s] %s' %(word0_first_half, word1))

        # DIRECT ADD == 3
        elif word0_second_half == 3:
            RAM[word0_first_half] += word1
            print('    ADD R[%s] %s' %(word0_first_half, word1))
            manage_ram_slot_overunder_flow(word0_first_half)

        # DIRECT SUBTRACT == 4
        elif word0_second_half == 4:
            RAM[word0_first_half] -= word1
            print('    SUB R[%s] %s' %(word0_first_half, word1))
            manage_ram_slot_overunder_flow(word0_first_half)

        # DIRECT MULTIPLY == 5
        elif word0_second_half == 5:
            RAM[word0_first_half] *= word1
            print('    MUL R[%s] %s' %(word0_first_half, word1))
            manage_ram_slot_overunder_flow(word0_first_half)

        # DIRECT DIVIDE == 6
        elif word0_second_half == 6:
            RAM[word0_first_half] /= word1
            print('    DIV R[%s] %s' %(word0_first_half, word1))
            manage_ram_slot_overunder_flow(word0_first_half)

        # REGISTER TO REGISTER LOAD == 7
        elif word0_second_half == 7:
            RAM[word0_first_half] = RAM[word1]
            print('    LD R[%s] R[%s]' %(word0_first_half, word1))

        # REGISTER TO REGISTER ADD == 8
        elif word0_second_half == 8:
            RAM[word0_first_half] += RAM[word1]
            print('    ADD R[%s] R[%s]' %(word0_first_half, word1))
            manage_ram_slot_overunder_flow(word0_first_half)

        # REGISTER TO REGISTER SUBTRACT == 9
        elif word0_second_half == 9:
            RAM[word0_first_half] -= RAM[word1]
            print('    SUB R[%s] R[%s]' %(word0_first_half, word1))
            manage_ram_slot_overunder_flow(word0_first_half)

        # REGISTER TO REGISTER MULTIPLY == a
        elif word0_second_half == 10:
            RAM[word0_first_half] *= RAM[word1]
            print('    MUL R[%s] R[%s]' %(word0_first_half, word1))
            manage_ram_slot_overunder_flow(word0_first_half)

        # REGISTER TO REGISTER DIVIDE == b
        elif word0_second_half == 11:
            RAM[word0_first_half] /= RAM[word1]
            print('    DIV R[%s] R[%s]' %(word0_first_half, word1))
            manage_ram_slot_overunder_flow(word0_first_half)

        # COMPARE REGISTER TO DIRECT  == c
        elif word0_second_half == 12:
            cmp_true = 'false'
            if RAM[word0_first_half] == word1:
                cmp_true = 'true'
                PC += 2
            print('    CMP R[%s] %s -> %s' %(word0_first_half, word1, cmp_true))

        # COMPARE REGISTER TO REGISTER == d
        elif word0_second_half == 13:
            cmp_true = 'false'
            if RAM[word0_first_half] == RAM[word1]:
                PC += 2
                cmp_true = 'true'

            print('    CMP R[%s] R[%s] -> %s' %(word0_first_half, word1, cmp_true))

        # CALL == e
        elif word0_second_half == 14:
            STACK.append(PC)

            manage_stack_size_overflow()

            index = len(STACK)
            a = STACK_FRAME_SIZE * (0 + index)
            b = STACK_FRAME_SIZE * (1 + index)
            RAM[a : b] = RAM[0 : STACK_FRAME_SIZE]
            PC = word1
            print('    CALL: Push %s to the Stack: PC -> %s' %(word1, word1))

        # RETURN == f
        elif word0_second_half == 15:
            index = len(STACK)

            manage_stack_size_overflow()

            a = STACK_FRAME_SIZE * (0 + index)
            b = STACK_FRAME_SIZE * (1 + index)
            RAM[0 : STACK_FRAME_SIZE] = RAM[a : b]
            PC = STACK.pop()
            print('    RETURN: Pop %s from the Stack: PC -> %s' %(PC, PC))

        # STRICT LESS THAN REGISTER TO DIRECT == 10
        elif word0_second_half == 16:
            is_this_true = 'false'
            if RAM[word0_first_half] < word1:
                is_this_true = 'true'
                PC += 2
            print('    LT R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

        # STRICT LESS THAN REGISTER TO REGISTER == 11
        elif word0_second_half == 17:
            is_this_true = 'false'
            if RAM[word0_first_half] < RAM[word1]:
                is_this_true = 'true'
                PC += 2
            print('    LT R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

        # LESS THAN OR EQUAL REGISTER TO DIRECT == 12
        elif word0_second_half == 18:
            is_this_true = 'false'
            if RAM[word0_first_half] <= word1:
                is_this_true = 'true'
                PC += 2
            print('    LTE R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

        # LESS THAN OR EQUAL REGISTER TO REGISTER == 13
        elif word0_second_half == 19:
            is_this_true = 'false'
            if RAM[word0_first_half] <= RAM[word1]:
                is_this_true = 'true'
                PC += 2
            print('    LTE R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

        # STRICT GREATER THAN REGISTER TO DIRECT == 14
        elif word0_second_half == 20:
            is_this_true = 'false'
            if RAM[word0_first_half] > word1:
                is_this_true = 'true'
                PC += 2
            print('    GT R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

        # STRICT GREATER THAN REGISTER TO REGISTER == 15
        elif word0_second_half == 21:
            is_this_true = 'false'
            if RAM[word0_first_half] > RAM[word1]:
                is_this_true = 'true'
                PC += 2
            print('    GT R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

        # GREATER THAN OR EQUAL REGISTER TO DIRECT == 16
        elif word0_second_half == 22:
            is_this_true = 'false'
            if RAM[word0_first_half] >= word1:
                is_this_true = 'true'
                PC += 2
            print('    GTE R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

        # GREATER THAN OR EQUAL REGISTER TO REGISTER == 17
        elif word0_second_half == 23:
            is_this_true = 'false'
            if RAM[word0_first_half] >= RAM[word1]:
                is_this_true = 'true'
                PC += 2
            print('    GTE R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

        # VRAM DIRECT LOAD == 18
        elif word0_second_half == 24:

            # load RAM slots 4096-4099
            r = RAM[4096]
            g = RAM[4097]
            b = RAM[4098]
            a = RAM[4099]

            # convert r,g,b,a to 4 byte hex string
            rgba_as_int = util.rgba_tuple_to_int(r,g,b,a)
            VRAM[word0_first_half] = rgba_as_int

            # draw

            x = word0_first_half % WIDTH_DISPLAY_PIXELS
            y = int((word0_first_half - x) / WIDTH_DISPLAY_PIXELS)

            # rgba_tuple = util.int_to_rgba_tuple(word1)
            rgba_tuple = (r,g,b,a)

            gfxdraw.pixel(gameDisplay, x, y, rgba_tuple)

            print('    LD V[%s] %s' %(word0_first_half, word1))




        # VRAM TO VRAM REGISTER LOAD == 19
        elif word0_second_half == 25:
            VRAM[word0_first_half] = VRAM[word1]

            # draw

            x = word0_first_half % WIDTH_DISPLAY_PIXELS
            y = int((word0_first_half - x) / WIDTH_DISPLAY_PIXELS)
            rgba_tuple = util.int_to_rgba_tuple(VRAM[word1])

            gfxdraw.pixel(gameDisplay, x, y, rgba_tuple)

            print('    LD V[%s] V[%s]' %(word0_first_half, word1))

        # RAM TO VRAM REGISTER LOAD == 20
        # stuff here...


        # EXIT VM == ffff
        elif word0_second_half == 2**16 - 1:
            EXIT_LOOP = True
            print('    EXIT')


        ########
        # VRAM #
        ########

        # exit pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_LOOP = True

        # debug prints
        print('')
        print('    %s'%ROM[PC])
        print('    %s'%ROM[PC+1])
        print('')
        print('    RAM[0-7]:    [%s, %s, %s, %s, %s, %s, %s, %s]' %(
            RAM[0], RAM[1], RAM[2], RAM[3], RAM[4], RAM[5], RAM[6], RAM[7])
        )
        print('    RAM[4096-4099]:  [%s, %s, %s, %s]' %(RAM[4096], RAM[4097], RAM[4098], RAM[4099]))
        print('    STACK:       %r' %STACK)
        print('    RAM[4100]:   %r  # return value' %RAM[4100])
        print('\n\n')

        # update frame
        pygame.display.update()

        if EXIT_LOOP:
            pygame.quit()
            util.slow_print('Exiting VM...', 0.11, print_empty_line=True)
            break


if __name__ == "__main__":
    hexfilename = 'hex/file.hex'
    hex_lines = util.return_lines_from_file(hexfilename)
    fill_ROM_with_hex_lines(hex_lines)
    validate_hex_file(hexfilename)

    exec(hex_lines)  # with pygame visualization
