file_asm = asm/fibo.asm
file_hex = fibo.hex

run:
	python asm.py $(file_asm) $(file_hex);
	python vm.py $(file_hex);

clean:
	rm -f *.hex
