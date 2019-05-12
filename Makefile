filename = goose_math  # name of file in /asm w/o .asm

run:
	python asm.py $(filename);
	python vm.py

clean:
	rm -f hex/*.hex
