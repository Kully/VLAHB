filename = test_inequality_operations.asm  # name of file in /asm you want to run

run:
	python asm.py $(filename)
	python vm.py

clean:  # remove all hex files in /hex
	rm -f hex/*.hex
