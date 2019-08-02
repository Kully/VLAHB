filename = array.asm

run:
	python3 asm.py $(filename)
	python3 vm.py # -O  # -O turns printing off

clean:
	rm -f hex/*.hex

graph:
	python3 run_analysis.py
