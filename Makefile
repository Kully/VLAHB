file_asm = file_test.asm
file_hex = file_test.hex

run :
	python asm.py $(file_asm) $(file_hex);
	python vm.py $(file_hex);