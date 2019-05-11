'''
Assembler: asm -> hex
'''
import json
import os
import re
import string
import sys
import time
import util


LABELS_TO_PC = {}

def compute_label_indices(file_asm, cumsum_hex_lines):
    '''line = code ; comment'''
    lines = util.return_lines_from_file(file_asm)
    lines_sans_labels = []
    for line in lines:
        first_semicolon_idx = line.find(';')

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
            lines_sans_labels.append(code)
            cumsum_hex_lines += 2

    return lines_sans_labels, cumsum_hex_lines


def validate_and_make_hexfile(lines):
    hex_file_str = ''

    for line in lines:
        first_semicolon_idx = line.find(';')

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

            elif opcode == 'LD':
                valid_opcode = True
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.GENERAL_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER LOAD']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT LOAD']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'ADD':
                valid_opcode = True
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.GENERAL_EXCEPTION_MSG.format(opcode=opcode)
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
                        util.GENERAL_EXCEPTION_MSG.format(opcode=opcode)
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
                        util.GENERAL_EXCEPTION_MSG.format(opcode=opcode)
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
                        util.GENERAL_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['REGISTER TO REGISTER DIVIDE']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['DIRECT DIVIDE']
                    word1 = util.int_to_hex(args[1]).zfill(8)

                word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
                word0_second_half = opcode_val.zfill(4)

            elif opcode == 'CMP':
                valid_opcode = True
                if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
                    raise Exception(
                        util.GENERAL_EXCEPTION_MSG.format(opcode=opcode)
                    )
                if re.search(r'R\[\d+]', args[1]):
                    opcode_val = util.op_codes_dict['COMPARE REGISTER TO REGISTER']
                    word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

                else:
                    opcode_val = util.op_codes_dict['COMPARE REGISTER TO VALUE']
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
    for f_name in all_files_in_asm_folder:
        if f_name.endswith('.asm'):
            all_asm_files.append(f_name)
    all_asm_files = sorted(all_asm_files)

    # generate all asm->hex files
    cumsum_hex_lines = 0
    where_PC_starts = None
    giant_hex_file_str = ''
    for asm_f in  all_asm_files:
        file_asm = 'asm/%s' %asm_f

        if filename + '.asm' == asm_f:
            print(filename)
            where_PC_starts = cumsum_hex_lines

        lines_sans_labels, cumsum_hex_lines = compute_label_indices(
            file_asm, cumsum_hex_lines
        )

        hex_file_str = validate_and_make_hexfile(lines_sans_labels)
        giant_hex_file_str += hex_file_str

    # write giant hex file
    # statically linked files FTW!
    f = open('hex/file.hex', 'w')
    f.write(giant_hex_file_str)
    f.close()

    # record starting PC
    f = open('start_pc.txt', 'w')
    f.write(str(where_PC_starts))
    f.close()
