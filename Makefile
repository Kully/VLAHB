filename = math

run:
	python asm.py $(filename);
	python vm.py hex/$(filename).hex;

clean:
	rm -f hex/*.hex
