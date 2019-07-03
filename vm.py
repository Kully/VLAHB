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

WIDTH_DISPLAY_PIXELS = 160
HEIGHT_DISPLAY_PIXELS = 120
pygame.init()
pygame.display.set_caption('VLAHB')
gameDisplay = pygame.display.set_mode((WIDTH_DISPLAY_PIXELS, HEIGHT_DISPLAY_PIXELS))


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

# Disable printing.
if False:
    def print(a):
        pass

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

def GOTO(PC, word1, word0_first_half):
    PC = word1
    print('    GOTO: PC -> %s' %word1)
    return PC

def DLD(PC, word1, word0_first_half):
    RAM[word0_first_half] = word1
    print('    LD R[%s] %s' %(word0_first_half, word1))
    return PC

def DADD(PC, word1, word0_first_half):
    RAM[word0_first_half] += word1
    print('    ADD R[%s] %s' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)
    return PC

def DSUB(PC, word1, word0_first_half):
    RAM[word0_first_half] -= word1
    print('    SUB R[%s] %s' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)
    return PC

def DMUL(PC, word1, word0_first_half):
    RAM[word0_first_half] *= word1
    print('    MUL R[%s] %s' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)
    return PC

def DDIV(PC, word1, word0_first_half):
    RAM[word0_first_half] /= word1
    print('    DIV R[%s] %s' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)
    return PC

def RRLD(PC, word1, word0_first_half):
    RAM[word0_first_half] = RAM[word1]
    print('    LD R[%s] R[%s]' %(word0_first_half, word1))
    return PC

def RRADD(PC, word1, word0_first_half):
    RAM[word0_first_half] += RAM[word1]
    print('    ADD R[%s] R[%s]' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)
    return PC

def RRSUB(PC, word1, word0_first_half):
    RAM[word0_first_half] -= RAM[word1]
    print('    SUB R[%s] R[%s]' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)
    return PC

def RRMUL(PC, word1, word0_first_half):
    RAM[word0_first_half] *= RAM[word1]
    print('    MUL R[%s] R[%s]' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)
    return PC

def RRDIV(PC, word1, word0_first_half):
    RAM[word0_first_half] /= RAM[word1]
    print('    DIV R[%s] R[%s]' %(word0_first_half, word1))
    manage_ram_slot_overunder_flow(word0_first_half)
    return PC

def CRD(PC, word1, word0_first_half):
    cmp_true = 'false'
    if RAM[word0_first_half] == word1:
        cmp_true = 'true'
        PC += 2
    print('    CMP R[%s] %s -> %s' %(word0_first_half, word1, cmp_true))
    return PC

def CRR(PC, word1, word0_first_half):
    cmp_true = 'false'
    if RAM[word0_first_half] == RAM[word1]:
        PC += 2
        cmp_true = 'true'
    print('    CMP R[%s] R[%s] -> %s' %(word0_first_half, word1, cmp_true))
    return PC

def CALL(PC, word1, word0_first_half):
    STACK.append(PC)
    manage_stack_size_overflow()
    index = len(STACK)
    a = STACK_FRAME_SIZE * (0 + index)
    b = STACK_FRAME_SIZE * (1 + index)
    RAM[a : b] = RAM[0 : STACK_FRAME_SIZE]
    PC = word1
    print('    CALL: Push %s to the Stack: PC -> %s' %(word1, word1))
    return PC

def RET(PC, word1, word0_first_half):
    manage_stack_size_overflow()
    index = len(STACK)
    a = STACK_FRAME_SIZE * (0 + index)
    b = STACK_FRAME_SIZE * (1 + index)
    RAM[0 : STACK_FRAME_SIZE] = RAM[a : b]
    PC = STACK.pop()
    print('    RETURN: Pop %s from the Stack: PC -> %s' %(PC, PC))
    return PC

def POP(PC, word1, word0_first_half):
    manage_stack_size_overflow()
    index = len(STACK)
    a = STACK_FRAME_SIZE * (0 + index)
    b = STACK_FRAME_SIZE * (1 + index)
    RAM[0 : STACK_FRAME_SIZE] = RAM[a : b]
    STACK.pop()
    print('    POP: Pop %s from the Stack' %(PC))
    return PC

def PUSH(PC, word1, word0_first_half):
    STACK.append(PC)
    manage_stack_size_overflow()
    index = len(STACK)
    a = STACK_FRAME_SIZE * (0 + index)
    b = STACK_FRAME_SIZE * (1 + index)
    RAM[a : b] = RAM[0 : STACK_FRAME_SIZE]
    print('    PUSH: Push %s to the Stack' %(word1))
    return PC

def SLRD(PC, word1, word0_first_half):
    is_this_true = 'false'
    if RAM[word0_first_half] < word1:
        is_this_true = 'true'
        PC += 2
    print('    LT R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))
    return PC

def SLRR(PC, word1, word0_first_half):
    is_this_true = 'false'
    if RAM[word0_first_half] < RAM[word1]:
        is_this_true = 'true'
        PC += 2
    print('    LT R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))
    return PC

def LTERD(PC, word1, word0_first_half):
    is_this_true = 'false'
    if RAM[word0_first_half] <= word1:
        is_this_true = 'true'
        PC += 2
    print('    LTE R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))
    return PC

def LTERR(PC, word1, word0_first_half):
    is_this_true = 'false'
    if RAM[word0_first_half] <= RAM[word1]:
        is_this_true = 'true'
        PC += 2
    print('    LTE R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))
    return PC

def SGRD(PC, word1, word0_first_half):
    is_this_true = 'false'
    if RAM[word0_first_half] > word1:
        is_this_true = 'true'
        PC += 2
    print('    GT R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))
    return PC

def SGRR(PC, word1, word0_first_half):
    is_this_true = 'false'
    if RAM[word0_first_half] > RAM[word1]:
        is_this_true = 'true'
        PC += 2
    print('    GT R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))
    return PC

def GTERD(PC, word1, word0_first_half):
    is_this_true = 'false'
    if RAM[word0_first_half] >= word1:
        is_this_true = 'true'
        PC += 2
    print('    GTE R[%s] %s -> %s' %(word0_first_half, word1, is_this_true))
    return PC

def GTERR(PC, word1, word0_first_half):
    is_this_true = 'false'
    if RAM[word0_first_half] >= RAM[word1]:
        is_this_true = 'true'
        PC += 2
    print('    GTE R[%s] R[%s] -> %s' %(word0_first_half, word1, is_this_true))
    return PC

def BLIT(PC, word1, word0_first_half):
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
    print('    BLIT')
    return PC

def DSQRT(PC, word1, word0_first_half):
    RAM[word0_first_half] = math.sqrt(word1)
    print('    SQRT R[%s] %s' %(word0_first_half, word1))
    return PC

def RRSQRT(PC, word1, word0_first_half):
    RAM[word0_first_half] = math.sqrt(RAM[word1])
    print('    SQRT R[%s] R[%s]' %(word0_first_half, word1))
    return PC

def DSIN(PC, word1, word0_first_half):
    RAM[word0_first_half] = math.sin(word1)
    print('    SIN R[%s] %s' %(word0_first_half, word1))
    return PC

def RRS(PC, word1, word0_first_half):
    RAM[word0_first_half] = math.sin(RAM[word1])
    print('    SIN R[%s] R[%s]' %(word0_first_half, word1))
    return PC

def DCOS(PC, word1, word0_first_half):
    RAM[word0_first_half] = math.cos(word1)
    print('    COS R[%s] %s' %(word0_first_half, word1))
    return PC

def RRC(PC, word1, word0_first_half):
    RAM[word0_first_half] = math.cos(RAM[word1])
    print('    COS R[%s] R[%s]' %(word0_first_half, word1))
    return PC

def UU0(PC, word1, word0_first_half):
    i = util.hex_to_int(ROM[PC][:4])
    j = util.hex_to_int(ROM[PC+1][:4])
    k = util.hex_to_int(ROM[PC+1][4:])
    RAM[i:j+1] = [k] * (j+1-i)
    print('    LD R[%s:%s] %s' %(i, j, k))
    return PC

def UU1(PC, word1, word0_first_half):
    i = util.hex_to_int(ROM[PC-2][:4])
    j = util.hex_to_int(ROM[PC+1 - 2][:4])
    k = util.hex_to_int(ROM[PC+1 - 2][4:])
    RAM[i:j+1] = [RAM[k]] * (j+1-i)
    print('    LD R[%s:%s] R[%s]' %(i, j, k))
    return PC

def UU2(PC, word1, word0_first_half):
    ram_span = util.hex_to_int(ROM[PC - 2][:4])  # ram_span := j-i
    i = util.hex_to_int(ROM[PC+1 - 2][:4])
    k = util.hex_to_int(ROM[PC+1 - 2][4:])
    RAM[i:i + ram_span+1] = RAM[k:k + ram_span+1]
    print('    LD R[%s:%s] R[%s:%s]' %(i, i+ram_span, k, k+ram_span))
    return PC

def FLOOR(PC, word1, word0_first_half):
    RAM[word1] = math.floor(RAM[word1])
    print('    FLOOR R[%s]' %word1)
    return PC

def CEIL(PC, word1, word0_first_half):
    RAM[word1] = math.ceil(RAM[word1])
    print('    CEIL R[%s]' %word1)
    return PC

def RAND(PC, word1, word0_first_half):
    RAM[word1] = random.choice([0, 1])
    print('    RAND R[%s]' %word1)
    return PC

def U0(PC, word1, word0_first_half):
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
    return PC

def U1(PC, word1, word0_first_half):
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
    return PC

def U2(PC, word1, word0_first_half):
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
    return PC

def U3(PC, word1, word0_first_half):
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
    return PC

def U4(PC, word1, word0_first_half):
    encoded_letters = util.int_to_hex(word0_first_half)
    i = encoded_letters[0]
    i = util.hex_digit_to_UVYZ[i]
    ram_index_i = util.UVYZ_to_ram_index[i]
    RAM[RAM[ram_index_i]] = RAM[word1]
    print('    LD R[%s] R[%s]' %(
        RAM[ram_index_i],
        word1,
        ))
    return PC

def U5(PC, word1, word0_first_half):
    encoded_letters = util.int_to_hex(word0_first_half)
    i = encoded_letters[0]
    i = util.hex_digit_to_UVYZ[i]
    ram_index_i = util.UVYZ_to_ram_index[i]
    RAM[RAM[ram_index_i]] = word1
    print('    LD R[%s] %s' %(
        RAM[ram_index_i],
        word1,
        ))
    return PC

def U6(PC, word1, word0_first_half):
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
    return PC

def EXIT(PC, word1, word0_first_half):
    print('    EXIT')
    exit(1)
    return PC

opcodes = [0] * (0xFFFF + 1)
opcodes[0x1] = GOTO
opcodes[0x2] = DLD
opcodes[0x3] = DADD
opcodes[0x4] = DSUB
opcodes[0x5] = DMUL
opcodes[0x6] = DDIV
opcodes[0x7] = RRLD
opcodes[0x8] = RRADD
opcodes[0x9] = RRSUB
opcodes[0xa] = RRMUL
opcodes[0xb] = RRDIV
opcodes[0xc] = CRD
opcodes[0xd] = CRR
opcodes[0xe] = CALL
opcodes[0xf] = RET
opcodes[0xfff0] = POP
opcodes[0xfff1] = PUSH
opcodes[0x10] = SLRD
opcodes[0x11] = SLRR
opcodes[0x12] = LTERD
opcodes[0x13] = LTERR
opcodes[0x14] = SGRD
opcodes[0x15] = SGRR
opcodes[0x16] = GTERD
opcodes[0x17] = GTERR
opcodes[0x18] = BLIT
opcodes[0x19] = DSQRT
opcodes[0x1a] = RRSQRT
opcodes[0x1b] = DSIN
opcodes[0x1c] = RRS
opcodes[0x1d] = DCOS
opcodes[0x1e] = RRC
opcodes[0x1f] = UU0
opcodes[0x20] = UU1
opcodes[0x21] = UU2
opcodes[0x22] = FLOOR
opcodes[0x23] = CEIL
opcodes[0x24] = RAND
opcodes[0x100] = U0
opcodes[0x101] = U1
opcodes[0x102] = U2
opcodes[0x103] = U3
opcodes[0x104] = U4
opcodes[0x105] = U5
opcodes[0x106] = U6
opcodes[0xffff] = EXIT

def exec(lines_from_file_hex):
    '''Execute lines in ROM'''

    clock = pygame.time.Clock()


    PC = starting_PC()  # program counter

    while True:

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

        PC += 2

        t0 = time.time()
        PC = opcodes[word0_second_half](PC, word1, word0_first_half)
        t1 = time.time()

        print(t1 - t0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(1)

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
