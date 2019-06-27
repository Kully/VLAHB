# TODO - add a debug flag -d for toggling print statements
filename = rotate_square.asm  # name of file in /asm you want to run

run:
	python3 asm.py $(filename)
	python3 vm.py

clean:  # empty /hex dir
	rm -f hex/*.hex
