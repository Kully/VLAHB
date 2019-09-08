import random

hex_values = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
color = '0XFF0000FF'  # red
how_many_steps = 320

script = ''

for _ in range(how_many_steps):
	random_color_idx = random.choice([2,3,4,5,6,7,8,9])
	color_digit = color[random_color_idx]
	idx_of_chosen_color_digit = hex_values.index(color_digit)

	# step up or down
	random_step = random.choice([-1,1])

	if idx_of_chosen_color_digit == len(hex_values) - 1:
		idx_of_chosen_color_digit -= 1
	elif idx_of_chosen_color_digit == 0:
		idx_of_chosen_color_digit += 1
	else:
		idx_of_chosen_color_digit += random_step

	color = color[:random_color_idx] + hex_values[idx_of_chosen_color_digit] + color[random_color_idx+1:]
	script += 'CLEAR %s\nBLIT\n' %color

script += 'EXIT\n'


f = open('madlib_clears.asm', 'w')
f.writelines(script)
print(script)
