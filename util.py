'''
Util Functions for VLAHB
'''
import re
import sys
import time


def hex_to_int(h):
	return int(h, 16)


def int_to_hex(i):
    if re.match(REGEX_HEX, str(i)):
        i = int(i, 16)

    return hex(int(i))[2:]


def int_to_rgba_tuple(i):
    '''eg. 146581 -> (240,0,150,255)'''
    color_hex = int_to_hex(i).zfill(8)

    return (
        hex_to_int(color_hex[ :2]),
        hex_to_int(color_hex[2:4]),
        hex_to_int(color_hex[4:6]),
        hex_to_int(color_hex[6: ]),
    )

def rgba_tuple_to_int(r,g,b,a):
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    if a > 255:
        a = 255

    r_hex = int_to_hex(r).zfill(2)
    g_hex = int_to_hex(g).zfill(2)
    b_hex = int_to_hex(b).zfill(2)
    a_hex = int_to_hex(a).zfill(2)
    rgba_hex = r_hex + g_hex + b_hex + a_hex

    return hex_to_int(rgba_hex)


def slow_print(msg, sleep_between_lines=0.02, sleep_after_msg=0.1,
               print_empty_line=False):
    '''only works for one line eg. strings with no \n'''
    for idx in range(1, len(msg) + 1):
        sys.stdout.write('\r%s' %msg[:idx])
        sys.stdout.flush()
        time.sleep(sleep_between_lines)
    if print_empty_line:
        time.sleep(sleep_after_msg)
        print('\n')


def return_lines_from_file(file_hex, remove_empty_lines=True):
    f = open(file_hex, 'r')
    lines = f.read().split('\n')

    if remove_empty_lines:
        while '' in lines:
            lines.remove('')
    f.close()
    return lines


UVYZ_to_hex_digit = {
    'U': '1',
    'V': '2',
    'Y': '3',
    'Z': '4',
}


hex_digit_to_UVYZ = {
    '1': 'U',
    '2': 'V',
    '3': 'Y',
    '4': 'Z', 
}


UVYZ_to_ram_index = {
    'U': 4096,
    'V': 4097,
    'Y': 4098,
    'Z': 4099,
}


# TODO - match the terminology across op_codes_dict,
# comments above opcodes in vm.py, and the README.md
# 
# eg. REGISTER TO VALUE -> REGISTER TO DIRECT
# 
op_codes_dict = {
    'GOTO': '1',
    'DIRECT LOAD': '2',
    'DIRECT ADD': '3',
    'DIRECT SUBTRACT': '4',
    'DIRECT MULTIPLY': '5',
    'DIRECT DIVIDE': '6',
    'REGISTER TO REGISTER LOAD': '7',
    'REGISTER TO REGISTER ADD': '8',
    'REGISTER TO REGISTER SUBTRACT': '9',
    'REGISTER TO REGISTER MULTIPLY': 'a',
    'REGISTER TO REGISTER DIVIDE': 'b',
    'COMPARE REGISTER TO DIRECT': 'c',
    'COMPARE REGISTER TO REGISTER': 'd',
    'CALL': 'e',  # PUSH + GOTO
    'RETURN': 'f', # POP + GOTO
    'LESS THAN REGISTER TO DIRECT': '10',
    'LESS THAN REGISTER TO REGISTER': '11',
    'LESS THAN OR EQUAL REGISTER TO DIRECT': '12',
    'LESS THAN OR EQUAL REGISTER TO REGISTER': '13',
    'STRICT GREATER THAN REGISTER TO DIRECT': '14',
    'STRICT GREATER THAN REGISTER TO REGISTER': '15',
    'GREATER THAN OR EQUAL REGISTER TO DIRECT': '16',
    'GREATER THAN OR EQUAL REGISTER TO REGISTER': '17',
    'BLIT': '18',
    'DIRECT SQRT': '19',
    'REGISTER TO REGISTER SQRT': '1a',
    'DIRECT SIN': '1b',
    'REGISTER TO REGISTER SIN': '1c',
    'DIRECT COS': '1d',
    'REGISTER TO REGISTER COS': '1e',
    'LD R[i:j] k': '1f',
    'LD R[i:j] R[k]': '20',
    'LD R[i:j] R[k:l]': '21',
    'FLOOR': '22',
    'CEIL': '23',
    'RAND': '24',
    # U,V,Y,Z
    'LD R[U] R[V]': '100',
    'LD R[U] R[i]': '104',
    'LD R[U] i': '105',
    'LD R[U:V] R[i]': '103',
    'LD R[U:V] i': '106',
    'LD R[U:V] R[Y]': '101',
    'LD R[U:V] R[Y:Z]': '102',
    'POP': 'fff0',
    'PUSH': 'fff1',
    'EXIT': 'ffff',
}

pointer_label_to_slot_index = {
    'U': '4096',
    'V': '4097',
    'Y': '4098',
    'Z': '4099',
}

# Error Messages
# HEX
EVEN_NUMBER_OF_HEX_LINES_ERROR_MSG = (
	'file.hex must contain exactly an even number of lines'
)
CORRECT_HEX_LINE_PREFIX_ERROR_MSG = (
	'all of lines in file.hex must start with "0x"'
)
CHARS_PER_LINE_ERROR_MSG = (
	'all lines in file.hex must be 8 characters long'
)
VALID_HEX_VALUES_ERROR_MSG = (
	'all characters of file.hex must be a hexidecimal value from 0-f'
)

STACK_OVERFLOW_ERROR_MSG = (
    'stack overflow: the maximum size of the stack is {}'    
)

# ASM
NO_FILE_FOUND_EXCEPTION_MSG = (
    '"{}" is not a file in the /asm folder.\n\nHere is a list '
    'of assembly files in this folder:\n{}'
)

GOTO_EXCEPTION_MSG = (
    '\nThe Opcode GOTO must be followed by 1 argument in '
    'the form:\n    GOTO X\n where X is the new PC that you '
    'want to go to'
)

CALL_EXCEPTION_MSG = (
    '\nThe Opcode CALL must be followed by 1 argument in '
    'the form:\n    CALL LABEL\n where LABEL is the function '
    ' name to move the PC to'
)

RETURN_EXCEPTION_MSG = (
    '\nThe Opcode RETURN requires no arguments afterwards'
)

POP_PUSH_EXCEPTION_MSG = (
    '\nThe Opcode {opcode} requires no arguments afterwards'
)


TWO_ARGS_EXCEPTION_MSG = (
    '\nThe Opcode {opcode} must be followed by 2 arguments '
    'either in the form:\n    {opcode} R[X] R[Y]\nor\n'
    '    {opcode} R[X] Y'
)

ONE_ARG_EXCEPTION_MSG = (
    '\nThe Opcode {opcode} must be followed by 1 argument '
    'in the form:\n    {opcode} R[X] where X is an int'
)

# TODO: update the syntax in error message below
LD_EXCEPTION_MSG = (
    '\nThe Opcode LD is used to load values into RAM slots\nLD '
    'must be followed by 2 exactly arguments:'
    '\n'
    '\nSyntax:'
    '\n    1. LD R[i] j'
    '\n    2. LD R[i] R[j]'
    '\n    3. LD R[i:j] x'
    '\n    4. LD R[i:j] R[k:l]'
    '\n'
)

LD_VRAM_EXCEPTION_MSG = (
    '\nWhen loading VRAM, LD must be followed by 2 arguments '
    'either in the form:\n    LD V[X] V[Y]\nor\n'
    '    LD V[X] (R,G,B,A) for direct load and where '
    'R,G,B,A are between 0 and 255 inclusive'
)

LABEL_DEFINED_MORE_THAN_ONCE_EXCEPTION_MSG = (
    '\nThe Label {label} is defined more than once. '
    'Labels can only be defined once across all asm files in ./asm'
)

# regex
REGEX_LABEL_PATTERN = r'[\t ]*[A-Z|\d|_]+:'
REGEX_RGBA_PATTERN = r'\d{1,3},\d{1,3},\d{1,3},\d{1,3}'
REGEX_LD_R_ONE = r'R\[\d+]'
REGEX_LD_R_RANGE = r'R\[\d+:\d+]'
REGEX_HEX = r'0X[0-9a-fA-F]+'

# for LD R[U:V] R[Z]
REGEX_UV_ONE_AND_ONE = r'R\[([UVYZ])] R\[([UVYZ])]'
REGEX_UV_ONE = r'R\[([UVYZ])]'
REGEX_UV_TWO = r'R\[([UVYZ]):([UVYZ])]'
