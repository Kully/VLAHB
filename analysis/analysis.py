import numpy as np
import pandas as pd

import plotly.plotly as py

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

from util import int_to_hex, op_codes_dict

df = pd.read_csv('timing_the_opcodes.csv')
inv_op_codes_dict = {v: k for k, v in op_codes_dict.items()}


def return_figure_for_graph():
    x = []
    y = []
    text_array = []

    groups = df.groupby('opcode')
    for g in groups:
        mean_time_for_opcode = g[1]['time'].mean()
        opcode = list(g[1]['opcode'])[0]
        opcode_hex = int_to_hex(opcode)

        x.append(mean_time_for_opcode)
        y.append(inv_map[opcode_hex])
        text_array.append('hex: ' + opcode_hex.zfill(4))

    figure = {
        'data': [{
            'type': 'scatter',
            'mode': 'markers',
            'x': x,
            'y': y,
            'text': text_array,
            'showlegend': False,
        }],
        'layout': {
            'showlegend': False,
            'title': 'Opcodes against Run Time',
            'margin': {
                'l': 200
            },
            'xaxis': {'title': 'time (seconds)'}
        }
    }

    return figure


def return_figure_for_table():
    table_data = [['hex', 'opcode/example']] + [[k, inv_op_codes_dict[k]] for k in inv_op_codes_dict.keys()]
    figure_table = ff.create_table(table_data, height_constant=40)
    return figure_table


fig1 = return_figure_for_table()
fig2 = return_figure_for_graph()

# py.plot(return_figure_for_table(), filename='opcode to time table')
# py.plot(return_figure_for_table(), filename='opcode to time graph')

if __name__ == "__main__":
	fig1 = return_figure_for_table()
	fig2 = return_figure_for_graph()

	# make offline plots so a user doesn't need an account to use
	py.plot(return_figure_for_table(), filename='opcode to time table')
	py.plot(return_figure_for_table(), filename='opcode to time graph')

