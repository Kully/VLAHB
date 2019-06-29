# TODO - add a debug flag -d for toggling print statements
filename = rotate_square_kully.asm
# filename = pride_flag.asm

run:
	python3 asm.py $(filename)
	python3 vm.py

clean:  # empty /hex dir
	rm -f hex/*.hex
