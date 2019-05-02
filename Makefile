file_asm = asm/recursion.asm
file_hex = recursion.hex

run:
	python asm.py $(file_asm) $(file_hex);
	python vm.py $(file_hex);

clean:
	rm -f *.hex
