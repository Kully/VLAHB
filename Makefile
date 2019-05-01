file_asm = file.asm
file_hex = myfile.hex

run :
	python asm.py $(file_asm) $(file_hex);
	python vm.py $(file_hex);