filename = mario_nes.asm

run:
	python3 asm.py $(filename)
	python3 vm.py

clean:
	rm -f hex/*.hex

graph:
	python3 run_analysis.py