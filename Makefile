file_asm = asm/math.asm
file_hex = math.hex

run:
	python asm.py $(file_asm) $(file_hex);
	python vm.py $(file_hex);

clean:
	rm -f *.hex
