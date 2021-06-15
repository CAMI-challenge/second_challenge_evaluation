import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker


pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)

FILE = 'data/ground_truth/coverage_short/coverage_new{}.tsv'
RESULTS_BINS = 'results/amber_rhizosphere_noplasmids/bin_metrics.tsv'
RESULTS_GENOMES = 'results/amber_rhizosphere_noplasmids/genome_metrics_cami1.tsv'
FUNGI = 'data/ground_truth/coverage_short/fungal_metadata.tsv'


def create_colors_list():
    colors_list = []
    for color in plt.cm.tab10(np.linspace(0, 1, 10))[:-1]:
        colors_list.append(tuple(color))
    colors_list.append("black")
    for color in plt.cm.Set2(np.linspace(0, 1, 8)):
        colors_list.append(tuple(color))
    for color in plt.cm.Set3(np.linspace(0, 1, 12)):
        colors_list.append(tuple(color))
    return colors_list


COLORS = create_colors_list()


def plot_metric(pdres, metric, tools, axs):
    # handles = []

    for i, tool in enumerate(tools):
        pdres_tool = pdres[pdres['Tool'] == tool].copy().sort_values(by=['coverage', metric])

        pdres_tool1 = pdres_tool[pdres_tool['genome_id'] != 'GCF_000001735.4_TAIR10.1_genomic']
        pdres_tool2 = pdres_tool[pdres_tool['genome_id'] == 'GCF_000001735.4_TAIR10.1_genomic']

        axs.scatter(np.log(pdres_tool1['coverage']), pdres_tool1[metric], marker='o', label=tool, color=COLORS[i], s=[5] * pdres_tool1.shape[0], rasterized=True)
        axs.scatter(np.log(pdres_tool2['coverage']), pdres_tool2[metric], marker='x', label=tool, color=COLORS[i], s=[30] * pdres_tool2.shape[0], rasterized=True)

        rolling_mean = pdres_tool1[metric].rolling(window=10, min_periods=10).mean()
        axs.plot(np.log(pdres_tool1['coverage']), rolling_mean, color=COLORS[i])

    axs.set_ylim([-0.02, 1.02])

    axs.set_xticklabels(['{:,.1f}'.format(np.exp(x)) for x in axs.get_xticks()], fontsize=14)
    axs.set_yticklabels(['{:3.0f}'.format(x * 100) for x in axs.get_yticks()], fontsize=14)
    # plt.legend(loc='upper left', fontsize=11)

    # axs.set_xlim([-0.02, 1.02])


    axs.set_xlabel('Genome coverage', fontsize=14)
    if metric == 'precision_bp':
        axs.set_ylabel('Purity (%)', fontsize=14)
    elif metric == 'recall_bp':
        axs.set_ylabel('Completeness (%)', fontsize=14)

    axs.grid(which='major', linestyle=':', linewidth='0.5')

    # plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')
    # return handles


def remove_suffix(s):
    if s.endswith('.fasta'):
        s = s[:-6]
    if s.endswith('.contigs'):
        s = s[:-8]
    return s


def main():
    fungi = pd.read_csv(FUNGI, sep='\t', header=None)

    df = pd.concat([pd.read_csv(FILE.format(i), sep='\t', header=None) for i in range(21)], ignore_index=True)
    df[0] = df.apply(lambda row: remove_suffix(row[0]), axis=1)
    df = df.groupby(0).sum().reset_index().rename(columns={0: 'genome_id', 1: 'coverage'})
    df = df[df['genome_id'].isin(list(fungi[0]) + ['GCF_000001735.4_TAIR10.1_genomic'])]

    pdbins = pd.read_csv(RESULTS_BINS, sep='\t', dtype={'BINID': str})
    pdbins = pdbins[pdbins['Tool'] != 'Gold standard']
    pdbins = pd.merge(pdbins, df, on='genome_id', how='inner')

    pdgen = pd.read_csv(RESULTS_GENOMES, sep='\t', dtype={'BINID': str})
    pdgen = pdgen[pdgen['Tool'] != 'Gold standard']
    pdgen = pd.merge(pdgen, df, on='genome_id', how='inner')

    tools = pdgen['Tool'].unique()

    fig, axs = plt.subplots(1, 2, figsize=(8, 4))

    plot_metric(pdgen, 'recall_bp', tools, axs[0])
    plot_metric(pdbins, 'precision_bp', tools, axs[1])
    plt.subplots_adjust(wspace=0.35)

    circles = []
    circles.append(Line2D([], [], markeredgewidth=2.0, linestyle="None", marker="o", markersize=11, markerfacecolor='white', markeredgecolor='black'))
    circles.append(Line2D([], [], markeredgewidth=2.0, linestyle="None", marker="x", markersize=9, markerfacecolor='white', markeredgecolor='black')) #markeredgewidth=10,
    colors_iter = iter(COLORS)
    for x in range(len(tools)):
        circles.append(Line2D([], [], markeredgewidth=0.0, linestyle="None", marker="s", markersize=11, markerfacecolor=next(colors_iter)))
    lgd = plt.legend(circles, ['Fungi', '$\it{A. thaliana}$'] + list(tools), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handlelength=0, frameon=False, fontsize=14)

    fig.savefig('coverage.pdf', dpi=100, format='pdf', bbox_inches='tight', bbox_extra_artists=(lgd,))
    fig.savefig('coverage.png', dpi=200, format='png', bbox_inches='tight', bbox_extra_artists=(lgd,))
    plt.close(fig)


if __name__ == "__main__":
    main()
