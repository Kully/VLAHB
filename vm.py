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

def starting_PC():
    f = open('start_pc.txt', 'r')
    PC = int(f.readlines()[0])
    f.close()
    return PC


# CPU constants and data structures

COMMANDS_PER_SEC = 10
DELAY_BETWEEN_COMMANDS = 1. / COMMANDS_PER_SEC  # in seconds

RAM_NUM_OF_SLOTS = 128000  # 512KB == Bill Gates Number
MAX_RAM_VALUE = 2**32 - 1  # largest value in a slot of RAM (hhhh hhhh) - 4 bytes
RAM = [0] * RAM_NUM_OF_SLOTS
PC = starting_PC()  # program counter

pygame.init()
pygame.display.set_caption('VLAHB')
WIDTH_DISPLAY_PIXELS = 160
HEIGHT_DISPLAY_PIXELS = 120
gameDisplay = pygame.display.set_mode((WIDTH_DISPLAY_PIXELS, HEIGHT_DISPLAY_PIXELS))

STACK = []
STACK_FRAME_SIZE = 128
STACK_MAX_SIZE = 32

ROM = []


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

# GOTO == 0001
def GOTO(word0_first_half, word1):
    global PC
    PC = word1
    print('    GOTO: PC -> %s' %word1)

def DIRECT_LOAD(word0_first_half, word1): # 0002
    RAM[word0_first_half] = word1
    print('    LD R[%s] %s' %(word0_first_half, word1))

def DIRECT_ADD(word0_first_half, word1): #3
    RAM[word0_first_half] += word1
    print('    ADD R[%s] %s' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)

def DIRECT_SUBTRACT(word0_first_half, word1): # 0004
    RAM[word0_first_half] -= word1
    print('    SUB R[%s] %s' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)

def DIRECT_MULTIPLY(word0_first_half, word1): # 0005
    RAM[word0_first_half] *= word1
    print('    MUL R[%s] %s' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)

def DIRECT_DIVIDE(word0_first_half, word1): # 0006
    RAM[word0_first_half] /= word1
    print('    DIV R[%s] %s' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)

def REGISTER_TO_REGISTER_LOAD(word0_first_half, word1): #0007
    RAM[word0_first_half] = RAM[word1]
    print('    LD R[%s] R[%s]' %(word0_first_half, word1))

def REGISTER_TO_REGISTER_ADD(word0_first_half, word1): # 0008
    RAM[word0_first_half] += RAM[word1]
    print('    ADD R[%s] R[%s]' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)

def REGISTER_TO_REGISTER_SUBTRACT(word0_first_half, word1): #0009
    RAM[word0_first_half] -= RAM[word1]
    print('    SUB R[%s] R[%s]' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)

def REGISTER_TO_REGISTER_MULTIPLY(word0_first_half, word1): #000a
    RAM[word0_first_half] *= RAM[word1]
    print('    MUL R[%s] R[%s]' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)

def REGISTER_TO_REGISTER_DIVIDE(word0_first_half, word1): # 000b
    RAM[word0_first_half] /= RAM[word1]
    print('    DIV R[%s] R[%s]' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)

def COMPARE_REGISTER_TO_DIRECT(word0_first_half, word1): #== 000c
    global PC
    cmp_true = 'false'
    if RAM[word0_first_half] == word1:
        cmp_true = 'true'
        PC += 2
    print('    CMP R[%s] %s -> %s' %(word0_first_half, word1, cmp_true))

def COMPARE_REGISTER_TO_REGISTER(word0_first_half, word1): #== 000d
    global PC
    cmp_true = 'false'
    if RAM[word0_first_half] == RAM[word1]:
        PC += 2
        cmp_true = 'true'
    print('    CMP R[%s] R[%s] -> %s' %(word0_first_half, word1, cmp_true))

def CALL(word0_first_half, word1): #== 000e
    global PC
    STACK.append(PC)
    manage_stack_size_overflow()
    index = len(STACK)
    a = STACK_FRAME_SIZE * (0 + index)
    b = STACK_FRAME_SIZE * (1 + index)
    RAM[a : b] = RAM[0 : STACK_FRAME_SIZE]
    PC = word1
    print('    CALL: Push %s to the Stack: PC -> %s' %(word1, word1))

def RETURN(word0_first_half, word1): #== 000f
    global PC
    manage_stack_size_overflow()
    index = len(STACK)
    a = STACK_FRAME_SIZE * (0 + index)
    b = STACK_FRAME_SIZE * (1 + index)
    RAM[0 : STACK_FRAME_SIZE] = RAM[a : b]
    PC = STACK.pop()
    print('    RETURN: Pop %s from the Stack: PC -> %s' %(PC, PC))

def POP(word0_first_half, word1): #== fff0
    manage_stack_size_overflow()
    index = len(STACK)
    a = STACK_FRAME_SIZE * (0 + index)
    b = STACK_FRAME_SIZE * (1 + index)
    RAM[0 : STACK_FRAME_SIZE] = RAM[a : b]
    STACK.pop()
    print('    POP: Pop %s from the Stack' %(PC))

def PUSH(word0_first_half, word1): #== fff1
    global PC
    STACK.append(PC)
    manage_stack_size_overflow()
    index = len(STACK)
    a = STACK_FRAME_SIZE * (0 + index)
    b = STACK_FRAME_SIZE * (1 + index)
    RAM[a : b] = RAM[0 : STACK_FRAME_SIZE]
    print('    PUSH: Push %s to the Stack' %(word1))

def STRICT_LESS_THAN_REGISTER_TO_DIRECT(word0_first_half, word1): #== 0010
    global PC
    is_this_true = 'false'
    if RAM[word0_first_half] < word1:
        is_this_true = 'true'
        PC += 2
    print('    LT R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

def STRICT_LESS_THAN_REGISTER_TO_REGISTER(word0_first_half, word1): #== 0011
    global PC
    is_this_true = 'false'
    if RAM[word0_first_half] < RAM[word1]:
        is_this_true = 'true'
        PC += 2
    print('    LT R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

def LESS_THAN_OR_EQUAL_REGISTER_TO_DIRECT(word0_first_half, word1): #== 0012
    global PC
    is_this_true = 'false'
    if RAM[word0_first_half] <= word1:
        is_this_true = 'true'
        PC += 2
    print('    LTE R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

def LESS_THAN_OR_EQUAL_REGISTER_TO_REGISTER(word0_first_half, word1): #== 0013
    global PC
    is_this_true = 'false'
    if RAM[word0_first_half] <= RAM[word1]:
        is_this_true = 'true'
        PC += 2
    print('    LTE R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

def STRICT_GREATER_THAN_REGISTER_TO_DIRECT(word0_first_half, word1): #== 0014
    global PC
    is_this_true = 'false'
    if RAM[word0_first_half] > word1:
        is_this_true = 'true'
        PC += 2
    print('    GT R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

def STRICT_GREATER_THAN_REGISTER_TO_REGISTER(word0_first_half, word1): #== 0015
    global PC
    is_this_true = 'false'
    if RAM[word0_first_half] > RAM[word1]:
        is_this_true = 'true'
        PC += 2
    print('    GT R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

def GREATER_THAN_OR_EQUAL_REGISTER_TO_DIRECT(word0_first_half, word1): #== 0016
    global PC
    is_this_true = 'false'
    if RAM[word0_first_half] >= word1:
        is_this_true = 'true'
        PC += 2
    print('    GTE R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))

def GREATER_THAN_OR_EQUAL_REGISTER_TO_REGISTER(word0_first_half, word1): #== 0017
    global PC
    is_this_true = 'false'
    if RAM[word0_first_half] >= RAM[word1]:
        is_this_true = 'true'
        PC += 2
    print('    GTE R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))

def BLIT(word0_first_half, word1): #== 0018
    surf = pygame.Surface((WIDTH_DISPLAY_PIXELS, HEIGHT_DISPLAY_PIXELS))
    surf.lock()
    for x in range(WIDTH_DISPLAY_PIXELS):
        for y in range(HEIGHT_DISPLAY_PIXELS):
            rgba_tuple = util.int_to_rgba_tuple(RAM[4101 + x + y*WIDTH_DISPLAY_PIXELS])
            surf.set_at((x, y), rgba_tuple)
    surf.unlock()
    gameDisplay.blit(surf, (0, 0))
    pygame.display.update()
    print('    BLIT')

def DIRECT_SQRT(word0_first_half, word1): #== 0019
    RAM[word0_first_half] = math.sqrt(word1)
    print('    SQRT R[%s] %s' %(word0_first_half, word1))

def REGISTER_TO_REGISTER_SQRT(word0_first_half, word1):#== 001a
    RAM[word0_first_half] = math.sqrt(RAM[word1])
    print('    SQRT R[%s] R[%s]' %(word0_first_half, word1))

def DIRECT_SIN(word0_first_half, word1): # == 001b
    RAM[word0_first_half] = math.sin(word1)
    print('    SIN R[%s] %s' %(word0_first_half, word1))

def REGISTER_TO_REGISTER_SIN(word0_first_half, word1): #== 001c
    RAM[word0_first_half] = math.sin(RAM[word1])
    print('    SIN R[%s] R[%s]' %(word0_first_half, word1))

def DIRECT_COS(word0_first_half, word1): #== 001d
    RAM[word0_first_half] = math.cos(word1)
    print('    COS R[%s] %s' %(word0_first_half, word1))

def REGISTER_TO_REGISTER_COS(word0_first_half, word1): # 001e
    RAM[word0_first_half] = math.cos(RAM[word1])
    print('    COS R[%s] R[%s]' %(word0_first_half, word1))

def LD0(word0_first_half, word1): # R[i:j] k == 001f
    global PC
    i = util.hex_to_int(ROM[PC][:4])
    j = util.hex_to_int(ROM[PC+1][:4])
    k = util.hex_to_int(ROM[PC+1][4:])
    RAM[i:j+1] = [k] * (j+1-i)
    print('    LD R[%s:%s] %s' %(i, j, k))

def LD1(word0_first_half, word1): #R[i:j] R[k] == 0020
    global PC
    i = util.hex_to_int(ROM[PC-2][:4])
    j = util.hex_to_int(ROM[PC+1 - 2][:4])
    k = util.hex_to_int(ROM[PC+1 - 2][4:])
    RAM[i:j+1] = [RAM[k]] * (j+1-i)
    print('    LD R[%s:%s] R[%s]' %(i, j, k))

def LD2(word0_first_half, word1): #R[i:j] R[k:l] == 0021
    global PC
    ram_span = util.hex_to_int(ROM[PC - 2][:4])  # ram_span := j-i
    i = util.hex_to_int(ROM[PC+1 - 2][:4])
    k = util.hex_to_int(ROM[PC+1 - 2][4:])
    RAM[i:i + ram_span+1] = RAM[k:k + ram_span+1]
    print('    LD R[%s:%s] R[%s:%s]' %(i, i+ram_span, k, k+ram_span))

def FLOOR(word0_first_half, word1): #== 0022
    RAM[word1] = math.floor(RAM[word1])
    print('    FLOOR R[%s]' %word1)

def CEIL(word0_first_half, word1): #== 0023
    RAM[word1] = math.ceil(RAM[word1])
    print('    CEIL R[%s]' %word1)

def RAND(word0_first_half, word1): # == 0024
    RAM[word1] = random.choice([0, 1])
    print('    RAND R[%s]' %word1)

# LD R[V] R[Z] == 0100
# LD R[R[i]] R[R[j]]
def UNKNOWN0(word0_first_half, word1):
    encoded_letters = util.int_to_hex(word0_first_half)
    i = encoded_letters[0]
    j = encoded_letters[1]
    i = util.hex_digit_to_UVYZ[i]
    j = util.hex_digit_to_UVYZ[j]
    ram_index_i = util.UVYZ_to_ram_index[i]
    ram_index_j = util.UVYZ_to_ram_index[j]
    RAM[RAM[ram_index_i]] = RAM[RAM[ram_index_j]]
    print('    LD R[%s] R[%s]' %(
        RAM[ram_index_i],
        RAM[ram_index_j],
        ))

# LD R[V:U] R[Z] == 0101
# LD R[R[i]:R[j]] R[R[k]]
def UNKNOWN1(word0_first_half, word1):
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
    print('    LD R[%s:%s] R[%s]' %(
        RAM[ram_index_i],
        RAM[ram_index_j],
        RAM[ram_index_k],
        ))

# LD R[U:V] R[Y:Z] == 0102
# LD R[R[i]:R[j]] R[R[k]:R[l]]
def UNKNOWN2(word0_first_half, word1):
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
    print('    LD R[%s:%s] R[%s:%s]' %(
        RAM[ram_index_i],
        RAM[ram_index_j],
        RAM[ram_index_k],
        RAM[ram_index_l],
        ))

# LD R[U:V] R[k] == 0103
# LD R[R[i]:R[j]] R[k]
def UNKNOWN3(word0_first_half, word1):
    encoded_letters = util.int_to_hex(word0_first_half)
    i = encoded_letters[0]
    j = encoded_letters[1]
    i = util.hex_digit_to_UVYZ[i]
    j = util.hex_digit_to_UVYZ[j]
    ram_index_i = util.UVYZ_to_ram_index[i]
    ram_index_j = util.UVYZ_to_ram_index[j]
    array_span = len(RAM[RAM[ram_index_i]:RAM[ram_index_j]])
    RAM[RAM[ram_index_i]:RAM[ram_index_j]] = [RAM[word1]] * array_span
    print('    LD R[%s:%s] R[%s]' %(
        RAM[ram_index_i],
        RAM[ram_index_j],
        word1,
        ))

# LD R[U] R[i] == 0104
def UNKNOWN4(word0_first_half, word1):
    encoded_letters = util.int_to_hex(word0_first_half)
    i = encoded_letters[0]
    i = util.hex_digit_to_UVYZ[i]
    ram_index_i = util.UVYZ_to_ram_index[i]
    RAM[RAM[ram_index_i]] = RAM[word1]
    print('    LD R[%s] R[%s]' %(
        RAM[ram_index_i],
        word1,
        ))

# LD R[U] i == 0105
def UNKNOWN5(word0_first_half, word1):
    encoded_letters = util.int_to_hex(word0_first_half)
    i = encoded_letters[0]
    i = util.hex_digit_to_UVYZ[i]
    ram_index_i = util.UVYZ_to_ram_index[i]
    RAM[RAM[ram_index_i]] = word1
    print('    LD R[%s] %s' %(
        RAM[ram_index_i],
        word1,
        ))

#  LD R[U:V] i
def UNKNOWN6(word0_first_half, word1): # 0106
    encoded_letters = util.int_to_hex(word0_first_half)
    u = encoded_letters[0]
    u = util.hex_digit_to_UVYZ[u]
    v = encoded_letters[1]
    v = util.hex_digit_to_UVYZ[v]
    ram_index_u = util.UVYZ_to_ram_index[u]
    ram_index_v = util.UVYZ_to_ram_index[v]
    array_span = len(RAM[RAM[ram_index_u] : RAM[ram_index_v]])
    RAM[RAM[ram_index_u] : RAM[ram_index_v]] = [word1] * array_span
    print('    LD R[%s:%s] %s' %(
        RAM[ram_index_u],
        RAM[ram_index_v],
        word1,
        ))

def EXIT(word0_first_half, word1): #ffff
    exit(1)
    print('    EXIT')

opcodes = [0] * 65536
opcodes[0x1] = GOTO # 01
opcodes[0x2] = DIRECT_LOAD # 0002
opcodes[0x3] = DIRECT_ADD #3
opcodes[0x4] = DIRECT_SUBTRACT # 0004
opcodes[0x5] = DIRECT_MULTIPLY # 0005
opcodes[0x6] = DIRECT_DIVIDE # 0006
opcodes[0x7] = REGISTER_TO_REGISTER_LOAD #0007
opcodes[0x8] = REGISTER_TO_REGISTER_ADD # 0008
opcodes[0x9] = REGISTER_TO_REGISTER_SUBTRACT #0009
opcodes[0xa] = REGISTER_TO_REGISTER_MULTIPLY #000a
opcodes[0xb] = REGISTER_TO_REGISTER_DIVIDE # 000b
opcodes[0xc] = COMPARE_REGISTER_TO_DIRECT #== 000c
opcodes[0xd] = COMPARE_REGISTER_TO_REGISTER #== 000d
opcodes[0xe] = CALL #== 000e
opcodes[0xf] = RETURN #== 000f
opcodes[0xfff0] = POP #== fff0
opcodes[0xfff1] = PUSH #== fff1
opcodes[0x10] = STRICT_LESS_THAN_REGISTER_TO_DIRECT #== 0010
opcodes[0x11] = STRICT_LESS_THAN_REGISTER_TO_REGISTER #== 0011
opcodes[0x12] = LESS_THAN_OR_EQUAL_REGISTER_TO_DIRECT #== 0012
opcodes[0x13] = LESS_THAN_OR_EQUAL_REGISTER_TO_REGISTER #== 0013
opcodes[0x14] = STRICT_GREATER_THAN_REGISTER_TO_DIRECT #== 0014
opcodes[0x15] = STRICT_GREATER_THAN_REGISTER_TO_REGISTER #== 0015
opcodes[0x16] = GREATER_THAN_OR_EQUAL_REGISTER_TO_DIRECT #== 0016
opcodes[0x17] = GREATER_THAN_OR_EQUAL_REGISTER_TO_REGISTER #== 0017
opcodes[0x18] = BLIT #== 0018
opcodes[0x19] = DIRECT_SQRT #== 0019
opcodes[0x1a] = REGISTER_TO_REGISTER_SQRT#== 001a
opcodes[0x1b] = DIRECT_SIN # == 001b
opcodes[0x1c] = REGISTER_TO_REGISTER_SIN #== 001c
opcodes[0x1d] = DIRECT_COS #== 001d
opcodes[0x1e] = REGISTER_TO_REGISTER_COS # 001e
opcodes[0x1f] = LD0 # R[i:j] k == 001f
opcodes[0x20] = LD1 #R[i:j] R[k] == 0020
opcodes[0x21] = LD2 #R[i:j] R[k:l] == 0021
opcodes[0x22] = FLOOR #== 0022
opcodes[0x23] = CEIL #== 0023
opcodes[0x24] = RAND # == 0024
opcodes[0x100] = UNKNOWN0 # == 0100
opcodes[0x101] = UNKNOWN1 # LD R[V:U] R[Z] == 0101
opcodes[0x102] = UNKNOWN2 # LD R[U:V] R[Y:Z] == 0102
opcodes[0x103] = UNKNOWN3 # LD R[U:V] R[k] == 0103
opcodes[0x104] = UNKNOWN4 # LD R[U] R[i] == 0104
opcodes[0x105] = UNKNOWN5 # LD R[U] i == 0105
opcodes[0x106] = UNKNOWN6 # 0106
opcodes[0xffff] = EXIT #ffff

def exec(lines_from_file_hex):
    '''Execute lines in ROM'''
    global PC
    clock = pygame.time.Clock()

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
        word0_second_half = util.hex_to_int(ROM[PC][4:]) # index.
        word1 = util.hex_to_int(ROM[PC+1])

        opcodes[word0_second_half](word0_first_half, word1)

        PC += 2

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


if __name__ == "__main__":
    hexfilename = 'hex/file.hex'
    hex_lines = util.return_lines_from_file(hexfilename)
    fill_ROM_with_hex_lines(hex_lines)
    validate_hex_file(hexfilename)

    exec(hex_lines)  # with pygame visualization
