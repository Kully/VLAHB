'''
Virtual Machine

The vm is what would be the Printed Circuit Board
as well as the etched silicon and logic gates

For now, vm.py looks at the hex file (file.hex)
Eventually, vm.py will look at the binary (file.bin)

```
hhhhhhhh
hhhhhhhh
hhhhhhhh
hhhhhhhh
...
```

where `h` is a hexadecimal value (4 bits, 1/2 a byte) which takes on a value
between 0-f (16 unique values).

This is how 2 rows is interpreted

```
hhhh[index in RAM]hhhh[command]
hhhhhhhh[value]
```


An example of my setup:
```python
ROM = [
    '0x00030001',
    '0x00000004',
    '0x00030002',
    '0x00000006',
    '0x00030003',
    '0x00000001'
]

RAM = []
PC = 0  # program counter
```
'''
import string
import time
import util

# CPU constants and data structures
COMMANDS_PER_SEC = 10
DELAY_BETWEEN_COMMANDS = 1. / COMMANDS_PER_SEC  # in seconds
ROM = []
# TODO: make RAM dynamic - index as I go
RAM = [None] * 2**16
RAM_SIZE = 500  # in units of 4 bytes

def return_lines_from_file_hex(file_hex, remove_empty_lines=True):
    f = open(file_hex, 'r')
    lines = f.read().split('\n')

    if remove_empty_lines:
        while '' in lines:
            lines.remove('')
    f.close()
    return lines

def fill_ROM_with_hex_lines(hex_lines):
    for line in hex_lines:
        ROM.append(line)

def validate_hex_file(file_hex, remove_empty_lines=True):
    print('Validating hex file...')
    lines = return_lines_from_file_hex(file_hex)

    assert len(lines) % 2 == 0, util.EVEN_NUMBER_HEX_LINES_ERROR_MSG
    print('    even number of hex lines (ok)')

    assert all(len(line) == 8 for line in lines), util.CHARS_PER_LINE_ERROR_MSG
    print('    all lines in file.hex are 8 chars long (ok)')

    assert all(char in string.hexdigits + 'x' for char in "".join(lines)), util.VALID_HEX_VALUES_ERROR_MSG
    print('    all chars are valid hexadecimal (ok)')

    print('Validation:\n    PASS!\n')

def exec(lines_from_file_hex):
    '''Execute lines in ROM'''
    PC = 0
    while True:
        time.sleep(DELAY_BETWEEN_COMMANDS)
        # check if end of ROM
        try:
            ROM[PC]
            ROM[PC+1]
        except IndexError:
            break

        print('\nPC: %r'%PC)
        print('    next 2 lines in ROM:')
        print('        %s'%ROM[PC])
        print('        %s'%ROM[PC+1])

        # convert all hex to int
        GOTO = False
        index_in_RAM = util.hex_to_int(ROM[PC][:4])
        command = util.hex_to_int(ROM[PC][4:])
        value = util.hex_to_int(ROM[PC+1])

        print('    index_in_RAM: %s'%index_in_RAM)
        print('    command: %s'%command)
        print('    value: %s'%value)

        print('    RAM[0]: %s'%RAM[0])
        print('    RAM[1]: %s'%RAM[1])
        print('    RAM[2]: %s'%RAM[2])
        print('    RAM[3]: %s'%RAM[3])
        print('    RAM[4]: %s'%RAM[4])

        if command == 1:  # LD (load)
            RAM[index_in_RAM] = value

        elif command == 2:  # ADD
            if RAM[index_in_RAM] is None:
                RAM[index_in_RAM] = 0
            RAM[index_in_RAM] += value

        elif command == 3:  # SUB (subtract)
            if RAM[index_in_RAM] is None:
                RAM[index_in_RAM] = 0
            RAM[index_in_RAM] -= value

        elif command == 4:  # GOTO (go to)
            PC = value
            GOTO = True

        # increment program counter
        if not GOTO:
            PC += 2

myHexFileName = 'file.hex'
hex_lines = return_lines_from_file_hex(myHexFileName)
fill_ROM_with_hex_lines(hex_lines)
validate_hex_file(myHexFileName)
exec(hex_lines)

print('\nRAM after program is done:')
print('    %s'%RAM[:10])
