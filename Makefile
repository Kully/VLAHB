file_asm = clock.asm  # the assembly file you want to turn into hex
file_hex = clock.hex  # target hex file to create from .asm

run :
	python asm.py $(file_asm) $(file_hex);
	python vm.py $(file_hex);