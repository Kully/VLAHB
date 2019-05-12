filename = dev.asm  # name of file in /asm

run:
	python asm.py $(filename);
	python vm.py

clean:
	rm -f hex/*.hex
