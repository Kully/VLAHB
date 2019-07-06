import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

import plotly.offline as off

import numpy as np
import pandas as pd

from util import int_to_hex, op_codes_dict


def return_data_for_graph():
    x = []
    y = []
    text_array = []

    groups = df.groupby('opcode')
    for g in groups:
        mean_time_for_opcode = g[1]['time'].mean()
        opcode = list(g[1]['opcode'])[0]
        opcode_hex = int_to_hex(opcode)

        x.append(mean_time_for_opcode)
        y.append(inv_op_codes_dict[opcode_hex])
        text_array.append('hex: ' + opcode_hex.zfill(4))
       

    # order based on x
    zipped_pairs = zip(x, y) 
    sorted_y = [x for _, x in sorted(zipped_pairs)] 

    figure = {
        'data': [{
            'type': 'scatter',
            'mode': 'markers',
            'marker': {'color': 'rgb(15,140,256)'},
            'x': sorted_y,
            'y': sorted(x),
            'xaxis': 'x1',
            'yaxis': 'y1',
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

    return go.Scatter(figure['data'][0])


def return_data_for_table():
    hex_values = pd.Series(k.zfill(4) for k in inv_op_codes_dict.keys())
    opcode_values = pd.Series([inv_op_codes_dict[k] for k in inv_op_codes_dict.keys()])

    table_data = go.Table(
        domain=dict(x=[0.5, 1.0],
                    y=[0, 1.0]),
        columnwidth = [1,7],
        header=dict(values=['hex', 'opcode description'],
                    fill = dict(color='#C2D4FF'),
                    align = ['left'] * 2),
        cells=dict(
           values=[hex_values, opcode_values],
           fill = dict(color='#F5F8FF'),
           align = ['left'] * 2)
        )
    return table_data

if __name__ == "__main__":

    print('load data')
    df = pd.read_csv('data/opcodes_speed_data.csv')
    inv_op_codes_dict = {v: k for k, v in op_codes_dict.items()}

    print('generating chart...')
    table_data = return_data_for_table()
    scatter_data = return_data_for_graph()

    axis=dict(
        showline=True,
        zeroline=False,
        showgrid=True,
        mirror=True,
        ticklen=4,
        gridcolor='#ffffff',
        tickfont=dict(size=10)
    )

    layout = dict(
        autosize=True,
        margin = dict(l=40, r=40, b=150),
        showlegend=False,
        title='Opcode Execution Speed',
        xaxis1=dict(axis, **dict(domain=[0, 0.48], anchor='y1')),
        yaxis1=dict(axis, **dict(domain=[0, 1.0], range=[-0.001, 0.03], anchor='x1')),  
        plot_bgcolor='#F5F8FF',
    )

    fig = dict(data=[table_data, scatter_data], layout=layout)
    off.plot(fig, validate=False, show_link=False)
