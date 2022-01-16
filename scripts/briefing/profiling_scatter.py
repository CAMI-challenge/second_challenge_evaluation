import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import os
import pandas as pd
from itertools import cycle


pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)


def get_colors_list(counts):
    cmaps = ['Purples', 'Reds_r', 'Greens', 'Purples_r', 'Blues_r', 'Greys_r', 'Greens_r', 'afmhot_r', 'pink', 'cool_r', 'Wistia', 'copper', 'bone_r']
    markers = ["o", "v", "^", "<", ">", "s"]
    markers_it = cycle(markers)
    markers2 = []
    colors_list = []

    for i, count in enumerate(counts):
        if isinstance(count, list):
            for j, b_val in enumerate(count):
                if b_val:
                    markers2.append(next(markers_it))
                else:
                    next(markers_it)

            colors = plt.get_cmap(cmaps[i])(np.linspace(.3, .7, len(count) + 1))[:-1]
            for color, b_val in zip(colors, count):
                if b_val:
                    colors_list.append(tuple(color))
        elif count != 0:
            for j in range(count):
                markers2.append(next(markers_it))

            if cmaps[i] == 'Purples':
                for xxx in range(count):
                    colors_list.append('orchid')
            elif cmaps[i] == 'afmhot_r':
                colors = plt.get_cmap(cmaps[i])(np.linspace(.3, .7, count + 2))[1:-1]
                for color in colors:
                    colors_list.append(tuple(color))
            else:
                colors = plt.get_cmap(cmaps[i])(np.linspace(.3, .7, count + 1))[:-1]
                for color in colors:
                    colors_list.append(tuple(color))
        else:
            next(markers_it)

    return colors_list, markers2


def plot_summary(counts, df_results, tools, xlabel, ylabel, metricx, metricy, axs):
    colors_list, markers = get_colors_list(counts)
    markers_it = iter(markers)

    df_mean = df_results.set_index('tool').loc[tools]

    # fig, axs = plt.subplots(figsize=(5.2, 4.8))

    axs.set_xlim([-2, 102])
    axs.set_ylim([-2, 102])

    # ratio = 1.0
    # xleft, xright = axs.get_xlim()
    # ybottom, ytop = axs.get_ylim()
    # axs.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)

    for i, (tool, df_row) in enumerate(df_mean.iterrows()):
        axs.errorbar(df_row[metricx + '_mean'], df_row[metricy + '_mean'], xerr=df_row[metricx + '_var'], yerr=df_row[metricy + '_var'],
                     fmt=next(markers_it),
                     ecolor=colors_list[i],
                     mec=colors_list[i],
                     mfc=colors_list[i],
                     capsize=3,
                     markersize=10,
                     capthick=2, elinewidth=2)

    # turn on grid
    axs.grid(which='major', linestyle=':', linewidth='0.5')

    axs.tick_params(axis='x', labelsize=16)
    axs.tick_params(axis='y', labelsize=16)
    axs.xaxis.set_major_locator(plt.MaxNLocator(6))

    plt.title('Marine', fontsize=20)

    axs.set_xlabel(xlabel, fontsize=20)
    axs.set_ylabel(ylabel, fontsize=20)

    create_legend(axs)


def create_legend(axs):
    labels = ['Bracken 2.2', 'CCMetagen 1.1.3', 'Centrifuge 1.0.4 beta', 'DUDes 0.08', 'DUDes cami1', 'FOCUS 1.5', 'FOCUS cami1', 'LSHVec gsa', 'Metalign 0.6.2 avg', 'MetaPalette 1.0.0', 'MetaPhlAn 2.9.22', 'MetaPhlAn cami1', 'MetaPhyler 1.25', 'mOTUs 2.5.1_2', 'mOTUs cami1', 'NBC++', 'TIPP 4.3.10', 'TIPP cami1']
    labels = [label if 'cami1' in label else label.split(' ')[0] for label in labels]
    labels = [label.replace('cami1', 'c1') for label in labels]
    counts = [1, 1, 1, 2, 2, 1, [True, False], 1, 2, 1, 2, 1, 2]
    colors_list, markers = get_colors_list(counts)

    colors_iter = iter(colors_list)
    markers_it = iter(markers)
    circles = [Line2D([], [], markeredgewidth=0.0, linestyle="None", marker=next(markers_it), markersize=14, markerfacecolor=next(colors_iter)) for label in labels]

    axs.legend(circles, labels, loc='lower left', frameon=False, ncol=3, handletextpad=-0.1, columnspacing=0.1,
               bbox_to_anchor=(-0.1, -0.65), fontsize=18)


def go(metricx, metricy, rank, workdir, tools, counts, ax):
    df_results = pd.read_csv(os.path.join(workdir, 'results.tsv'), sep='\t')
    df_results = df_results[df_results['tool'].isin(tools)]

    df_results = df_results[(df_results['metric'] == metricx) | (df_results['metric'] == metricy)]

    df_results['value'] = df_results['value'] * 100
    df_results = df_results[df_results['rank'] == rank]

    groups = df_results.groupby(['tool', 'metric'], sort=False)

    df_mean = groups.mean().reset_index()

    df_mean = df_mean.pivot_table(index=['tool'], columns='metric', values='value').reset_index() #.fillna(0)
    df_mean.rename(columns={metricy: metricy + '_mean', metricx: metricx + '_mean'}, inplace=True)

    df_var = groups.std().reset_index()
    df_var = df_var.pivot_table(index=['tool'], columns='metric', values='value').reset_index() #.fillna(0)
    df_var.rename(columns={metricy: metricy + '_var', metricx: metricx + '_var'}, inplace=True)

    df_results = pd.merge(df_mean, df_var, on=['tool'], how='outer')

    plot_summary(counts, df_results, tools,
             'Purity (%)',
             'Completeness (%)',
              metricx, metricy, ax)


def main(ax):
    rank = 'genus'

    workdir = '../../profiling/marine_dataset/results/OPAL_short_long_noplasmids/'
    counts = [1, 1, 1, 2, 2, 1, [True, False], 1, 2, 1, 2, 1, 2]

    tools = ['Bracken 2.2', 'CCMetagen 1.1.3', 'Centrifuge 1.0.4 beta', 'DUDes 0.08', 'DUDes cami1', 'FOCUS 1.5', 'FOCUS cami1', 'LSHVec gsa', 'Metalign 0.6.2 avg', 'MetaPalette 1.0.0', 'MetaPhlAn 2.9.22', 'MetaPhlAn cami1', 'MetaPhyler 1.25', 'mOTUs 2.5.1_2', 'mOTUs cami1', 'NBC++', 'TIPP 4.3.10', 'TIPP cami1']
    go('Purity', 'Completeness', rank, workdir, tools, counts, ax)

