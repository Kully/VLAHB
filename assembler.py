'''
Assembler: asm -> hex

Notes/Best Practices about ASM:
1. ALWAYS use LABELS - do not say GOTO 42
2. If you do not EXIT at the end of your program
   the next lines in the giant hex file will run
3. The giant file.hex in /hex is a statically
   linked hex file containing the assembled
   hex from all assembly files in /asm in
   alphabetical order
'''
import io
import json
import os
import re
import string
import sys
import time
import util

from termcolor import colored


LABELS_TO_PC = {}
COMMENT_SYMBOL = '//'

valid_opcodes_keywords = [
    'LD', 'ADD', 'SUB', 'MUL', 'DIV', 'REM', 'CALL', 'CMP', 'LT', 'LTE', 'GT',
    'GTE', 'GOTO', 'RETURN', 'PUSH', 'POP', 'EXIT', 'WAIT', 'SHT', 'RAND',
    'INPUT', 'BLIT'
]

def error_msg(file_asm, line_idx, line, num_errors, msg):
    print(f'\n{file_asm}:{line_idx}', colored('error:', 'red'), msg)
    print(f'{line}')
    print(colored('^'+'~'*(len(line)-1), 'green'))
    num_errors += 1

    return num_errors


def write_two_lines_to_hexfile(word0_first_half,
                               word0_second_half,
                               word1, hex_file_str):
    # write to hex file
    hex_file_str += word0_first_half
    hex_file_str += word0_second_half
    hex_file_str += '\n'
    hex_file_str += word1
    hex_file_str += '\n'

    return hex_file_str


def compute_label_indices_from_file(file_asm, cumsum_hex_lines, num_errors):
    '''line = code // comment'''
    lines = util.return_lines_from_file(file_asm)
    lines_for_program = []  # all but commentsa and blank lines
    for line_idx, line in enumerate(lines):
        first_comment_idx = line.find(COMMENT_SYMBOL)

        comment = line[first_comment_idx+1:]
        code = line[:first_comment_idx]

        if first_comment_idx == -1:
            comment = ''
            code = line

        # match label regex
        if re.match(util.REGEX_LABEL_AND_COLON, code):
            label = re.findall(util.REGEX_LABEL_AND_COLON, code)[0]

            if label in LABELS_TO_PC.keys():
                msg='label defined more than once'
                num_errors = error_msg(
                    file_asm, line_idx, line, num_errors, msg
                )

            LABELS_TO_PC[label] = cumsum_hex_lines

        elif re.match(util.REGEX_HEX_WITH_SPACE_BEFORE, code):
            lines_for_program.append(code)
            cumsum_hex_lines += 1  # eg 0XFF0000FF

        elif not code.isspace() and code != '':
            lines_for_program.append(code)
            cumsum_hex_lines += 2

    return lines_for_program, cumsum_hex_lines, num_errors


def split_hexfile_into_byte_array(giant_hex_file_str):
    byte_arr = []
    for word in giant_hex_file_str.split('\n'):
        byte_arr += [
            util.hex_to_int(word[:2]),
            util.hex_to_int(word[2:4]),
            util.hex_to_int(word[4:6]),
            util.hex_to_int(word[6:])
        ]
    return bytearray(byte_arr)


def validate_and_make_hexfile(file_asm, lines, num_errors):
    hex_file_str = ''
    extra_line_for_raw_hex = 0

    # for line in lines:
    for line_idx, line in enumerate(lines):
        first_comment_idx = line.find(COMMENT_SYMBOL)

        if first_comment_idx == -1:
            comment = ''
            code = line
        else:
            comment = line[first_comment_idx+1:]
            code = line[:first_comment_idx]

        # args in code
        code_split = code.split(' ')

        # filter \t and ' '
        while '' in code_split:
            code_split.remove('')
        for idx in range(len(code_split)):
            code_split[idx] = code_split[idx].replace('\t', '')

        if len(code_split) > 0:
            opcode = code_split[0]
            args = code_split[1:]

            word0_first_half = '0000'
            word0_second_half = '0000'
            word1 = '00000000'

            valid_opcode = False

            # raw data
            if re.match(util.REGEX_HEX, opcode):
                valid_opcode = False
                if len(args) > 0:
                    msg='invalid hexcode'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                opcode_int = util.hex_to_int(opcode)
                opcode_hex = util.int_to_hex(opcode_int)

                hex_file_str += opcode_hex.zfill(8)
                hex_file_str += '\n'

            # valid opcode
            elif opcode not in valid_opcodes_keywords:
                msg=f'invalid opcode'
                num_errors = error_msg(
                    file_asm, line_idx, line, num_errors, msg
                )

            elif opcode == 'GOTO':
                valid_opcode = True
                if len(args) < 1:
                    msg='missing argument'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                # GOTO LABEL
                elif re.match(util.REGEX_LABEL, args[0]):
                    opcode_val = util.opcode_lookup_dict['GOTO']

                    if args[0] not in LABELS_TO_PC.keys():
                        msg='unknown label'
                        num_errors = error_msg(
                            file_asm, line_idx, line, num_errors, msg
                        )
                    else:
                        word1 = util.int_to_hex(LABELS_TO_PC[args[0]]).zfill(8)
                        word0_second_half = opcode_val.zfill(4)

                # GOTO i
                elif re.match(util.REGEX_INT, args[0]):
                    opcode_val = util.opcode_lookup_dict['GOTO']
                    word1 = util.int_to_hex(args[0]).zfill(8)
                    word0_second_half = opcode_val.zfill(4)

                # GOTO R[i]
                elif re.match(util.REGEX_LD_R_ONE, args[0]):
                    opcode_val = util.opcode_lookup_dict['GOTO R[i]']
                    word1 = util.int_to_hex(args[0][2:-1]).zfill(8)
                    word0_second_half = opcode_val.zfill(4)

            elif opcode == 'LD':
                # Validate
                if len(args) < 2:
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                # LD ARRAY R[X] R[Y] W H (X,Y must be <= 255)
                elif re.match(util.REGEX_ARRAY_LD, ' '.join(args)):
                    valid_opcode = True
                    opcode_val = util.opcode_lookup_dict['LD ARRAY TO VRAM']

                    all_args = re.findall(util.REGEX_ARRAY_LD, ' '.join(args))

                    label          = all_args[0][0]
                    x_sprite       = all_args[0][1]
                    y_sprite       = all_args[0][2]
                    width_sprite   = all_args[0][3]
                    height_sprite  = all_args[0][4]

                    if label not in LABELS_TO_PC.keys():
                        msg='unknown label'
                        num_errors = error_msg(
                            file_asm, line_idx, line, num_errors, msg
                        )

                    label_idx = util.int_to_hex(LABELS_TO_PC[label]).zfill(4)
                    x_sprite = util.int_to_hex(x_sprite).zfill(2)
                    y_sprite = util.int_to_hex(y_sprite).zfill(2)
                    width_sprite = util.int_to_hex(width_sprite).zfill(2)
                    height_sprite = util.int_to_hex(height_sprite).zfill(2)

                    word0_first_half = label_idx
                    word0_second_half = opcode_val.zfill(4)
                    word1 = x_sprite + y_sprite + width_sprite + height_sprite

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                # LD R[i] ARRAY  (load PC of ARRAY to R[i])
                elif re.match(util.REGEX_LD_LABEL_PC, ' '.join(args)):
                    valid_opcode = True
                    opcode_val = util.opcode_lookup_dict['LD ARRAY PC TO REGISTER']
                    word0_second_half = opcode_val.zfill(4)

                    # parse out args
                    all_args = re.findall(util.REGEX_LD_LABEL_PC, ' '.join(args))
                    ram_index = all_args[0][0]
                    label = all_args[0][1]

                    if label not in LABELS_TO_PC.keys():
                        msg='unknown label'
                        num_errors = error_msg(
                            file_asm, line_idx, line, num_errors, msg
                        )

                    label_idx = util.int_to_hex(LABELS_TO_PC[label]).zfill(4)

                    word0_first_half = label_idx
                    word1 = '0000' + util.int_to_hex(ram_index).zfill(4)

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                # LD R[U] R[i] R[j] R[k] R[k] (i,j,k,l must be <= 255)
                elif re.match(util.REGEX_REGISTER_ONLY_ARRAY_LD, ' '.join(args)):
                    valid_opcode = True
                    opcode_val = util.opcode_lookup_dict['LD REGISTERS TO VRAM']

                    all_args = re.findall(util.REGEX_REGISTER_ONLY_ARRAY_LD, ' '.join(args))

                    UVYZ           = all_args[0][0]
                    x_sprite       = all_args[0][1]
                    y_sprite       = all_args[0][2]
                    width_sprite   = all_args[0][3]
                    height_sprite  = all_args[0][4]

                    UVYZ_digit = util.UVYZ_to_hex_digit[str(UVYZ)]
                    x_sprite = util.int_to_hex(x_sprite).zfill(2)
                    y_sprite = util.int_to_hex(y_sprite).zfill(2)
                    width_sprite = util.int_to_hex(width_sprite).zfill(2)
                    height_sprite = util.int_to_hex(height_sprite).zfill(2)

                    word0_first_half = UVYZ_digit + '000'
                    word0_second_half = opcode_val.zfill(4)
                    word1 = x_sprite + y_sprite + width_sprite + height_sprite

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                # LD R[U] R[vram_idx] R[k] R[k] (k,l must be <= 255)
                elif re.match(util.REGEX_REGISTER_ONLY_VRAM_IDX_ARRAY_LD, ' '.join(args)):
                    valid_opcode = True
                    opcode_val = util.opcode_lookup_dict['LD REGISTERS TO VRAM W VRAM INDEX']

                    all_args = re.findall(
                        util.REGEX_REGISTER_ONLY_VRAM_IDX_ARRAY_LD,
                        ' '.join(args)
                    )

                    UVYZ           = all_args[0][0]
                    idx_to_vram_idx       = all_args[0][1]
                    width_sprite   = all_args[0][2]
                    height_sprite  = all_args[0][3]

                    UVYZ_digit = util.UVYZ_to_hex_digit[str(UVYZ)]
                    idx_to_vram_idx = util.int_to_hex(idx_to_vram_idx).zfill(4)
                    width_sprite = util.int_to_hex(width_sprite).zfill(2)
                    height_sprite = util.int_to_hex(height_sprite).zfill(2)

                    word0_first_half = UVYZ_digit + '000'
                    word0_second_half = opcode_val.zfill(4)
                    word1 = idx_to_vram_idx + width_sprite + height_sprite

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                elif re.match(util.REGEX_LD_R_ONE, args[0]):
                    valid_opcode = True

                    # LD R[i] R[j]
                    if re.match(util.REGEX_LD_R_ONE, args[1]):
                        opcode_val = util.opcode_lookup_dict['REGISTER TO REGISTER LOAD']
                        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                    # LD R[i] j
                    elif re.match(r'\d+', args[1]) or re.match(util.REGEX_HEX, args[1]):
                        opcode_val = util.opcode_lookup_dict['DIRECT LOAD']
                        word1 = util.int_to_hex(args[1]).zfill(8)

                    # LD R[i] R[U]
                    elif re.match(util.REGEX_UV_ONE, args[1]) and len(args) == 2:
                        opcode_val = util.opcode_lookup_dict['LD R[i] R[U]']

                        letters_arg0 = re.findall(util.REGEX_UV_ONE, args[1])
                        i = util.UVYZ_to_hex_digit[str(letters_arg0[0])]
                        word1 = i+'0000000'

                    word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                    word0_second_half = opcode_val.zfill(4)

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                elif re.match(util.REGEX_UV_ONE, args[0]) and len(args) == 2:
                    valid_opcode = True
                    letters_arg0 = re.findall(util.REGEX_UV_ONE, args[0])
                    i = util.UVYZ_to_hex_digit[str(letters_arg0[0])]
                    j = '0'

                    # LD R[U] R[V]
                    if re.match(util.REGEX_UV_ONE, args[1]):
                        opcode_val = util.opcode_lookup_dict['LD R[U] R[V]']
                        j = util.UVYZ_to_hex_digit[args[1][2:-1]]

                    # LD R[U] R[i]
                    elif re.match(r'R\[\d+]', args[1]):
                        opcode_val = util.opcode_lookup_dict['LD R[U] R[i]']
                        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                    # LD R[U] i
                    elif re.match(r'\d+', args[1]):
                        opcode_val = util.opcode_lookup_dict['LD R[U] i']
                        word1 = util.int_to_hex(args[1]).zfill(8)

                    word0_first_half = i+j+'00'
                    word0_second_half = opcode_val.zfill(4)

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                elif re.match(util.REGEX_UV_TWO, args[0]):
                    valid_opcode = True
                    letters_arg0 = re.findall(util.REGEX_UV_TWO, args[0])
                    i = util.UVYZ_to_hex_digit[str(letters_arg0[0][0])]
                    j = util.UVYZ_to_hex_digit[str(letters_arg0[0][1])]
                    k = '0'
                    l = '0'

                    # LD R[U:V] R[i]
                    if re.match(r'R\[\d+]', args[1]):
                        opcode_val = util.opcode_lookup_dict['LD R[U:V] R[i]']
                        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                    # LD R[U:V] i
                    if re.match(r'\d+', args[1]):
                        opcode_val = util.opcode_lookup_dict['LD R[U:V] i']
                        word1 = util.int_to_hex(args[1]).zfill(8)

                    # LD R[U:V] R[Y]
                    elif re.match(util.REGEX_UV_ONE, args[1]):
                        opcode_val = util.opcode_lookup_dict['LD R[U:V] R[Y]']
                        k = re.findall(util.REGEX_UV_ONE, args[1])[0]
                        k = util.UVYZ_to_hex_digit[k]
                        
                    # LD R[U:V] R[Y:Z]
                    elif re.match(util.REGEX_UV_TWO, args[1]):
                        opcode_val = util.opcode_lookup_dict['LD R[U:V] R[Y:Z]']

                        k_and_l = re.findall(util.REGEX_UV_TWO, args[1]) 
                        k = util.UVYZ_to_hex_digit[str(k_and_l[0][0])]
                        l = util.UVYZ_to_hex_digit[str(k_and_l[0][1])]

                    word0_first_half = i+j+k+l
                    word0_second_half = opcode_val.zfill(4)

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                if not valid_opcode:
                    msg='invalid syntax'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

            elif opcode == 'ADD':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                elif re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.opcode_lookup_dict['REGISTER TO REGISTER ADD']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.opcode_lookup_dict['DIRECT ADD']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'SUB':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                elif re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.opcode_lookup_dict['REGISTER TO REGISTER SUBTRACT']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.opcode_lookup_dict['DIRECT SUBTRACT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'MUL':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )
                elif re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.opcode_lookup_dict['REGISTER TO REGISTER MULTIPLY']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.opcode_lookup_dict['DIRECT MULTIPLY']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'DIV':
                valid_opcode = True

                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                elif re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.opcode_lookup_dict['REGISTER TO REGISTER DIVIDE']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.opcode_lookup_dict['DIRECT DIVIDE']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                # check if dividing by 0
                if word1 == '00000000':
                    msg=f'attempting to divide by zero'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'REM':
                valid_opcode = True

                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                elif re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.opcode_lookup_dict['REGISTER TO REGISTER REMAINDER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.opcode_lookup_dict['DIRECT REMAINDER']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                # check if remainder by 0
                if word1 == '00000000':
                    msg=f'attempting to divide by zero'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # ==
            elif opcode == 'CMP':
                valid_opcode = True
                if len(args) < 2:
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                elif re.match(util.REGEX_LD_R_ONE, args[0]):
                    if re.match(util.REGEX_LD_R_ONE, args[1]):
                        opcode_val = util.opcode_lookup_dict['COMPARE REGISTER TO REGISTER']
                        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                        word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                        word0_second_half = opcode_val.zfill(4)

                    else:
                        opcode_val = util.opcode_lookup_dict['COMPARE REGISTER TO DIRECT']
                        word1 = util.int_to_hex(args[1]).zfill(8)

                        word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                        word0_second_half = opcode_val.zfill(4)

                elif re.match(util.REGEX_UV_ONE, args[0]):
                    letters_arg0 = re.findall(util.REGEX_UV_ONE, args[0])
                    i = util.UVYZ_to_hex_digit[str(letters_arg0[0])]

                    if re.match(r'\d+', args[1]):
                        opcode_val = util.opcode_lookup_dict['COMPARE UV TO DIRECT']
                        word1 = util.int_to_hex(args[1]).zfill(8)

                        word0_first_half = i + '000'
                        word0_second_half = opcode_val.zfill(4)


                hex_file_str = write_two_lines_to_hexfile(
                    word0_first_half, word0_second_half,
                    word1, hex_file_str
                )

            # <
            elif opcode == 'LT':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )
                elif re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.opcode_lookup_dict['LESS THAN REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.opcode_lookup_dict['LESS THAN REGISTER TO DIRECT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # <=
            elif opcode == 'LTE':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )
                elif re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.opcode_lookup_dict['LESS THAN OR EQUAL REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.opcode_lookup_dict['LESS THAN OR EQUAL REGISTER TO DIRECT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # >
            elif opcode == 'GT':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )
                elif re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.opcode_lookup_dict['STRICT GREATER THAN REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.opcode_lookup_dict['STRICT GREATER THAN REGISTER TO DIRECT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # >=
            elif opcode == 'GTE':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    msg=f'requires 2 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )
                elif re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.opcode_lookup_dict['GREATER THAN OR EQUAL REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.opcode_lookup_dict['GREATER THAN OR EQUAL REGISTER TO DIRECT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'CALL':
                valid_opcode = True
                if len(args) < 1:
                    msg=f'requires 1 or more arguments after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                # CALL LABEL
                elif re.match(util.REGEX_LABEL, args[0]):
                    opcode_val = util.opcode_lookup_dict['CALL']

                    if args[0] not in LABELS_TO_PC.keys():
                        raise Exception('\nUnknown Label %s' %args[0])
                    word1 = util.int_to_hex(LABELS_TO_PC[args[0]]).zfill(8)

                # CALL i
                elif re.match(util.REGEX_INT, args[0]):
                    opcode_val = util.opcode_lookup_dict['CALL']
                    word1 = util.int_to_hex(args[0]).zfill(8)

                # CALL R[i]
                elif re.match(util.REGEX_LD_R_ONE, args[0]):
                    opcode_val = util.opcode_lookup_dict['CALL R[i]']
                    word1 = util.int_to_hex(args[0][2:-1]).zfill(8)

                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'RETURN':
                valid_opcode = True
                
                if len(args) > 0:
                    msg=f'no args after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                opcode_val = util.opcode_lookup_dict['RETURN']
                word0_second_half = opcode_val.zfill(4)

            elif opcode in ('POP', 'PUSH'):
                valid_opcode = True
                if len(args) > 0:
                    msg=f'no args after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                opcode_val = util.opcode_lookup_dict[opcode]
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'BLIT':
                valid_opcode = True

                if len(args) > 0:
                    msg=f'no args after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                opcode_val = util.opcode_lookup_dict['BLIT']
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'RAND':
                valid_opcode = True
                opcode_val = util.opcode_lookup_dict[opcode]
                word0_second_half = opcode_val.zfill(4)

                if len(args) != 1:
                    msg=f'1 arg after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

                elif re.match(r'R\[\d+]', args[0]):
                    word1 = util.int_to_hex(args[0][2:-1]).zfill(8)

                else:
                    msg='invalid syntax'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

            elif opcode == 'INPUT':
                valid_opcode = True
                opcode_val = util.opcode_lookup_dict[opcode]
                word0_second_half = opcode_val.zfill(4)

                if len(args) == 1 and re.match(util.REGEX_LD_R_ONE, args[0]):
                    ram_slot_idx = re.findall(r'R\[(\d+)]', args[0])[0]
                    word0_first_half = util.int_to_hex(ram_slot_idx).zfill(4)

                else:
                    msg='invalid syntax'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

            elif opcode == 'SHT':  # shift right plus AND
                valid_opcode = True
                opcode_val = util.opcode_lookup_dict[opcode]
                word0_second_half = opcode_val.zfill(4)

                if len(args) == 3 and (re.match(util.REGEX_LD_R_ONE, args[0]) and
                                       re.match(util.REGEX_LD_R_ONE, args[1]) and
                                       re.match(r'\d+', args[2])):

                    ram_idx_from = re.findall(r'R\[(\d+)]', args[0])[0]
                    ram_idx_to = re.findall(r'R\[(\d+)]', args[1])[0]
                    bitshift = args[2]

                    word0_first_half = util.int_to_hex(ram_idx_to).zfill(4)
                    word1_first_half = util.int_to_hex(ram_idx_from).zfill(4)
                    word1_second_half = util.int_to_hex(bitshift).zfill(4)
                    word1 = word1_first_half + word1_second_half

                else:
                    msg='invalid syntax'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

            elif opcode == 'WAIT':  # wait 17 ms
                valid_opcode = True
                opcode_val = util.opcode_lookup_dict[opcode]
                word0_second_half = opcode_val.zfill(4)

                if len(args) > 0:
                    msg=f'no args after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

            elif opcode == 'EXIT':
                valid_opcode = True
                opcode_val = util.opcode_lookup_dict['EXIT']
                word0_second_half = opcode_val.zfill(4)

                if len(args) > 0:
                    msg=f'no args after {opcode}'
                    num_errors = error_msg(
                        file_asm, line_idx, line, num_errors, msg
                    )

            # write lines for LD and CMP
            if valid_opcode and opcode not in ['LD', 'CMP']:
                hex_file_str = write_two_lines_to_hexfile(
                    word0_first_half, word0_second_half,
                    word1, hex_file_str
                )

    return hex_file_str, num_errors


if __name__ == '__main__':
    staticallyLinked = (True if '-s' in sys.argv else False)
    asm_filenames_in_argv = [f for f in sys.argv if f.endswith('.vasm')]
    all_files_in_asm_folder = sorted([f for f in os.listdir('./asm') if f.endswith('.vasm')])

    filename_where_pc_starts = asm_filenames_in_argv[0]

    if staticallyLinked:
        # gather all files in /asm folder
        asm_files_for_compile = all_files_in_asm_folder
    else:
        asm_files_for_compile = sorted(asm_filenames_in_argv)

        # check if asm filenames are valid
        for filename in asm_files_for_compile:
            if filename not in all_files_in_asm_folder:
                print(f'"{filename}" is not a file in /asm folder.')

    # gather all labels across hex files
    num_errors = 0
    cumsum_hex_lines = 0
    giant_hex_file_str = ''
    all_lines_for_programs = []
    filename_and_lines_pairs = []
    for asm_file in  asm_files_for_compile:
        # set where PC starts
        if asm_file == filename_where_pc_starts:
            where_PC_starts = cumsum_hex_lines

        lines_for_program, cumsum_hex_lines, num_errors = compute_label_indices_from_file(
            'asm/'+asm_file, cumsum_hex_lines, num_errors
        )
        filename_and_lines_pairs.append((asm_file, lines_for_program))

    for item in filename_and_lines_pairs:
        asm_file = item[0]
        lines_for_program = item[1]

        hex_file_str, num_errors = validate_and_make_hexfile(
            asm_file, lines_for_program, num_errors
        )
        giant_hex_file_str += hex_file_str

    # compiler messages
    print('\n%s error%s generated' %(num_errors, ('s' if num_errors!=1 else '')))
    if num_errors == 0:
        print(colored('pass', 'green'))
    else:
        print(colored('fail', 'red'))

    # convert hexfile to byte array
    binary_format = split_hexfile_into_byte_array(giant_hex_file_str[:-1])

    # write bytearray to disk
    f = open('bin/file.bin', 'w+b')
    f.write(binary_format)
    f.close()

    # write starting Program Counter (PC)
    f = open('start_pc.txt', 'w')
    f.write(str(where_PC_starts))
    f.close()
