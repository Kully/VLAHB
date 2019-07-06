filename = ball_bouncing_off_walls.asm

run:
	python3 asm.py $(filename)
	python3 vm.py

clean:
	rm -f hex/*.hex

graph:
	python3 asm.py opcode_speeds.asm
	python3 vm.py
	python3 run_analysis.py