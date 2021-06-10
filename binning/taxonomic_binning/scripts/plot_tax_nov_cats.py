import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import numpy as np
import os, sys, inspect
import pandas as pd
import itertools

RANKS = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
RANK_TO_INDEX = dict(zip(RANKS, list(range(len(RANKS)))))

AVG_RECALL_BP = 'Average completeness (bp)'
AVG_RECALL_BP_SEM = 'Std error of av. completeness (bp)'
AVG_PRECISION_BP = 'Average purity (bp)'
AVG_PRECISION_BP_SEM = 'Std error of av. purity (bp)'
ACCURACY_PER_BP = 'Accuracy (bp)'
UNFILTERED = ' (unfiltered)'
TOOL = 'Tool'


def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])


def get_colors():
    x = sns.color_palette('colorblind')
    return [x[0], x[1], x[2], x[0], x[1], x[2]]


def plot_taxonomic_results(df_summary_t, metrics_list, errors_list, categories, output_dir):
    colors_list = get_colors()

    num_rows = len(df_summary_t.index.get_level_values(0).unique()) # df_summary_t['Tool'].nunique() - 1
    num_cols = len(categories)
    fontsize = 9

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(8, 6), sharex=True, sharey=True)

    row = 0
    plot_and_fill = []

    for tool, pd_resultsx in df_summary_t.groupby(TOOL):
        print('=======================================')
        print(tool)
        col = 0
        pd_results = pd_resultsx.reset_index()

        for i, category in enumerate(categories):
            pd_cat = pd_results[pd_results['category'] == category]


            for metric, error, color in zip(metrics_list, errors_list, colors_list):
                metric_values = [0] * len(RANKS)
                metric_error = [0] * len(RANKS)
                for index, pd_row in pd_cat.iterrows():
                    index = RANK_TO_INDEX[pd_row['rank']]
                    metric_values[index] = .0 if np.isnan(pd_row[metric]) else pd_row[metric]
                    metric_error[index] = .0 if (error == '' or np.isnan(pd_row[error])) else pd_row[error]

                x_values = range(len(RANKS))
                plota = axs[row, col].plot(x_values, metric_values, color=color, linewidth=1.2, linestyle='solid' if 'unfiltered' in metric else 'dotted')
                plotb = axs[row, col].fill_between(x_values, np.subtract(metric_values, metric_error).tolist(), np.add(metric_values, metric_error).tolist(), facecolor=color, alpha=0.3, edgecolor=None)

                if row == 0 and col == 0:
                    if error == '':
                        plot_and_fill.append(plota[0])
                    else:
                        plot_and_fill.append((plota[0], plotb))

            # force axes to be from 0 to 100%
            axs[row, col].set_xlim([0, len(RANKS)-1])
            axs[row, col].set_ylim([0.0, 1.0])

            if row == 0:
                axs[row, col].set_title(category.replace('_', ' '), fontsize=fontsize, pad=3)

            x_values = range(len(RANKS))

            plt.xticks(x_values)
            axs[row, col].set_xticklabels(['domain'] + RANKS[1:], rotation='60', fontsize=fontsize, horizontalalignment='right', rotation_mode='anchor')

            axs[row, col].tick_params(axis='x', pad=1, length=3 if row == num_rows - 1 else 0)

            axs[row, col].tick_params(axis='y', pad=1, labelsize=fontsize-1, length=3 if col == 0 else 0)

            vals = axs[row, col].get_yticks()
            axs[row, col].set_yticklabels(['{:3.0f}%'.format(x * 100) for x in vals])
            if col == 0:
                axs[row, col].set_ylabel(tool.split(' ')[0], fontsize=9, labelpad=4, backgroundcolor='0.8')

            axs[row, col].grid(which='major', linestyle=':', linewidth='0.5')

            # reduce number of ticks
            axs[row, col].yaxis.set_major_locator(plt.MaxNLocator(4))

            col += 1

        row += 1

    plt.subplots_adjust(hspace=0.1, wspace=0.1)

    mlabels = metrics_labels(metrics_list)

    lgd = plt.legend(flip(plot_and_fill[:6], 3), flip(mlabels, 3), bbox_to_anchor=(-1.9, 5.65), loc=8, borderaxespad=0., handlelength=1.5, frameon=False, fontsize=fontsize, ncol=3, handletextpad=.5)
    fig.savefig(os.path.join(output_dir, 'novelty_categories.pdf'), dpi=100, format='pdf', bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'novelty_categories.png'), dpi=200, format='png', bbox_inches='tight')
    plt.close()


def metrics_labels(metrics_list):
    mlabels = []
    for metric in metrics_list:
        if 'unfiltered' in metric:
            mlabels.append(metric.rstrip(' (bp) (unfiltered)'))
        else:
            mlabels.append(metric.rstrip(' (bp)') + ' (1% filtered)')
    return mlabels


def create_legend(metrics_list, output_dir):
    colors_list = get_colors()

    colors_iter = iter(colors_list)
    lines = [Line2D([], [], lw=2, color=next(colors_iter), linestyle='solid' if 'unfiltered' in metric else 'dotted' , markeredgewidth=10, markeredgecolor='red') for metric in metrics_list]

    metrics_list = metrics_labels(metrics_list)

    fig = plt.figure(figsize=(0.5, 0.5))
    fig.legend(flip(lines, 3), flip(metrics_list, 3), loc='center', frameon=False, ncol=3, handletextpad=0.5)
    fig.savefig(os.path.join(output_dir, 'legend.png'), dpi=200, format='png', bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'legend.pdf'), dpi=100, format='pdf', bbox_inches='tight')
    plt.close(fig)


def get_metrics():
    metrics_list = [AVG_RECALL_BP + UNFILTERED, AVG_PRECISION_BP + UNFILTERED, ACCURACY_PER_BP + UNFILTERED]
    metrics_list += [AVG_RECALL_BP, AVG_PRECISION_BP, ACCURACY_PER_BP]

    errors_list = [AVG_RECALL_BP_SEM + UNFILTERED, AVG_PRECISION_BP_SEM + UNFILTERED, '', '', '', '']

    return metrics_list, errors_list


def main(base_path, categories):
    metrics_list, errors_list = get_metrics()
    # create_legend(metrics_list, base_path)
    # exit()

    df_summaries = pd.DataFrame()
    for category in categories:
        df_summary = pd.read_csv(base_path + category + '/results.tsv', sep='\t')
        df_summary['category'] = category
        df_summaries = pd.concat([df_summaries, df_summary], ignore_index=True)

    df_summaries = df_summaries[df_summaries['Tool'] != 'Gold standard']
    print(df_summaries['Tool'].unique())

    df_summaries['Tool'] = df_summaries.apply(lambda row: row['Tool'].split(' ')[0], axis=1)

    tools = ['LSHVec', 'PhyloPythiaS+', 'Kraken', 'DIAMOND', 'MEGAN']

    df_summaries = df_summaries.set_index(['Tool', 'rank', 'category']).reindex(tools, level=TOOL)

    plot_taxonomic_results(df_summaries, metrics_list, errors_list, categories, base_path)


if __name__ == "__main__":
    main('../marine_dataset/data/results/deep_branching/',
         ['new_species', 'known_strain', 'new_strain', 'virus', 'plasmid'])
    main('../strain_madness_dataset/data/results/deep_branching/',
         ['new_species', 'new_strain'])
