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
    'GOTO R[i]': '2',
    'DIRECT LOAD': '3',
    'DIRECT ADD': '4',
    'DIRECT SUBTRACT': '5',
    'DIRECT MULTIPLY': '6',
    'DIRECT DIVIDE': '7',
    'REGISTER TO REGISTER LOAD': '8',
    'REGISTER TO REGISTER ADD': '9',
    'REGISTER TO REGISTER SUBTRACT': 'a',
    'REGISTER TO REGISTER MULTIPLY': 'b',
    'REGISTER TO REGISTER DIVIDE': 'c',
    'COMPARE REGISTER TO DIRECT': 'd',
    'COMPARE REGISTER TO REGISTER': 'e',
    'COMPARE UV TO DIRECT': 'f',
    'CALL': '10',
    'CALL R[i]': '11',
    'RETURN': '12',
    'LESS THAN REGISTER TO DIRECT': '13',
    'LESS THAN REGISTER TO REGISTER': '14',
    'LESS THAN OR EQUAL REGISTER TO DIRECT': '15',
    'LESS THAN OR EQUAL REGISTER TO REGISTER': '16',
    'STRICT GREATER THAN REGISTER TO DIRECT': '17',
    'STRICT GREATER THAN REGISTER TO REGISTER': '18',
    'GREATER THAN OR EQUAL REGISTER TO DIRECT': '19',
    'GREATER THAN OR EQUAL REGISTER TO REGISTER': '1a',
    'BLIT': '1b',
    'RAND': '1c',
    'LD ARRAY TO VRAM': '1d',
    'LD ARRAY PC TO REGISTER': '1e',
    'LD REGISTERS TO VRAM': '1f',
    'LD R[U] R[V]': '20',
    'LD R[U:V] R[Y]': '21',
    'LD R[U:V] R[Y:Z]': '22',
    'LD R[U:V] R[i]': '23',
    'LD R[U] R[i]': '24',
    'LD R[U] i': '25',
    'LD R[U:V] i': '26',
    'LD REGISTERS TO VRAM W VRAM INDEX': '27',
    'LD R[i] R[U]': '28',
    'POP': '29',
    'PUSH': '2a',
    'INPUT': '2b',
    'SHT': '2c',
    'WAIT': '2d',
    'REGISTER TO REGISTER REMAINDER': '2e',
    'DIRECT REMAINDER': '2f',
    'EXIT': 'ff',
}

pointer_label_to_slot_index = {
    'U': '4096',
    'V': '4097',
    'Y': '4098',
    'Z': '4099',
}
