'''
Util Functions for VLAHB
'''
import sys
import time


def hex_to_int(h):
	return int(h, 16)


def int_to_hex(i):
    return hex(int(i))[2:]


def slow_print(msg, sleep_between_lines=0.02, sleep_after_msg=0.1, print_empty_line=False):
    '''only works for one line eg. strings with no \n'''
    for idx in range(1, len(msg) + 1):
        sys.stdout.write('\r %s' %msg[:idx])
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
    'COMPARE REGISTER TO VALUE': 'c',
    'COMPARE REGISTER TO REGISTER': 'd',
    'CALL': 'e',
    'RETURN': 'f',
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

# ASM
goto_exception_msg = (
    '\nThe Opcode GOTO must be followed by 1 argument in '
    'the form:\n    GOTO X\n where X is the new PC that you '
    'want to go to'
)

call_exception_msg = (
    '\nThe Opcode CALL must be followed by 1 argument in '
    'the form:\n    CALL LABEL\n where LABEL is the function '
    ' name to move the PC to'
)

return_exception_msg = (
    '\nThe Opcode RETURN requires no arguments afterwards'
)

general_exception_msg = (
    '\nThe Opcode {opcode} must be followed by 2 arguments '
    'either in the form:\n    {opcode} R[X] R[Y]\nor\n'
    '    {opcode} R[X] Y'
)

label_defined_more_than_once_exception_msg = (
    '\nThe Label {label} is defined more than once. '
    'Labels can only be defined once.'
)
