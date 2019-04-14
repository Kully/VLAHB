'''
Util Functions for VLAHB
'''

def return_lines_from_file_hex(file_hex, remove_empty_lines=True):
	f = open(file_hex, 'r')
	lines = f.read().split('\n')

	if remove_empty_lines:
		while '' in lines:
			lines.remove('')
	return lines
