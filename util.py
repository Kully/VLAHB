'''
Util Functions for VLAHB
'''
import re
import sys
import time


#########
# REGEX #
#########

REGEX_LABEL_AND_COLON = r'[\t ]*([A-Za-z_]{1}[A-Za-z_\d]{1,}):'
REGEX_LABEL = r'([A-Za-z_]{1}[A-Za-z_\d]{1,})'

REGEX_LD_R_ONE = r'R\[\d+]'
REGEX_HEX = r'0X[0-9a-fA-F]+'
REGEX_INT = r'[0-9]+'
REGEX_HEX_WITH_SPACE_BEFORE = r'[\t ]*0X[0-9a-fA-F]+'

# for pointers U,V,Y,Z
REGEX_UV_ONE = r'R\[([UVYZ])]'
REGEX_UV_TWO = r'R\[([UVYZ]):([UVYZ])]'

# for arrays
REGEX_ARRAY_LD = r'([A-Za-z_]{1}[A-Za-z_\d]{1,}) R\[(\d+)\] R\[(\d+)\] (\d+) (\d+)'
REGEX_REGISTER_ONLY_ARRAY_LD = r'R\[([UVYZ])] R\[(\d+)\] R\[(\d+)\] R\[(\d+)\] R\[(\d+)\]'
REGEX_REGISTER_ONLY_VRAM_IDX_ARRAY_LD = r'R\[([UVYZ])] R\[(\d+)\] R\[(\d+)\] R\[(\d+)\]'
REGEX_LD_LABEL_PC = r'R\[(\d+)\] ([A-Za-z_]{1}[A-Za-z_\d]{1,})'


def hex_to_int(h):
	return int(h, 16)

def int_to_hex(i):
    if re.match(REGEX_HEX, str(i)):
        i = int(i, 16)

    return hex(int(i))[2:]

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

opcode_lookup_dict = {
    'GOTO': '1',
    'GOTO R[i]': '2e',
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
    'COMPARE UV TO DIRECT': '24',
    'CALL': 'e',
    'CALL R[i]': '2f',
    'RETURN': 'f',
    'LESS THAN REGISTER TO DIRECT': '10',
    'LESS THAN REGISTER TO REGISTER': '11',
    'LESS THAN OR EQUAL REGISTER TO DIRECT': '12',
    'LESS THAN OR EQUAL REGISTER TO REGISTER': '13',
    'STRICT GREATER THAN REGISTER TO DIRECT': '14',
    'STRICT GREATER THAN REGISTER TO REGISTER': '15',
    'GREATER THAN OR EQUAL REGISTER TO DIRECT': '16',
    'GREATER THAN OR EQUAL REGISTER TO REGISTER': '17',
    'BLIT': '18',
    'RAND': '19',
    'LD ARRAY TO VRAM': '1a',
    'LD ARRAY PC TO REGISTER': '1b',
    'LD REGISTERS TO VRAM': '1c',
    'LD R[U] R[V]': '1d',
    'LD R[U:V] R[Y]': '1e',
    'LD R[U:V] R[Y:Z]': '1f',
    'LD R[U:V] R[i]': '20',
    'LD R[U] R[i]': '21',
    'LD R[U] i': '22',
    'LD R[U:V] i': '23',
    'LD REGISTERS TO VRAM W VRAM INDEX': '2a',
    'LD R[i] R[U]': '2b',
    'POP': '25',
    'PUSH': '26',
    'INPUT': '27',
    'SHT': '28',
    'WAIT': '29',
    'REGISTER TO REGISTER REMAINDER': '2c',
    'DIRECT REMAINDER': '2d',
    'EXIT': 'ff',
}

pointer_label_to_slot_index = {
    'U': '4096',
    'V': '4097',
    'Y': '4098',
    'Z': '4099',
}
