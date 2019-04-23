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

# write hex file
hex_file_body = ''
for line in lines:
	line_split = line.split(';')[0].split(' ')
	while '' in line_split:
		line_split.remove('')

	opcode = line_split[0]
	args = line_split[1:]

	print(line_split)
	print(opcode)
	print(args)
	print('#####')

	word0_first_half = '0000'
	word0_second_half = '0000'
	word1 = '00000000'
	if opcode == 'LD':
		if len(args) < 2:
			raise Exception(
				'\nThe Opcode LD must be followed by 2 arguments '
				'either in the form:\n'
				'    LD R[X] R[Y]    \nor\n'
				'    LD R[X] Y'
			)

		word0_second_half = str(hex(2)[2:]).zfill(4)
		print('word0_second_half: %s' %word0_second_half)

		# should X in R[X] be hex or int?
		word0_first_half = re.search(r'R\[\d]', 'R[2]')  # TODO: correct this
