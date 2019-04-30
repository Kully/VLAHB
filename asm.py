'''
Assembler: asm -> hex
'''
import os
import re
import string
import sys
import time
import util

file_asm = 'file.asm'
file_hex = 'myfile.hex'
lines = util.return_lines_from_file(file_asm)

goto_exception_msg = (
	'\nThe Opcode GOTO must be followed by 1 argument in '
	'the form:\n    GOTO X\n where X is the new PC that you '
	'want to go to'
)

exception_msg = (
	'\nThe Opcode {opcode} must be followed by 2 arguments '
	'either in the form:\n    {opcode} R[X] R[Y]\nor\n'
	'    {opcode} R[X] Y'
)

op_codes_dict = {
	'GOTO': '1', #
	'DIRECT LOAD': '2', #
	'DIRECT ADD': '3', #
	'DIRECT SUBTRACT': '4', #
	'DIRECT MULTIPLY': '5', #
	'DIRECT DIVIDE': '6', #
	'REGISTER TO REGISTER LOAD': '7', #
	'REGISTER TO REGISTER ADD': '8', #
	'REGISTER TO REGISTER SUBTRACT': '9', #
	'REGISTER TO REGISTER MULTIPLY': 'a', #
	'REGISTER TO REGISTER DIVIDE': 'b', #
	'COMPARE REGISTER TO VALUE': 'c',
	'COMPARE REGISTER TO REGISTER': 'd',
	'EXIT': 'ffff', #
}

# write hex file
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
	while '' in code_split:
		code_split.remove('')

	if len(code_split) > 0:
		opcode = code_split[0]
		args = code_split[1:]

		word0_first_half = '0000'
		word0_second_half = '0000'
		word1 = '00000000'

		if opcode == 'GOTO':
			if len(args) != 1:
				raise Exception(goto_exception_msg)

			opcode_val = op_codes_dict['GOTO']
			word0_second_half = opcode_val.zfill(4)
			word1 = util.int_to_hex(args[0]).zfill(8)

		if opcode == 'LD':
			if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
				raise Exception(
					exception_msg.format(opcode=opcode)
				)
			if re.search(r'R\[\d+]', args[1]):
				opcode_val = op_codes_dict['REGISTER TO REGISTER LOAD']
				word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

			else:
				opcode_val = op_codes_dict['DIRECT LOAD']
				word1 = util.int_to_hex(args[1]).zfill(8)

			word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
			word0_second_half = opcode_val.zfill(4)

		if opcode == 'ADD':
			if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
				raise Exception(
					exception_msg.format(opcode=opcode)
				)
			if re.search(r'R\[\d+]', args[1]):
				opcode_val = op_codes_dict['REGISTER TO REGISTER ADD']
				word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

			else:
				opcode_val = op_codes_dict['DIRECT ADD']
				word1 = util.int_to_hex(args[1]).zfill(8)

			word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
			word0_second_half = opcode_val.zfill(4)

		if opcode == 'SUB':
			if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
				raise Exception(
					exception_msg.format(opcode=opcode)
				)
			if re.search(r'R\[\d+]', args[1]):
				opcode_val = op_codes_dict['REGISTER TO REGISTER SUBTRACT']
				word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

			else:
				opcode_val = op_codes_dict['DIRECT SUBTRACT']
				word1 = util.int_to_hex(args[1]).zfill(8)

			word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
			word0_second_half = opcode_val.zfill(4)

		if opcode == 'MUL':
			if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
				raise Exception(
					exception_msg.format(opcode=opcode)
				)
			if re.search(r'R\[\d+]', args[1]):
				opcode_val = op_codes_dict['REGISTER TO REGISTER MULTIPLY']
				word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

			else:
				opcode_val = op_codes_dict['DIRECT MULTIPLY']
				word1 = util.int_to_hex(args[1]).zfill(8)

			word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
			word0_second_half = opcode_val.zfill(4)

		if opcode == 'DIV':
			if len(args) < 2 or not re.search(r'R\[\d+]', args[0]):
				raise Exception(
					exception_msg.format(opcode=opcode)
				)
			if re.search(r'R\[\d+]', args[1]):
				opcode_val = op_codes_dict['REGISTER TO REGISTER DIVIDE']
				word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

			else:
				opcode_val = op_codes_dict['DIRECT DIVIDE']
				word1 = util.int_to_hex(args[1]).zfill(8)

			word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)
			word0_second_half = opcode_val.zfill(4)

		if opcode == 'EXIT':
			opcode_val = op_codes_dict['EXIT']
			word0_second_half = opcode_val.zfill(4)

		hex_file_str += word0_first_half
		hex_file_str += word0_second_half
		hex_file_str += '\n'
		hex_file_str += word1
		hex_file_str += '\n\n'

# remove extra white space
hex_file_str = hex_file_str[:-1]

# write file
f = open(file_hex, 'w')
f.write(hex_file_str)
f.close()
