filename = array.asm
# filename = pride_flag.asm

run:
	python3 asm.py $(filename)
	python3 vm.py

clean:
	rm -f hex/*.hex

graph:
#   TODO: pick a designated script to test opcode speeds
# 	python3 asm.py opcode_speeds.asm
# 	python3 vm.py
	python3 run_analysis.py