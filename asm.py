'''
Assembler: asm -> hex
'''
import os
import re
import string
import sys
import time
import util


LABELS_TO_PC = {}

def compute_label_indices(file_asm, global_hex_line):
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
            LABELS_TO_PC[label] = global_hex_line

        elif not code.isspace() and code != '':
            lines_sans_labels.append(code)
            global_hex_line += 2

    return lines_sans_labels, global_hex_line


def validate_and_generate_hexfile(lines, file_hex):
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

    # write file
    f = open(file_hex, 'w')
    f.write(hex_file_str)
    f.close()


if __name__ == "__main__":
    filename = sys.argv[1]

    # collect, sort all .asm files
    all_asm_files = []
    all_files_in_asm_folder = os.listdir('./asm')
    for filename in all_files_in_asm_folder:
        if filename.endswith('.asm'):
            all_asm_files.append(filename)
    all_asm_files = sorted(all_asm_files)

    # generate all asm->hex files
    global_hex_line = 0
    for asm_f in  all_asm_files:
        file_asm = 'asm/%s' %asm_f
        file_hex = 'hex/%s' %asm_f
        file_hex = file_hex.replace('.asm', '.hex')

        print('%s, %s' %(file_asm, file_hex))

        lines_sans_labels, global_hex_line = compute_label_indices(
            file_asm, global_hex_line
        )
        validate_and_generate_hexfile(
            lines_sans_labels, file_hex
        )
        print(LABELS_TO_PC)
        print(global_hex_line)
        print('\n')
