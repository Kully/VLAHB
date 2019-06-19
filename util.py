'''
Util Functions for VLAHB
'''
import sys
import time


def hex_to_int(h):
	return int(h, 16)


def int_to_hex(i):
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
    'CALL': 'e',
    'RETURN': 'f',
    'LESS THAN REGISTER TO DIRECT': '10',
    'LESS THAN REGISTER TO REGISTER': '11',
    'LESS THAN OR EQUAL REGISTER TO DIRECT': '12',
    'LESS THAN OR EQUAL REGISTER TO REGISTER': '13',
    'STRICT GREATER THAN REGISTER TO DIRECT': '14',
    'STRICT GREATER THAN REGISTER TO REGISTER': '15',
    'GREATER THAN OR EQUAL REGISTER TO DIRECT': '16',
    'GREATER THAN OR EQUAL REGISTER TO REGISTER': '17',
    'VRAM DIRECT LOAD': '18',
    'VRAM REGISTER TO REGISTER LOAD': '19',
    'EXIT': 'ffff',
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

TWO_ARGS_EXCEPTION_MSG = (
    '\nThe Opcode {opcode} must be followed by 2 arguments '
    'either in the form:\n    {opcode} R[X] R[Y]\nor\n'
    '    {opcode} R[X] Y'
)

LD_EXCEPTION_MSG = (
    '\nThe Opcode LD is used to load values into RAM slots or '
    'VRAM slots. LD must be followed by 2 arguments exactly:'
    ''
    'Syntax for RAM:'
    ''
    '    1. LD R[i] j'
    '    2. LD R[i] R[j]'
    ''
    'Syntax for VRAM:'
    ''
    '    1. LD V[i] j,k,l,m'
    '    2. LD V[i] V[j]'
    '    3. LD R[i] R[j],R[k],R[l],R[m]'
    ''
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
REGEX_LABEL_PATTERN = r' *[A-Z|\d|_]+:'
REGEX_RGBA_PATTERN = r'\d{1,3},\d{1,3},\d{1,3},\d{1,3}'
REGEX_VRAM_FROM_RAM_PATTERN = r'R\[\d+],R\[\d+],R\[\d+],R\[\d+]'
