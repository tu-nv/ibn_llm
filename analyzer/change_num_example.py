import argparse
import copy
import os
import warnings
import time
import json
import numpy as np
import itertools
import scienceplots

import matplotlib.pyplot as plt
plt.style.use(['science','ieee', 'no-latex'])
plt.rcParams.update({'font.size': 12, 'hatch.linewidth': 0.25, 'hatch.color': 'gray', 'font.serif': 'DejaVu Sans',})
scriptDir = os.path.dirname(os.path.realpath(__file__))


def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, legend=True):
    """Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    hatches = ['xx', '..', '++', '//']
    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []
    max_y = 0

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            y_avg = np.mean(y)
            bar = ax.bar(x + x_offset, y_avg, yerr=np.std(y) if hasattr(y, "__len__") else None, ecolor="firebrick", capsize=3, hatch=hatches[i % len(hatches)], width=bar_width * single_width, fill=False)
            if max_y < y_avg: max_y = y_avg

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # plt.ylim([0, max_y*1.6])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())


if __name__ == '__main__':
    # data from summary.py


    accuracy_change_num_example_nfv_conf = {
        "data": {
            "no example":[57.5, 60.0, 30.0, 62.5, 51.667, 72.5],
            "1 example":[89.167,90.833,91.667,89.167, 93.33, 90.0],
            "3 examples":[90.833, 91.597,95.0, 95.0, 0, 0],
            "6 examples":[94.167, 92.5, 98.333, 96.667, 0, 0],
            "9 examples":[99.167, 97.414, 99.167, 98.333, 0, 0]
        },
        "ylim": (0, 100),
        "xticks" : ["qwen2:7b", "llama3.1:8b", "gemma2:9b", "gemma2:27b", "qwen2:72b", "llama3.1:70b"],
        "xlabel": "Model",
        "ylabel": "Accuracy (%)",
        "name": "accuracy_change_num_example_nfv_conf"
    }

    accuracy_change_num_example_formal_spec = {
        "data": {
            "no example":[97.587, 86.736, 80.448, 59.577, 98.01, 99.279, 99.328],
            "1 example":[98.682, 93.505, 93.234, 94.03, 97.63, 99.08, 99.627],
            "3 examples":[98.682, 95.156, 94.154, 97.55, 98.06, 0, 0],
            "6 examples":[98.856, 95.167, 95.1, 97.587, 98.308, 0, 0],
            "9 examples":[98.806, 95.025, 94.9, 97.413, 98.259, 0, 0 ]
        },
        "ylim": (50, 100),
        "xticks" : ['formal_spec_ft', "qwen2:7b", "llama3.1:8b", "gemma2:9b", "gemma2:27b", "qwen2:72b", "llama3.1:70b"],
        "xlabel": "Model",
        "ylabel": "Accuracy (%)",
        "name": "accuracy_change_num_example_formal_spec"
    }

    processing_time_change_num_example_nfv_conf = {
        "data": {
            "no example":[1.2, 1.2, 2.0, 3.6, 4.9, 5.9],
            "1 example":[1.1, 1.2, 1.7, 2.9, 5.6, 5.0],
            "3 examples":[1.2, 1.2, 1.7, 3.0, 0, 0],
            "6 examples":[1.3, 1.4, 2.0, 3.4, 0, 0],
            "9 examples":[1.3, 1.4, 2.0, 3.5, 0, 0]
        },
        "ylim": (0, 6),
        "xticks" : ["qwen2:7b", "llama3.1:8b", "gemma2:9b", "gemma2:27b", "qwen2:72b", "llama3.1:70b"],
        "xlabel": "Model",
        "ylabel": "Processing time (s)",
        "name": "processing_time_change_num_example_nfv_conf"
    }

    processing_time_change_num_example_formal_spec = {
        "data": {
            "no example":[1.5, 1.6, 1.7, 3.2, 5.9, 8.5, 8.3],
            "1 example":[1.7, 1.8, 1.8, 3.4, 5.5, 9.9, 8.7],
            "3 examples":[1.9, 2.0, 1.8, 3.1, 5.3, 0, 0],
            "6 examples":[2.3, 2.4, 2.2, 3.6, 6.6, 0, 0],
            "9 examples":[2.5, 2.6, 2.4, 3.9, 7.1,0,0 ]
        },
        "ylim": (0, 10),
        "xticks" : ['formal_spec_ft', "qwen2:7b", "llama3.1:8b", "gemma2:9b", "gemma2:27b", "qwen2:72b", "llama3.1:70b"],
        "xlabel": "Model",
        "ylabel": "Processing time (s)",
        "name": "processing_time_change_num_example_formal_spec"
    }

    for data in [accuracy_change_num_example_nfv_conf, accuracy_change_num_example_formal_spec, processing_time_change_num_example_formal_spec, processing_time_change_num_example_nfv_conf]:
        print(f'-----{data["name"]}-----')
        # for key in data["data"]:
        #     print(f'{key}: {np.average(data["data"][key])}')

        fig, ax = plt.subplots(figsize=(9, 4))
        # participants
        if data.get("xticks"):
            plt.xticks(range(len(data["xticks"])), data["xticks"], rotation=45, ha='right')
        if data.get('ylim'):
            plt.ylim(*data.get('ylim'))
        # plt.xlabel(data["xlabel"])
        plt.ylabel(data["ylabel"])

        bar_plot(ax, data["data"], total_width=.8, single_width=.9)
        ratio = 0.3
        xleft, xright = ax.get_xlim()
        ybottom, ytop = ax.get_ylim()
        ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
        ax.legend_.set_bbox_to_anchor((1, 1))
        plt.savefig(f'{scriptDir}/output/{data["name"]}.pdf', dpi=300, format='pdf')
        plt.clf()
