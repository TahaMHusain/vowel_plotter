import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm


def draw_plot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 8))

    x_name = 'F2'
    y_name = 'F1'

    x = df[x_name]
    y = df[y_name]

    ax.scatter(x, y, marker="")

    cmap = cm.get_cmap('tab10')
    for v, color in zip(df.vowel.unique(), cmap.colors):
        x_data = df[x_name].loc[df.vowel == v]
        y_data = df[y_name].loc[df.vowel == v]
        for x, y in zip(x_data, y_data):
            ax.annotate(v, (x, y), fontsize=14, color=color)

    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.set_xlabel(x_name, fontsize=20)
    ax.set_ylabel(y_name, fontsize=20)
    ax.yaxis.tick_right()
    ax.xaxis.tick_top()
    ax.yaxis.set_label_position('right')
    ax.xaxis.set_label_position('top')

    plt.savefig('data/vowel_plot.png', format='png')
    plt.show()
