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


LABELS_TO_PC = {}
COMMENT_SYMBOL = '//'


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



# WIP for DRY
def return_hex_instruction_lines(opcode, args, word0_first_half,
                                 word0_second_half, word1,
                                 to_register_key, to_direct_key):
    if len(args) < 2 or not re.search(util.REGEX_LD_R_ONE, args[0]):
        raise Exception(
            util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
        )
    if re.search(util.REGEX_LD_R_ONE, args[1]):
        opcode_val = util.op_codes_dict[to_register_key]
        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

    else:
        opcode_val = util.op_codes_dict[to_direct_key]
        word1 = util.int_to_hex(args[1]).zfill(8)

    word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
    word0_second_half = opcode_val.zfill(4)

    return word0_first_half, word0_second_half, word1


def compute_label_indices_from_file(file_asm, cumsum_hex_lines):
    '''line = code // comment'''
    lines = util.return_lines_from_file(file_asm)
    lines_for_program = []  # all but commentsa and blank lines
    for line in lines:
        first_comment_idx = line.find(COMMENT_SYMBOL)

        comment = line[first_comment_idx+1:]
        code = line[:first_comment_idx]

        if first_comment_idx == -1:
            comment = ''
            code = line

        # match label regex
        if re.match(util.REGEX_LABEL_AND_COLON, code):
            label = re.findall(r'[\t ]*([A-z|\d|_]+):', code)[0]

            if label in LABELS_TO_PC.keys():
                raise Exception(
                    util.LABEL_DEFINED_MORE_THAN_ONCE_EXCEPTION_MSG.format(
                        label=label
                    )
                )
            LABELS_TO_PC[label] = cumsum_hex_lines

        elif re.match(util.REGEX_HEX_WITH_SPACE_BEFORE, code):
            lines_for_program.append(code)
            cumsum_hex_lines += 1  # eg 0XFF0000FF

        elif not code.isspace() and code != '':
            lines_for_program.append(code)
            cumsum_hex_lines += 2

    return lines_for_program, cumsum_hex_lines


def validate_and_make_hexfile(lines):
    hex_file_str = ''
    extra_line_for_raw_hex = 0

    for line in lines:
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
                    raise Exception(util.RAW_HEX_EXCEPTION_MSG)

                opcode_int = util.hex_to_int(opcode)
                opcode_hex = util.int_to_hex(opcode_int)

                hex_file_str += opcode_hex.zfill(8)
                hex_file_str += '\n'


            elif opcode == 'GOTO':
                valid_opcode = True
                if len(args) < 1:
                    raise Exception(util.GOTO_EXCEPTION_MSG)

                opcode_val = util.op_codes_dict['GOTO']
                word0_second_half = opcode_val.zfill(4)

                try:
                    word1 = util.int_to_hex(args[0]).zfill(8)
                except ValueError:
                    if args[0] not in LABELS_TO_PC.keys():
                        raise Exception('\nUnknown Label %s' %args[0])
                    word1 = util.int_to_hex(LABELS_TO_PC[args[0]]).zfill(8)

            elif opcode == 'LD':
                valid_opcode = True

                # Validate
                if len(args) < 2:
                    raise Exception(util.LD_EXCEPTION_MSG)

                # LD MARIO R[X] R[Y] W H (X,Y must be <= 255)
                if re.match(util.REGEX_ARRAY_LD, ' '.join(args)):
                    opcode_val = util.op_codes_dict['ARRAY']

                    all_args = re.findall(util.REGEX_ARRAY_LD, ' '.join(args))

                    label          = all_args[0][0]
                    x_sprite       = all_args[0][1]
                    y_sprite       = all_args[0][2]
                    width_sprite   = all_args[0][3]
                    height_sprite  = all_args[0][4]

                    if label not in LABELS_TO_PC.keys():
                        raise Exception('\nUnknown Label %s' %label)

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

                # LD R[i] MARIO  (load PC of MARIO array to R[i])
                elif re.match(util.REGEX_LD_LABEL_PC, ' '.join(args)):
                    opcode_val = util.op_codes_dict['LABEL_PC']
                    word0_second_half = opcode_val.zfill(4)

                    # parse out args
                    all_args = re.findall(util.REGEX_LD_LABEL_PC, ' '.join(args))
                    ram_index = all_args[0][0]
                    label = all_args[0][1]

                    if label not in LABELS_TO_PC.keys():
                        raise Exception('\nUnknown Label %s' %label)

                    label_idx = util.int_to_hex(LABELS_TO_PC[label]).zfill(4)

                    word0_first_half = label_idx
                    word1 = '0000' + util.int_to_hex(ram_index).zfill(4)

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                # LD R[U] R[i] R[j] R[k] R[k] (i,j,k,l must be <= 255)
                elif re.match(util.REGEX_REGISTER_ONLY_ARRAY_LD, ' '.join(args)):
                    opcode_val = util.op_codes_dict['ARRAY_REGISTER_ONLY']

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

                elif re.match(util.REGEX_LD_R_ONE, args[0]):
                    if re.match(util.REGEX_LD_R_ONE, args[1]):
                        # LD R[i] R[j]
                        opcode_val = util.op_codes_dict['REGISTER TO REGISTER LOAD']
                        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                    elif re.match(r'\d+', args[1]) or re.match(util.REGEX_HEX, args[1]):
                        # LD R[i] j
                        opcode_val = util.op_codes_dict['DIRECT LOAD']
                        word1 = util.int_to_hex(args[1]).zfill(8)

                    else:
                        raise Exception('LD R[i] XXX')

                    word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                    word0_second_half = opcode_val.zfill(4)

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                elif re.match(util.REGEX_UV_ONE, args[0]) and len(args) == 2:
                    letters_arg0 = re.findall(util.REGEX_UV_ONE, args[0])
                    i = util.UVYZ_to_hex_digit[str(letters_arg0[0])]
                    j = '0'

                    if re.match(util.REGEX_UV_ONE, args[1]):
                        # LD R[U] R[V]
                        j = util.UVYZ_to_hex_digit[args[1][2:-1]]
                        opcode_val = '100'

                    elif re.match(r'R\[\d+]', args[1]):
                        # LD R[U] R[i]
                        opcode_val = '104'
                        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                    elif re.match(r'\d+', args[1]):
                        # LD R[U] i
                        opcode_val = '105'
                        word1 = util.int_to_hex(args[1]).zfill(8)

                    word0_first_half = i+j+'00'
                    word0_second_half = opcode_val.zfill(4)

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                elif re.match(util.REGEX_UV_TWO, args[0]):
                    letters_arg0 = re.findall(util.REGEX_UV_TWO, args[0])
                    i = util.UVYZ_to_hex_digit[str(letters_arg0[0][0])]
                    j = util.UVYZ_to_hex_digit[str(letters_arg0[0][1])]
                    k = '0'
                    l = '0'

                    # LD R[U:V] R[i]
                    if re.match(r'R\[\d+]', args[1]):
                        opcode_val = '103'

                        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                    # LD R[U:V] i
                    if re.match(r'\d+', args[1]):
                        opcode_val = '106'

                        word1 = util.int_to_hex(args[1]).zfill(8)

                    # LD R[U:V] R[Y]
                    elif re.match(util.REGEX_UV_ONE, args[1]):
                        opcode_val = '101'
                        k = re.findall(util.REGEX_UV_ONE, args[1])[0]
                        k = util.UVYZ_to_hex_digit[k]
                        
                    # LD R[U:V] R[Y:Z]
                    elif re.match(util.REGEX_UV_TWO, args[1]):
                        opcode_val = '102'

                        k_and_l = re.findall(util.REGEX_UV_TWO, args[1]) 
                        k = util.UVYZ_to_hex_digit[str(k_and_l[0][0])]
                        l = util.UVYZ_to_hex_digit[str(k_and_l[0][1])]

                    word0_first_half = i+j+k+l
                    word0_second_half = opcode_val.zfill(4)

                    hex_file_str = write_two_lines_to_hexfile(
                        word0_first_half, word0_second_half,
                        word1, hex_file_str
                    )

                else:
                    raise Exception(util.LD_EXCEPTION_MSG)

            elif opcode == 'ADD':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER ADD']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT ADD']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'SUB':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER SUBTRACT']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT SUBTRACT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'MUL':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER MULTIPLY']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT MULTIPLY']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'DIV':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER DIVIDE']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT DIVIDE']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # ==
            elif opcode == 'CMP':
                valid_opcode = True
                if len(args) < 2:
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )

                if re.match(util.REGEX_LD_R_ONE, args[0]):
                    if re.match(util.REGEX_LD_R_ONE, args[1]):
                        opcode_val = util.op_codes_dict['COMPARE REGISTER TO REGISTER']
                        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                        word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                        word0_second_half = opcode_val.zfill(4)

                    else:
                        opcode_val = util.op_codes_dict['COMPARE REGISTER TO DIRECT']
                        word1 = util.int_to_hex(args[1]).zfill(8)

                        word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                        word0_second_half = opcode_val.zfill(4)

                elif re.match(util.REGEX_UV_ONE, args[0]):
                    letters_arg0 = re.findall(util.REGEX_UV_ONE, args[0])
                    i = util.UVYZ_to_hex_digit[str(letters_arg0[0])]

                    if re.match(r'\d+', args[1]):
                        opcode_val = util.op_codes_dict['COMPARE UV TO DIRECT']
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
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.op_codes_dict['LESS THAN REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['LESS THAN REGISTER TO DIRECT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # <=
            elif opcode == 'LTE':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.op_codes_dict['LESS THAN OR EQUAL REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['LESS THAN OR EQUAL REGISTER TO DIRECT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # >
            elif opcode == 'GT':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.op_codes_dict['STRICT GREATER THAN REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['STRICT GREATER THAN REGISTER TO DIRECT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # >=
            elif opcode == 'GTE':
                valid_opcode = True
                if len(args) < 2 or not re.match(util.REGEX_LD_R_ONE, args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.match(util.REGEX_LD_R_ONE, args[1]):
                    opcode_val = util.op_codes_dict['GREATER THAN OR EQUAL REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['GREATER THAN OR EQUAL REGISTER TO DIRECT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'CALL':
                valid_opcode = True
                if len(args) != 1:
                    raise Exception(util.CALL_EXCEPTION_MSG)

                opcode_val = util.op_codes_dict['CALL']
                word0_second_half = opcode_val.zfill(4)

                if args[0] not in LABELS_TO_PC.keys():
                    raise Exception('\nUnknown Label %s' %args[0])
                word1 = util.int_to_hex(LABELS_TO_PC[args[0]]).zfill(8)

            elif opcode == 'RETURN':
                valid_opcode = True
                if len(args) > 0:
                    raise Exception(util.RETURN_EXCEPTION_MSG)

                opcode_val = util.op_codes_dict['RETURN']
                word0_second_half = opcode_val.zfill(4)

            elif opcode in ('POP', 'PUSH'):
                valid_opcode = True
                if len(args) > 0:
                    raise Exception(util.POP_PUSH_EXCEPTION_MSG.format(opcode))

                opcode_val = util.op_codes_dict[opcode]
                word0_second_half = opcode_val.zfill(4)

            # transfer RAM portion to display and update
            elif opcode == 'BLIT':
                valid_opcode = True
                opcode_val = util.op_codes_dict['BLIT']
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'RAND':
                valid_opcode = True
                opcode_val = util.op_codes_dict[opcode]
                word0_second_half = opcode_val.zfill(4)

                if len(args) < 1:
                    raise Exception(
                        util.ONE_ARG_EXCEPTION_MSG.format(opcode=opcode)
                    )

                if re.match(r'R\[\d+]', args[0]):
                    word1 = util.int_to_hex(args[0][2:-1]).zfill(8)

            elif opcode == 'INPUT':
                valid_opcode = True
                opcode_val = util.op_codes_dict[opcode]
                word0_second_half = opcode_val.zfill(4)

                if len(args) == 1 and re.match(util.REGEX_LD_R_ONE, args[0]):
                    ram_slot_idx = re.findall(r'R\[(\d+)]', args[0])[0]
                    word0_first_half = util.int_to_hex(ram_slot_idx).zfill(4)

            elif opcode == 'SHT':  # shift right plus AND
                valid_opcode = True
                opcode_val = util.op_codes_dict[opcode]
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

            elif opcode == 'WAIT':  # wait 1/60 sec
                valid_opcode = True
                opcode_val = util.op_codes_dict[opcode]
                word0_second_half = opcode_val.zfill(4)    

            elif opcode == 'EXIT':
                valid_opcode = True
                opcode_val = util.op_codes_dict['EXIT']
                word0_second_half = opcode_val.zfill(4)

            # TODO: ignore line if invalid line of code

            if valid_opcode and opcode not in ['LD', 'CMP']:
                hex_file_str = write_two_lines_to_hexfile(
                    word0_first_half, word0_second_half,
                    word1, hex_file_str
                )

    return hex_file_str


if __name__ == "__main__":
    filename = sys.argv[1]

    # gather all files in /asm folder
    all_asm_files = []
    all_files_in_asm_folder = os.listdir('./asm')

    # check if picked valid filename
    if filename not in all_files_in_asm_folder:
        raise Exception(util.NO_FILE_FOUND_EXCEPTION_MSG.format(
            filename, all_files_in_asm_folder
        ))

    # gather and sort all .asm files
    for f_name in all_files_in_asm_folder:
        if f_name.endswith('.asm'):
            all_asm_files.append(f_name)
    all_asm_files = sorted(all_asm_files)

    # gather all labels across hex files
    cumsum_hex_lines = 0
    giant_hex_file_str = ''
    all_lines_for_programs = []
    for asm_f in  all_asm_files:
        file_asm = 'asm/%s' %asm_f

        if filename == asm_f:
            where_PC_starts = cumsum_hex_lines

        # one file at a time
        lines_for_program, cumsum_hex_lines = compute_label_indices_from_file(
            file_asm, cumsum_hex_lines
        )
        all_lines_for_programs.append(lines_for_program)

    # combine all asm files into one BIG hexfile
    for lines_for_program in all_lines_for_programs:
        hex_file_str = validate_and_make_hexfile(lines_for_program)
        giant_hex_file_str += hex_file_str

    # write statically linked hexfile to disk
    f = open('hex/file.hex', 'w')
    f.write(giant_hex_file_str)
    f.close()

    # set PC for program start
    f = open('start_pc.txt', 'w')
    f.write(str(where_PC_starts))
    f.close()
