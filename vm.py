# read hex file
f = open('file.hex', 'r')
lines_from_hex_file = f.readlines()
bin_file_string = ''


def hex_string_to_bin(x):
    return bin(int(x, 16))[2:]

is_op_code = True
for line in lines_from_hex_file:
    if line != '\n':
        bin_file_string += hex_string_to_bin(line)

print(bin_file_string)

# write bin file
