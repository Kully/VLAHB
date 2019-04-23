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

# Error Messages
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
