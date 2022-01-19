#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import itertools

AVG_RECALL_BP = 'Average completeness (bp)'
AVG_RECALL_BP_SEM = 'Std error of av. completeness (bp)'
AVG_PRECISION_BP = 'Average purity (bp)'
AVG_PRECISION_BP_SEM = 'Std error of av. purity (bp)'
ACCURACY_PER_BP = 'Accuracy (bp)'
UNFILTERED = ' (unfiltered)'
TOOL = 'Tool'
RANKS = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

DATASET_TO_TITLE = {'mar': 'Marine'}

DATASET_TO_PATH = {'mar': '../../binning/taxonomic_binning/marine_dataset/data/results/'}

DATASET_TO_TOOLS = {'mar': ['MEGAN (GSA)', 'Kraken (GSA)', 'DIAMOND (GSA)', 'Ganon (SR)']}


def get_colors():
    x = sns.color_palette('colorblind')
    return [x[0], x[1], x[2], x[0], x[1], x[2]]


def create_legend(metrics_list):
    def flip(items, ncol):
        return itertools.chain(*[items[i::ncol] for i in range(ncol)])

    colors_list = get_colors()

    colors_iter = iter(colors_list)
    lines = [Line2D([], [], lw=2, color=next(colors_iter), linestyle='solid' if 'unfiltered' in metric else 'dotted' , markeredgewidth=10, markeredgecolor='red') for metric in metrics_list]

    # metrics_list = metrics_labels(metrics_list)

    mlabels = []
    for metric in metrics_list:
        if 'unfiltered' in metric:
            mlabels.append(metric.rstrip(' (bp) (unfiltered)'))
        else:
            mlabels.append(metric.rstrip(' (bp)') + ' (1% filtered)')

    # fig = plt.figure(figsize=(0.5, 0.5))
    # fig.legend(flip(lines, 3), flip(mlabels, 3), loc='center', frameon=False, ncol=3, handletextpad=0.5)
    # fig.savefig(os.path.join(output_dir, 'legend.png'), dpi=200, format='png', bbox_inches='tight')
    # fig.savefig(os.path.join(output_dir, 'legend.pdf'), dpi=100, format='pdf', bbox_inches='tight')
    # plt.close(fig)


def plot_taxonomic_results(df_summary_t, metrics_list, errors_list, dataset, tools, axs):
    colors_list = get_colors()

    df_summary_t = df_summary_t.set_index(['Tool', 'rank']).reindex(tools, level=TOOL)

    num_cols = 2
    # fig, axs = plt.subplots(2, num_cols, figsize=(21, 7), sharex=True, sharey=True)

    x_values = range(len(RANKS))
    rank_to_index = dict(zip(RANKS, list(range(len(RANKS)))))
    rank_labels = list(map(str.capitalize, ['domain'] + RANKS[1:]))

    plot_and_fill = []

    col = 0
    row = 0

    for i, (tool, tool_group) in enumerate(df_summary_t.groupby(TOOL)):
        print(tool)

        axs[row, col].set_title(tool, fontsize=20, pad=5)
        axs[row, col].set(xlim=[0, 6], ylim=[-0.02, 1.02])

        # ratio = 0.9
        # xleft, xright = axs[row, col].get_xlim()
        # ybottom, ytop = axs[row, col].get_ylim()
        # axs[row, col].set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)

        for metric, error, xcolor in zip(metrics_list, errors_list, colors_list):
            metric_values = [0] * len(RANKS)
            metric_error = [0] * len(RANKS)
            for index, pd_row in tool_group.iterrows():
                rank = pd_row.name[1]
                index = rank_to_index[rank]
                metric_values[index] = .0 if np.isnan(pd_row[metric]) else pd_row[metric]
                metric_error[index] = .0 if (error == '' or np.isnan(pd_row[error])) else pd_row[error]

            plota = axs[row, col].plot(x_values, metric_values, color=xcolor, linewidth=2, linestyle='solid' if 'unfiltered' in metric else 'dashed')
            plotb = axs[row, col].fill_between(x_values, np.subtract(metric_values, metric_error).tolist(), np.add(metric_values, metric_error).tolist(), facecolor=xcolor, alpha=0.3, edgecolor=None)

            if col == 0:
                if error == '':
                    plot_and_fill.append(plota[0])
                else:
                    plot_and_fill.append((plota[0], plotb))

        axs[row, col].set_xticklabels(rank_labels, horizontalalignment='right', fontsize=16, rotation_mode='anchor')
        axs[row, col].tick_params(axis='x', labelrotation=45, pad=0)
        axs[row, col].tick_params(axis='y', labelsize=14, pad=0)

        # reduce number of ticks
        # axs[row, col].yaxis.set_major_locator(plt.MaxNLocator(5))

        if col == 0:
            yticks = axs[row, col].get_yticks()
            axs[row, col].set_yticklabels(['{:3.0f}'.format(y * 100) for y in yticks], fontsize=17)
        else:
            axs[row, col].set_yticklabels('')

        if row == 0:
            axs[row, col].set_xticklabels('')

        axs[row, col].grid(which='major', linestyle=':', linewidth='0.5')

        if (i + 1) % num_cols == 0:
            row += 1
            col = 0
        else:
            col += 1

    # fig.text(0.08, 0.5, 'Metric (%)', ha='center', va='center', rotation='vertical', size=25)
    axs[0, 0].text(-1.7, -0.44, 'Metric (%)', size=20, rotation='vertical')

    # plt.subplots_adjust(wspace=0.13, hspace=0.25)
    # fig.suptitle(DATASET_TO_TITLE[dataset], fontsize=28, y=1.01)


    def flip(items, ncol):
        return itertools.chain(*[items[i::ncol] for i in range(ncol)])

    colors_list = get_colors()

    colors_iter = iter(colors_list)
    lines = [Line2D([], [], lw=2, color=next(colors_iter), linestyle='solid' if 'unfiltered' in metric else 'dashed' , markeredgewidth=10, markeredgecolor='red') for metric in metrics_list]

    # metrics_list = metrics_labels(metrics_list)

    mlabels = []
    for metric in metrics_list:
        if 'unfiltered' in metric:
            mlabels.append(metric.rstrip(' (bp) (unfiltered)'))
        else:
            mlabels.append(metric.rstrip(' (bp)') + ' (1% filtered)')
    mlabels = [xx.replace('Average', 'Av.') for xx in mlabels]

    # axs[1,0].legend(flip(lines, 3), flip(mlabels, 3), loc='lower left', frameon=False, ncol=3, handletextpad=0.5,
    #                 bbox_to_anchor=(-0.25, -0.5), fontsize=20)
    leg = axs[1,0].legend(flip(lines, 3), flip(mlabels, 3), loc='lower left', frameon=False, ncol=1, handletextpad=0.5,
                          bbox_to_anchor=(-0.2, -1.43), fontsize=18,
                          borderaxespad=0.5, handlelength=1.5)
    for line in leg.get_lines():
        line.set_linewidth(4)

    # leg = ax.legend(subsets, loc='lower left', bbox_to_anchor=(-0.25, -0.4), fontsize=20, ncol=2, frameon=False,
    #                 handletextpad=0.2, columnspacing=1, borderaxespad=0.5, handlelength=1.5)
    # for line in leg.get_lines():
    #     line.set_linewidth(4)

    # fig.savefig(os.path.join(output_dir, 'taxonomic.pdf'), dpi=100, format='pdf', bbox_inches='tight')
    # fig.savefig(os.path.join(output_dir, 'taxonomic.png'), dpi=200, format='png', bbox_inches='tight')
    # plt.close(fig)


def main(dataset, ax):
    df_summary = pd.read_csv(DATASET_TO_PATH[dataset] + 'results_all.tsv', sep='\t')

    sample_dict = {'contigs': 'GSA', 'short reads': 'SR', 'long reads': 'LR'}
    df_summary['Tool'] = df_summary.apply(lambda row: '{} ({})'.format(row['Tool'], sample_dict[row['Sample']]), axis=1)

    df_summary = df_summary[df_summary['rank'].isin(RANKS)]

    metrics_list = [AVG_RECALL_BP + UNFILTERED, AVG_PRECISION_BP + UNFILTERED, ACCURACY_PER_BP + UNFILTERED]
    metrics_list += [AVG_RECALL_BP, AVG_PRECISION_BP, ACCURACY_PER_BP]

    errors_list = [AVG_RECALL_BP_SEM + UNFILTERED, AVG_PRECISION_BP_SEM + UNFILTERED, '', '', '', '']

    plot_taxonomic_results(df_summary, metrics_list, errors_list, dataset, DATASET_TO_TOOLS[dataset], ax)
