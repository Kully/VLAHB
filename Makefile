# TODO - add a debug flag -d for toggling print statements
# filename = ball_bouncing_off_walls.asm
filename = ball_bouncing_off_walls.asm

run:
	python3 asm.py $(filename)
	python3 vm.py

clean:  # empty /hex dir
	rm -f hex/*.hex

graph:
	python3 analysis.py