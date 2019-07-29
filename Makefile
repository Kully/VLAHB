filename = array.asm

run:
	python3 asm.py $(filename)
	python3 vm.py -O  # remove -O to toggle debug printing

clean:
	rm -f hex/*.hex

graph:
	python3 run_analysis.py
