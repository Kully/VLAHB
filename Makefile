# TODO - add a debug flag -d for toggling print statements
filename = 1111draw.asm  # name of file in /asm you want to run

run:
	python3 asm.py $(filename)
	python3 vm.py

clean:  # remove all hex files in /hex
	rm -f hex/*.hex
