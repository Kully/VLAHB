'''
Virtual Machine

The vm is what would be the PCB, etched silicon 

The file.hex that the vm looks at is of the form

```
hhhhhhhh
hhhhhhhh

hhhhhhhh
hhhhhhhh

...
```

where `h` is a hexadecimal value which takes on a value
between 0-f (16 unique values).

This is how 2 rows (32x2 bits) is interpreted

```
[index in RAM][command]
[value]
```

PC = program counter
'''
import pprint

ROM = []
RAM = [None] * 2**16
PC = []
ALU = ['+', '-', '*', '%']

def return_lines_from_file_hex(file_hex):
	f = open(file_hex, 'r')
	lines = f.read().split('\n')
	while '' in lines:
		lines.remove('')
	return lines

def hex_to_int(h):
	return int(h, 16)

def read_and_exec_hex_file(file_hex):
	lines_from_file_hex = return_lines_from_file_hex(file_hex)

	isCommand = True
	for PC, line in enumerate(lines_from_file_hex):
		print('PC: %r' %PC)
		print('line: %r\n' %line)
		if isCommand:
			index_in_register = hex_to_int(line[:4])
			command = line[4:]

		else:
			value = line
			if command == '0001':  # LD
				RAM[index_in_register] = hex_to_int(value)

			elif command == '0002':  # ADD
				if RAM[index_in_register] is None:
					RAM[index_in_register] = 0
				RAM[index_in_register] += hex_to_int(value)

			elif command == '0003':  # SUB
				if RAM[index_in_register] is None:
					RAM[index_in_register] = 0
				RAM[index_in_register] -= hex_to_int(value)

			elif command == '0004':  # GOTO
				pass
		isCommand = not isCommand


read_and_exec_hex_file('file.hex')
pprint.pprint(RAM[:11])
