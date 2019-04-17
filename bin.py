def hex_string_to_bin(x):
    return bin(int(x, 16))[2:]

def return_lines_from_file_hex(file_hex):
	f = open(file_hex, 'r')
	lines = f.read().split('\n')
	while '' in lines:
		lines.remove('')
	print('\n%r\n'%lines)
	return lines

lines_from_hex_file = return_lines_from_file_hex('file.hex')
for line in lines_from_hex_file:
	reversed_line = line[::-1]

	# each linej is 1 byte - hh
	line0 = reversed_line[:2]
	line1 = reversed_line[2:4]
	line2 = reversed_line[4:6]
	line3 = reversed_line[6:]
	print(line0)
	print(line1)
	print(line2)
	print(line3)
	print('')
	# load each hh into binary file


# f = open('file.hex', 'r')
# lines_from_hex_file = f.readlines()
# bin_file_string = ''

# for line in lines_from_hex_file:
#     if line != '\n':
#         bin_file_string += hex_string_to_bin(line)

# print(bin_file_string)


