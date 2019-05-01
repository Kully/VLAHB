file_asm = file_test.asm  # the assembly file you want to turn into hex
file_hex = file_test.hex  # target hex file to create from .asm

run :
	python asm.py $(file_asm) $(file_hex);
	python vm.py $(file_hex);