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

# TODO: opcodes dict

# write hex file
hex_file_body = ''
for line in lines:
	line_split = line.split(';')[0].split(' ')
	while '' in line_split:
		line_split.remove('')

	opcode = line_split[0]
	args = line_split[1:]

	# print(line_split)
	# print(opcode)
	# print(args)

	word0_first_half = '0000'
	word0_second_half = '0000'
	word1 = '00000000'

	if opcode == 'LD':  # 2, 7
		if len(args) < 2:
			raise Exception(
				'\nThe Opcode LD must be followed by 2 arguments '
				'either in the form:\n    LD R[X] R[Y]    \nor\n'
				'    LD R[X] Y'
			)

		if re.search(r'R\[\d+]', args[1]):
			word0_second_half = util.int_to_hex(7).zfill(4)
			word1 = util.int_to_hex(args[1][2:-1]).zfill(8)

		else:
			word0_second_half = util.int_to_hex(2).zfill(4)
			word1 = util.int_to_hex(args[1]).zfill(8)

		word0_first_half = util.int_to_hex(args[0][2:-1]).zfill(4)

	hex_file_body += word0_first_half
	hex_file_body += word0_second_half
	hex_file_body += '\n'
	hex_file_body += word1
	hex_file_body += '\n\n'

# write file
f = open(file_hex, 'w')
f.write(hex_file_body)
f.close()
