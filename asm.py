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
import json
import os
import pprint
import re
import string
import sys
import time
import util


LABELS_TO_PC = {}


# WIP for DRY
def return_hex_instruction_lines(opcode, args, word0_first_half,
                                 word0_second_half, word1,
                                 to_register_key, to_direct_key):
    valid_opcode = True
    if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
        raise Exception(
            util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
        )
    if re.search(r'R\[\d+]', args[1]):
        opcode_val = util.op_codes_dict[to_register_key]
        word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

    else:
        opcode_val = util.op_codes_dict[to_direct_key]
        word1 = util.int_to_hex(args[1]).zfill(8)

    word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
    word0_second_half = opcode_val.zfill(4)

    return word0_first_half, word0_second_half, word1


def compute_label_indices(file_asm, cumsum_hex_lines):
    '''line = code // comment'''
    lines = util.return_lines_from_file(file_asm)
    lines_for_program = []  # all but comments, blank and comments
    for line in lines:
        first_semicolon_idx = line.find('//')

        if first_semicolon_idx == -1:
            comment = ''
            code = line
        else:
            comment = line[first_semicolon_idx+1:]
            code = line[:first_semicolon_idx]

        # match label regex
        if re.match(util.REGEX_LABEL_PATTERN, code):
            label = re.findall(util.REGEX_LABEL_PATTERN[2:], code)[0][:-1]

            if label in LABELS_TO_PC.keys():
                raise Exception(
                    util.LABEL_DEFINED_MORE_THAN_ONCE_EXCEPTION_MSG.format(label=label)
                )
            LABELS_TO_PC[label] = cumsum_hex_lines

        elif not code.isspace() and code != '':
            lines_for_program.append(code)
            cumsum_hex_lines += 2

    return lines_for_program, cumsum_hex_lines


def validate_and_make_hexfile(lines):
    hex_file_str = ''

    for line in lines:
        first_semicolon_idx = line.find('//')

        if first_semicolon_idx == -1:
            comment = ''
            code = line
        else:
            comment = line[first_semicolon_idx+1:]
            code = line[:first_semicolon_idx]

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
            if opcode == 'GOTO':
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

            elif opcode == 'LD':  # RAM and VRAM
                valid_opcode = True

                # invalid_LD_R_condition = len(args) < 2 or re.search(r'R\[\d+]', args[0])
                # invalid_LD_V_condition = len(args) < 1 or re.search(r'V\[\d+]', args[0])

                # if invalid_LD_R_condition or invalid_LD_V_condition:
                #     raise Exception(util.LD_EXCEPTION_MSG)

                #######
                # RAM #
                #######

                # 1. LD R[i] R[j]
                if re.search(r'R\[\d+]', args[0]) and re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER LOAD']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                # 2. LD R[i] j
                elif re.search(r'R\[\d+]', args[0]) and re.search(r'\d+', args[1]):
                    opcode_val = util.op_codes_dict['DIRECT LOAD']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                ########
                # VRAM #
                ########

                # 1. LD V[i]  <- load from slots R[4096-4099]
                elif re.search(r'V\[\d+]', args[0]) and len(args) == 1:
                    opcode_val = util.op_codes_dict['VRAM DIRECT LOAD']

                # 2. V[i] V[j]
                elif re.search(r'V\[\d+]', args[0]) and re.search(r'V\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['VRAM TO VRAM REGISTER LOAD']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                # 3. LD V[i] R[j]
                elif re.search(r'V\[\d+]', args[0]) and re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['RAM TO VRAM REGISTER LOAD']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)                   

                else:
                    raise Exception(util.LD_EXCEPTION_MSG)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)


            elif opcode == 'ADD':
                valid_opcode = True
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER ADD']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT ADD']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'SUB':
                valid_opcode = True
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER SUBTRACT']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT SUBTRACT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'MUL':
                valid_opcode = True
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER MULTIPLY']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT MULTIPLY']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'DIV':
                valid_opcode = True
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER DIVIDE']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT DIVIDE']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # compare
            elif opcode == 'CMP':
                valid_opcode = True
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['COMPARE REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['COMPARE REGISTER TO DIRECT']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            # <
            elif opcode == 'LT':
                valid_opcode = True
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
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
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
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
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
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
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.TWO_ARGS_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
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

            elif opcode == 'EXIT':
                valid_opcode = True
                opcode_val = util.op_codes_dict['EXIT']
                word0_second_half = opcode_val.zfill(4)

            if valid_opcode:
                hex_file_str += word0_first_half
                hex_file_str += word0_second_half
                hex_file_str += '\n'
                hex_file_str += word1
                hex_file_str += '\n\n'

    return hex_file_str


if __name__ == "__main__":
    filename = sys.argv[1]

    # collect, sort all .asm files
    all_asm_files = []
    all_files_in_asm_folder = os.listdir('./asm')

    # check if picked valid filename
    if filename not in all_files_in_asm_folder:
        raise Exception(util.NO_FILE_FOUND_EXCEPTION_MSG.format(
            filename, all_files_in_asm_folder
        ))

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

        lines_for_program, cumsum_hex_lines = compute_label_indices(
            file_asm, cumsum_hex_lines
        )
        all_lines_for_programs.append(lines_for_program) 

    # generate all asm -> hex files
    for lines_for_program in all_lines_for_programs:
        hex_file_str = validate_and_make_hexfile(lines_for_program)
        giant_hex_file_str += hex_file_str

    # write statically linked hex file
    f = open('hex/file.hex', 'w')
    f.write(giant_hex_file_str)
    f.close()

    # write PC for program
    f = open('start_pc.txt', 'w')
    f.write(str(where_PC_starts))
    f.close()
