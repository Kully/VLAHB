'''
Converts a hex file into binary

bin.py: HEX -> BIN
'''
binary = open('file.bin', 'wb')
binary.write(bytes(int('00', 16)))
binary.write(bytes(int('00', 16)))
binary.write(bytes(int('00', 16)))
binary.write(bytes(int('04', 16)))


# read hex file
# f = open('file.hex', 'r')
# lines_from_hex_file = f.readlines()
# bin_file_string = ''

# def hex_string_to_bin(x):
#     return bin(int(x, 16))[2:]

# for line in lines_from_hex_file:
#     if line != '\n':
#         bin_file_string += hex_string_to_bin(line)

# print(bin_file_string)

# write bin file
