'''
Assembler: asm -> hex
'''
import os
import re
import string
import sys
import time
import util


labels_to_pc = {}

# TODO: make PC a global variable
def compute_label_indices(file_asm):
    lines = util.return_lines_from_file(file_asm)
    lines_sans_labels = []
    PC = 0
    for line in lines:
        first_semicolon_idx = line.find(';')

        if first_semicolon_idx == -1:
            comment = ''
            code = line
        else:
            comment = line[first_semicolon_idx+1:]
            code = line[:first_semicolon_idx]

        # match label regex
        if re.match(r' *[A-Z|\d|_]+:', code):
            label = re.findall(r'[A-Z|\d|_]+:', code)[0][:-1]
            labels_to_pc[label] = PC

        elif not code.isspace() and code != '':
            lines_sans_labels.append(code)
            PC += 2

    # print code
    print('-> labels: %r' %labels_to_pc)
    return lines_sans_labels


def validate_and_run(lines, file_hex):
    hex_file_str = ''
    PC = 0

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
                    if args[0] not in labels_to_pc.keys():
                        raise Exception('\nUnknown Label %s' %args[0])
                    word1 = util.int_to_hex(labels_to_pc[args[0]]).zfill(8)

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

                if args[0] not in labels_to_pc.keys():
                    raise Exception('\nUnknown Label %s' %args[0])
                word1 = util.int_to_hex(labels_to_pc[args[0]]).zfill(8)

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
    file_asm = sys.argv[1]
    file_hex = sys.argv[2]
    lines_sans_labels = compute_label_indices(file_asm)
    validate_and_run(lines_sans_labels, file_hex)
